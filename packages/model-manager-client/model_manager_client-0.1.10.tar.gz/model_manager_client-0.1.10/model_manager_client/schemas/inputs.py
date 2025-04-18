from pydantic import BaseModel
from typing import List, Union, Optional

from model_manager_client.enums import ProviderType, InvokeType
from model_manager_client.enums.channel import Channel


class TextInput(BaseModel):
    text: str  # 文本内容


class FileInput(BaseModel):
    file_url: str  # 文件URL 或者 文件 Base64 编码


class UserContext(BaseModel):
    org_id: str  # 组织id
    user_id: str  # 用户id
    client_type: str  # 客户端类型，这里记录的是哪个服务请求过来的


class ThinkingConfig(BaseModel):
    include_thoughts: bool = True  # 是否在响应中包含思考过程
    thinking_budget: int  # 以令牌（tokens）为单位的思考预算


class BaseRequest(BaseModel):
    model_provider: ProviderType  # 供应商，如 "openai", "google" 等
    channel: Optional[Channel] = None  # 渠道：不同服务商之前有不同的调用SDK，这里指定是调用哪个SDK
    invoke_type: InvokeType = InvokeType.GENERATION  # 模型调用类型：generation-生成模型调用
    model_name: Optional[str] = None  # 具体模型名，如 "gpt-4o-mini", "gemini-2.0-flash" 等
    input: List[Union[TextInput, FileInput]]  # 传递给模型的输入内容，可以是文本、图像，用于生成响应
    stream: bool = False  # 是否流式输出，默认false
    instructions: Optional[str] = None  # （可选）system prompt
    max_output_tokens: Optional[int] = None  # （可选）限制模型生成响应时的最大 token 数
    temperature: Optional[float] = None  # （可选）采样温度，取值范围为 0 到 2
    top_p: Optional[float] = None  # （可选）称为 nucleus sampling 的采样方法的参数，表示只考虑累计概率质量为 top_p 的 token
    timeout: Optional[float] = None  # （可选）覆盖客户端默认的超时设置，单位为秒
    custom_id: Optional[str] = None  # （可选）用于批量请求时结果关联
    thinking_config: Optional[ThinkingConfig] = None  # （可选）思考功能配置


class ModelRequest(BaseRequest):
    user_context: UserContext  # 用户信息


class BatchModelRequestItem(BaseRequest):
    priority: Optional[int] = None  # （可选、预留字段）批量调用时执行的优先级


class BatchModelRequest(BaseModel):
    user_context: UserContext  # 用户信息
    items: List[BatchModelRequestItem]  # 批量请求项列表
