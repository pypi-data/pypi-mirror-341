import asyncio
import atexit
import json
import logging
import os

import grpc
from typing import Optional, AsyncIterator, Union

from .auth import JWTAuthHandler
from .exceptions import ConnectionError, ValidationError
from .schemas import ModelRequest, ModelResponse, TextInput, FileInput, BatchModelRequest, BatchModelResponse
from .generated import model_service_pb2, model_service_pb2_grpc

if not logging.getLogger().hasHandlers():
    # 配置日志格式
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

logger = logging.getLogger(__name__)


class AsyncModelManagerClient:
    def __init__(
            self,
            server_address: Optional[str] = None,
            jwt_secret_key: Optional[str] = None,
            jwt_token: Optional[str] = None,
            default_payload: Optional[dict] = None,
            token_expires_in: int = 3600,
            max_retries: int = 3,  # 最大重试次数
            retry_delay: float = 1.0,  # 初始重试延迟（秒）
    ):
        # 服务端地址
        self.server_address = server_address or os.getenv("MODEL_MANAGER_SERVER_ADDRESS")
        if not self.server_address:
            raise ValueError("Server address must be provided via argument or environment variable.")
        self.default_invoke_timeout = float(os.getenv("MODEL_MANAGER_SERVER_INVOKE_TIMEOUT", 30.0))

        # JWT 配置
        self.jwt_secret_key = jwt_secret_key or os.getenv("MODEL_MANAGER_SERVER_JWT_SECRET_KEY")
        self.jwt_handler = JWTAuthHandler(self.jwt_secret_key)
        self.jwt_token = jwt_token  # 用户传入的 Token（可选）
        self.default_payload = default_payload
        self.token_expires_in = token_expires_in

        # === TLS/Authority 配置 ===
        self.use_tls = os.getenv("MODEL_MANAGER_SERVER_GRPC_USE_TLS", "true").lower() == "true"
        self.default_authority = os.getenv("MODEL_MANAGER_SERVER_GRPC_DEFAULT_AUTHORITY")

        # === 重试配置 ===
        self.max_retries = max_retries if max_retries is not None else int(
            os.getenv("MODEL_MANAGER_SERVER_GRPC_MAX_RETRIES", 3))
        self.retry_delay = retry_delay if retry_delay is not None else float(
            os.getenv("MODEL_MANAGER_SERVER_GRPC_RETRY_DELAY", 1.0))

        # === gRPC 通道相关 ===
        self.channel: Optional[grpc.aio.Channel] = None
        self.stub: Optional[model_service_pb2_grpc.ModelServiceStub] = None
        self._closed = False
        atexit.register(self._safe_sync_close)  # 注册进程退出自动关闭

    def _build_auth_metadata(self) -> list:
        if not self.jwt_token and self.jwt_handler:
            self.jwt_token = self.jwt_handler.encode_token(self.default_payload, expires_in=self.token_expires_in)
        return [("authorization", f"Bearer {self.jwt_token}")] if self.jwt_token else []

    async def _ensure_initialized(self):
        """初始化 gRPC 通道，支持 TLS 与重试机制"""
        if self.channel and self.stub:
            return

        retry_count = 0
        options = []
        if self.default_authority:
            options.append(("grpc.default_authority", self.default_authority))

        while retry_count <= self.max_retries:
            try:
                if self.use_tls:
                    credentials = grpc.ssl_channel_credentials()
                    self.channel = grpc.aio.secure_channel(
                        self.server_address,
                        credentials,
                        options=options
                    )
                    logger.info("🔐 Using secure gRPC channel (TLS enabled)")
                else:
                    self.channel = grpc.aio.insecure_channel(
                        self.server_address,
                        options=options
                    )
                    logger.info("🔓 Using insecure gRPC channel (TLS disabled)")
                await self.channel.channel_ready()
                self.stub = model_service_pb2_grpc.ModelServiceStub(self.channel)
                logger.info(f"✅ gRPC channel initialized to {self.server_address}")
                return
            except grpc.FutureTimeoutError as e:
                logger.warning(f"❌ gRPC channel initialization timed out: {str(e)}")
            except grpc.RpcError as e:
                logger.warning(f"❌ gRPC channel initialization failed: {str(e)}")
            except Exception as e:
                logger.warning(f"❌ Unexpected error during channel initialization: {str(e)}")

            retry_count += 1
            if retry_count > self.max_retries:
                raise ConnectionError(f"❌ Failed to initialize gRPC channel after {self.max_retries} retries.")

            # 指数退避：延迟时间 = retry_delay * (2 ^ (retry_count - 1))
            delay = self.retry_delay * (2 ** (retry_count - 1))
            logger.info(f"🚀 Retrying connection (attempt {retry_count}/{self.max_retries}) after {delay:.2f}s delay...")
            await asyncio.sleep(delay)

    async def _stream(self, model_request, metadata, invoke_timeout) -> AsyncIterator[ModelResponse]:
        try:
            async for response in self.stub.Invoke(model_request, metadata=metadata, timeout=invoke_timeout):
                yield ModelResponse(
                    content=response.content,
                    usage=json.loads(response.usage) if response.usage else None,
                    raw_response=json.loads(response.raw_response) if response.raw_response else None,
                    error=response.error or None,
                )
        except grpc.RpcError as e:
            raise ConnectionError(f"gRPC call failed: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Invalid input: {str(e)}")

    async def invoke(self, model_request: ModelRequest, timeout: Optional[float] = None) -> Union[
        ModelResponse, AsyncIterator[ModelResponse]]:
        """
       通用调用模型方法。

        Args:
            model_request: ModelRequest 对象，包含请求参数。

        Yields:
            ModelResponse: 支持流式或非流式的模型响应

        Raises:
            ValidationError: 输入验证失败。
            ConnectionError: 连接服务端失败。
        """
        await self._ensure_initialized()

        if not self.default_payload:
            self.default_payload = {
                "org_id": model_request.user_context.org_id or "",
                "user_id": model_request.user_context.user_id or ""
            }

        # 构造 InputItem 列表
        input_items = []
        for item in model_request.input:
            if isinstance(item, TextInput):
                input_items.append(model_service_pb2.InputItem(
                    text=model_service_pb2.TextInput(
                        text=item.text
                    )
                ))
            elif isinstance(item, FileInput):
                input_items.append(model_service_pb2.InputItem(
                    file=model_service_pb2.FileInput(
                        file_url=item.file_url
                    )
                ))
            else:
                raise ValidationError("Invalid input type, must be TextInput or ImageInput.")
        thinking_config = None
        if model_request.thinking_config and model_request.thinking_config.thinking_budget > 0:
            thinking_config = model_service_pb2.ThinkingConfig(
                include_thoughts=model_request.thinking_config.include_thoughts,
                thinking_budget=model_request.thinking_config.thinking_budget,
            )

        request = model_service_pb2.ModelRequestItem(
            model_provider=model_request.model_provider.value,
            model_name=model_request.model_name or "",
            channel=model_request.channel.value if model_request.channel else "",
            invoke_type=model_request.invoke_type.value,
            input=model_service_pb2.Input(contents=input_items),
            stream=model_request.stream,
            instructions=model_request.instructions or "",
            max_output_tokens=model_request.max_output_tokens or 0,
            temperature=model_request.temperature or 0.0,
            top_p=model_request.top_p or 0.0,
            timeout=model_request.timeout or 0.0,
            org_id=model_request.user_context.org_id,
            user_id=model_request.user_context.user_id,
            client_type=model_request.user_context.client_type,
            priority=1,
            custom_id=model_request.custom_id or "",
            thinking_config=thinking_config,
        )

        metadata = self._build_auth_metadata()

        invoke_timeout = timeout or self.default_invoke_timeout
        if model_request.stream:
            return self._stream(request, metadata, invoke_timeout)
        else:
            async for response in self.stub.Invoke(request, metadata=metadata, timeout=invoke_timeout):
                return ModelResponse(
                    content=response.content,
                    usage=json.loads(response.usage) if response.usage else None,
                    raw_response=json.loads(response.raw_response) if response.raw_response else None,
                    error=response.error or None,
                    custom_id=model_request.custom_id or None,
                    request_id=response.request_id if response.request_id else None,
                )

    async def invoke_batch(self, batch_request_model: BatchModelRequest, timeout: Optional[float] = None) -> \
            BatchModelResponse:
        """
        批量模型调用接口

        Args:
            batch_request_model: 多条 BatchModelRequest 输入
            timeout: 调用超时，单位秒

        Returns:
            BatchModelResponse: 批量请求的结果
        """
        await self._ensure_initialized()

        if not self.default_payload:
            self.default_payload = {
                "org_id": batch_request_model.user_context.org_id or "",
                "user_id": batch_request_model.user_context.user_id or ""
            }

        metadata = self._build_auth_metadata()

        # 构造批量请求
        items = []
        for model_request_item in batch_request_model.items:
            # 构建 input contents
            input_items = []
            for item in model_request_item.input:
                if isinstance(item, TextInput):
                    input_items.append(model_service_pb2.InputItem(
                        text=model_service_pb2.TextInput(text=item.text)
                    ))
                elif isinstance(item, FileInput):
                    input_items.append(model_service_pb2.InputItem(
                        file=model_service_pb2.FileInput(file_url=item.file_url)
                    ))

            # 构建 ModelRequestItem
            req_item = model_service_pb2.ModelRequestItem(
                model_provider=model_request_item.model_provider.value,
                model_name=model_request_item.model_name or "",
                channel=model_request_item.channel.value if model_request_item.channel else "",
                invoke_type=model_request_item.invoke_type.value,
                input=model_service_pb2.Input(contents=input_items),
                stream=False,
                instructions=model_request_item.instructions or "",
                max_output_tokens=model_request_item.max_output_tokens or 0,
                temperature=model_request_item.temperature or 0.0,
                top_p=model_request_item.top_p or 0.0,
                org_id=batch_request_model.user_context.org_id,
                user_id=batch_request_model.user_context.user_id,
                client_type=batch_request_model.user_context.client_type,
                priority=model_request_item.priority or 1,
                custom_id=model_request_item.custom_id or "",
            )
            items.append(req_item)

        try:
            # 超时处理逻辑
            invoke_timeout = timeout or self.default_invoke_timeout

            # 调用 gRPC 接口
            response = await self.stub.BatchInvoke(
                model_service_pb2.ModelRequest(items=items),
                timeout=invoke_timeout,
                metadata=metadata
            )

            result = []
            for res_item in response.items:
                result.append(ModelResponse(
                    content=res_item.content,
                    usage=json.loads(res_item.usage) if res_item.usage else None,
                    raw_response=json.loads(res_item.raw_response) if res_item.raw_response else None,
                    error=res_item.error or None,
                    custom_id=res_item.custom_id if res_item.custom_id else None
                ))
            return BatchModelResponse(
                request_id=response.request_id if response.request_id else None,
                responses=result
            )
        except grpc.RpcError as e:
            raise ConnectionError(f"BatchInvoke failed: {str(e)}")

    async def close(self):
        """关闭 gRPC 通道"""
        if self.channel and not self._closed:
            await self.channel.close()
            self._closed = True
            await self.channel.close()
            logger.info("✅ gRPC channel closed")

    def _safe_sync_close(self):
        """进程退出时自动关闭 channel（事件循环处理兼容）"""
        if self.channel and not self._closed:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(self.close())
                else:
                    loop.run_until_complete(self.close())
            except Exception as e:
                logger.warning(f"❌ gRPC channel close failed at exit: {e}")

    async def __aenter__(self):
        """支持 async with 自动初始化连接"""
        await self._ensure_initialized()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """支持 async with 自动关闭连接"""
        await self.close()
