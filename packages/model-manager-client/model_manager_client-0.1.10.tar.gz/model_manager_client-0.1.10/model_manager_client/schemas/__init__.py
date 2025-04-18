"""
Schema definitions for the API
"""

from .inputs import TextInput, FileInput, UserContext, ModelRequest, BatchModelRequestItem, BatchModelRequest
from .outputs import ModelResponse, BatchModelResponse

__all__ = [
    # Model Inputs
    "TextInput",
    "FileInput",
    "UserContext",
    "ModelRequest",
    "BatchModelRequestItem",
    "BatchModelRequest",
    # Model Outputs
    "ModelResponse",
    "BatchModelResponse",
]
