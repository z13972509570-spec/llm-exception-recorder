"""错误分类器 — 自动识别错误类型"""
from typing import Optional, Dict, List
from .models import ErrorType, RetryStrategy


class ErrorClassifier:
    """LLM 错误自动分类器"""

    # 错误模式映射
    ERROR_PATTERNS = {
        ErrorType.RATE_LIMIT: [
            "rate limit", "rate_limit", "quota", "exceeded", "too many requests",
            "请求频率", "配额", "超出限制"
        ],
        ErrorType.AUTH: [
            "authentication", "auth", "invalid api key", "unauthorized",
            "api key", "token", "认证", "密钥", "权限"
        ],
        ErrorType.INVALID_REQUEST: [
            "invalid request", "invalid_request", "parameter", "validation",
            "malformed", "invalid JSON", "参数", "格式"
        ],
        ErrorType.TIMEOUT: [
            "timeout", "timed out", "request timeout", "504", "超时"
        ],
        ErrorType.CONNECTION: [
            "connection", "connect", "network", "refused", "errno",
            "连接", "网络", "无法连接"
        ],
        ErrorType.SERVER_ERROR: [
            "internal error", "server error", "500", "502", "503", "服务器错误"
        ],
        ErrorType.CONTENT_FILTER: [
            "content filter", "content_filter", "blocked", "filtered",
            "harmful", "policy", "内容被过滤", "敏感词"
        ],
        ErrorType.MODEL_OVERLOADED: [
            "model overloaded", "overloaded", "busy", "模型过载", "忙碌"
        ],
        ErrorType.CONTEXT_LENGTH: [
            "context length", "max tokens", "too long", "上下文", "过长"
        ],
        ErrorType.QUOTA_EXCEEDED: [
            "quota exceeded", "insufficient quota", "配额", "额度"
        ],
    }

    # HTTP 状态码映射
    STATUS_CODE_MAP = {
        401: ErrorType.AUTH,
        403: ErrorType.AUTH,
        404: ErrorType.INVALID_REQUEST,
        408: ErrorType.TIMEOUT,
        413: ErrorType.CONTEXT_LENGTH,
        429: ErrorType.RATE_LIMIT,
        500: ErrorType.SERVER_ERROR,
        502: ErrorType.SERVER_ERROR,
        503: ErrorType.SERVER_ERROR,
        504: ErrorType.TIMEOUT,
    }

    def classify(self, error: Exception, status_code: Optional[int] = None) -> ErrorType:
        """自动分类错误类型"""
        error_msg = str(error).lower()

        # 1. 先检查状态码
        if status_code and status_code in self.STATUS_CODE_MAP:
            return self.STATUS_CODE_MAP[status_code]

        # 2. 匹配错误模式
        for error_type, patterns in self.ERROR_PATTERNS.items():
            for pattern in patterns:
                if pattern.lower() in error_msg:
                    return error_type

        return ErrorType.UNKNOWN

    def get_retry_strategy(self, error_type: ErrorType) -> RetryStrategy:
        """根据错误类型推荐重试策略"""
        strategies = {
            ErrorType.RATE_LIMIT: RetryStrategy(
                suggestion="exponential_backoff",
                max_retries=5,
                base_delay=2.0,
                max_delay=60.0,
                backoff_factor=2.0
            ),
            ErrorType.AUTH: RetryStrategy(
                suggestion="no_retry_check_key",
                max_retries=0,
                base_delay=0,
                max_delay=0,
                backoff_factor=1.0
            ),
            ErrorType.INVALID_REQUEST: RetryStrategy(
                suggestion="no_retry_fix_request",
                max_retries=0,
                base_delay=0,
                max_delay=0,
                backoff_factor=1.0
            ),
            ErrorType.TIMEOUT: RetryStrategy(
                suggestion="linear_backoff",
                max_retries=3,
                base_delay=5.0,
                max_delay=30.0,
                backoff_factor=1.5
            ),
            ErrorType.CONNECTION: RetryStrategy(
                suggestion="exponential_backoff",
                max_retries=4,
                base_delay=1.0,
                max_delay=30.0,
                backoff_factor=2.0
            ),
            ErrorType.SERVER_ERROR: RetryStrategy(
                suggestion="exponential_backoff",
                max_retries=5,
                base_delay=3.0,
                max_delay=60.0,
                backoff_factor=2.0
            ),
            ErrorType.CONTENT_FILTER: RetryStrategy(
                suggestion="no_retry_modify_prompt",
                max_retries=0,
                base_delay=0,
                max_delay=0,
                backoff_factor=1.0
            ),
            ErrorType.MODEL_OVERLOADED: RetryStrategy(
                suggestion="exponential_backoff",
                max_retries=10,
                base_delay=5.0,
                max_delay=120.0,
                backoff_factor=2.0
            ),
            ErrorType.CONTEXT_LENGTH: RetryStrategy(
                suggestion="reduce_context",
                max_retries=0,
                base_delay=0,
                max_delay=0,
                backoff_factor=1.0
            ),
            ErrorType.QUOTA_EXCEEDED: RetryStrategy(
                suggestion="no_retry_upgrade_plan",
                max_retries=0,
                base_delay=0,
                max_delay=0,
                backoff_factor=1.0
            ),
            ErrorType.UNKNOWN: RetryStrategy(
                suggestion="exponential_backoff",
                max_retries=3,
                base_delay=2.0,
                max_delay=30.0,
                backoff_factor=2.0
            ),
        }
        return strategies.get(error_type, strategies[ErrorType.UNKNOWN])

    def extract_tags(self, error: Exception, provider: str) -> List[str]:
        """提取错误标签"""
        tags = [provider.lower()]
        
        error_type = self.classify(error)
        tags.append(error_type.value.lower())
        
        error_msg = str(error).lower()
        
        # 添加关键词标签
        keywords = ["api", "network", "timeout", "quota", "auth"]
        for kw in keywords:
            if kw in error_msg:
                tags.append(kw)
        
        return list(set(tags))
