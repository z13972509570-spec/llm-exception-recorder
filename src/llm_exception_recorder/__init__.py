"""LLM Exception Recorder — 大模型异常自动收录规范文档"""
__version__ = "1.0.0"

from .recorder import ExceptionRecorder, record_exception
from .models import LLMError, ErrorRecord, ErrorType

__all__ = ["ExceptionRecorder", "record_exception", "LLMError", "ErrorRecord", "ErrorType"]
