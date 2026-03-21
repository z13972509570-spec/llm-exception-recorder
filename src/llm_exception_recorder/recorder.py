"""核心记录器"""
import traceback
from typing import Optional, Dict, Any
from datetime import datetime
from .models import ErrorRecord, ErrorType, LLMError
from .classifiers import ErrorClassifier
from .storage import ErrorStorage


class ExceptionRecorder:
    """LLM 异常记录器"""

    def __init__(
        self,
        storage_dir: str = "./.llm_errors",
        provider: str = "openai",
        auto_analyze: bool = False
    ):
        self.storage = ErrorStorage(storage_dir)
        self.classifier = ErrorClassifier()
        self.default_provider = provider
        self.auto_analyze = auto_analyze

    def record(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        provider: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> ErrorRecord:
        """记录异常"""
        provider = provider or self.default_provider
        
        # 分类错误
        error_type = self.classifier.classify(error, status_code)
        
        # 提取标签
        tags = self.classifier.extract_tags(error, provider)
        
        # 获取重试策略
        retry_strategy = self.classifier.get_retry_strategy(error_type)
        
        # 构建记录
        record = ErrorRecord(
            provider=provider,
            error_type=error_type,
            status_code=status_code or self._extract_status_code(error),
            message=str(error),
            details=self._extract_details(error),
            context=context or {},
            tags=tags,
            retry_strategy=retry_strategy,
            stack_trace=traceback.format_exc(),
        )
        
        # 自动分析根因（可选）
        if self.auto_analyze:
            record = self._auto_analyze(record)
        
        # 保存
        self.storage.save(record)
        
        return record

    def _extract_status_code(self, error: Exception) -> Optional[int]:
        """从异常中提取状态码"""
        # 尝试从错误属性获取
        if hasattr(error, "status_code"):
            return error.status_code
        if hasattr(error, "response"):
            resp = error.response
            if hasattr(resp, "status_code"):
                return resp.status_code
        return None

    def _extract_details(self, error: Exception) -> dict:
        """提取错误详情"""
        details = {}
        
        # 尝试获取各种属性
        if hasattr(error, "response"):
            resp = error.response
            if hasattr(resp, "json"):
                try:
                    details["response"] = resp.json()
                except:
                    pass
            if hasattr(resp, "text"):
                details["response_text"] = resp.text
        
        if hasattr(error, "body"):
            details["body"] = error.body
        
        if hasattr(error, "param"):
            details["param"] = error.param
        
        if hasattr(error, "type"):
            details["error_type"] = error.type
        
        return details

    def _auto_analyze(self, record: ErrorRecord) -> ErrorRecord:
        """自动分析根因（简化版）"""
        # 简单规则映射
        solutions = {
            ErrorType.RATE_LIMIT: "增加重试间隔，使用指数退避策略",
            ErrorType.AUTH: "检查 API Key 是否正确，确认权限配置",
            ErrorType.INVALID_REQUEST: "检查请求参数格式，确保 JSON 格式正确",
            ErrorType.TIMEOUT: "增加超时时间，检查网络连接",
            ErrorType.CONNECTION: "检查网络状况，确认 VPN/代理设置",
            ErrorType.SERVER_ERROR: "服务端临时错误，等待后重试",
            ErrorType.CONTENT_FILTER: "修改提示词，避免敏感内容",
            ErrorType.MODEL_OVERLOADED: "模型负载高，建议稍后重试或切换模型",
            ErrorType.CONTEXT_LENGTH: "减少输入文本长度或使用摘要",
            ErrorType.QUOTA_EXCEEDED: "检查账户配额，考虑升级套餐",
        }
        
        record.solution = solutions.get(record.error_type, "请查看官方文档")
        
        # 根因分析
        root_causes = {
            ErrorType.RATE_LIMIT: "用户请求频率超过 API 服务商设定的限额",
            ErrorType.AUTH: "API Key 无效、过期或缺少必要权限",
            ErrorType.INVALID_REQUEST: "请求参数不符合 API 规范",
            ErrorType.TIMEOUT: "网络延迟或服务端响应缓慢",
            ErrorType.CONNECTION: "网络连接问题或服务端不可达",
            ErrorType.SERVER_ERROR: "服务端内部错误，通常是临时性的",
            ErrorType.CONTENT_FILTER: "提示词或内容触发了安全过滤",
            ErrorType.MODEL: "当前模型负载过高",
        }
        
        record.root_cause = root_causes.get(record.error_type, "未知原因")
        
        return record

    def get_stats(self, days: int = 7) -> ErrorStats:
        """获取错误统计"""
        return self.storage.get_stats(days)

    def list_errors(self, limit: int = 10) -> list:
        """列出最近错误"""
        errors = self.storage.load_recent(30)
        return errors[:limit]


# 全局记录器实例
_default_recorder: Optional[ExceptionRecorder] = None


def get_recorder() -> ExceptionRecorder:
    """获取默认记录器"""
    global _default_recorder
    if _default_recorder is None:
        _default_recorder = ExceptionRecorder()
    return _default_recorder


def record_exception(
    error: Exception,
    context: Optional[Dict] = None,
    provider: str = "openai"
) -> ErrorRecord:
    """快速记录异常的便捷函数"""
    return get_recorder().record(error, context, provider)
