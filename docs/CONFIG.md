# 配置说明

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `LLM_ERR_STORAGE_DIR` | 错误记录存储目录 | `./.llm_errors` |
| `LLM_ERR_AUTO_ANALYZE` | 是否自动分析根因 | `false` |

## 存储配置

错误记录存储在 `./.llm_errors/` 目录下：

```
.llm_errors/
├── errors.json        # 所有错误记录
└── archives/          # 归档目录（可选）
    └── 2026-03.json
```

## 错误记录格式

```json
{
  "error_id": "err_20260322_061234_abc123",
  "timestamp": "2026-03-22T06:12:34Z",
  "provider": "openai",
  "error_type": "RateLimitError",
  "status_code": 429,
  "message": "Rate limit exceeded",
  "context": {
    "model": "gpt-4",
    "tokens": 1500
  },
  "tags": ["openai", "ratelimiterror", "api"],
  "retry_strategy": {
    "suggestion": "exponential_backoff",
    "max_retries": 5,
    "base_delay": 2.0
  }
}
```

## 自定义配置

```python
from llm_exception_recorder import ExceptionRecorder

recorder = ExceptionRecorder(
    storage_dir="/path/to/errors",  # 自定义存储路径
    provider="openai",              # 默认服务商
    auto_analyze=True               # 启用自动分析
)
```
