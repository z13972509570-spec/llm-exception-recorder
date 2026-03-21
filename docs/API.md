# API 文档

## ExceptionRecorder

主记录器类。

### 构造函数

```python
ExceptionRecorder(
    storage_dir: str = "./.llm_errors",  # 存储目录
    provider: str = "openai",            # 默认服务商
    auto_analyze: bool = False           # 自动分析根因
)
```

### 方法

#### `record()`

记录异常。

```python
def record(
    self,
    error: Exception,              # 异常对象
    context: Optional[Dict] = None, # 上下文信息
    provider: Optional[str] = None, # 服务商名称
    status_code: Optional[int] = None  # HTTP 状态码
) -> ErrorRecord
```

**示例**:
```python
recorder = ExceptionRecorder()

try:
    response = client.chat.completions.create(...)
except Exception as e:
    record = recorder.record(
        e,
        context={"model": "gpt-4", "tokens": 1500},
        provider="openai"
    )
    print(record.error_id)  # err_20260322_061234_abc123
```

#### `get_stats()`

获取错误统计。

```python
def get_stats(self, days: int = 7) -> ErrorStats
```

**返回**:
- `total_errors`: 总错误数
- `by_type`: 按类型统计
- `by_provider`: 按服务商统计
- `top_errors`: 高频错误 Top 5

#### `list_errors()`

列出最近错误。

```python
def list_errors(self, limit: int = 10) -> List[dict]
```

---

## ErrorClassifier

错误分类器。

### 方法

#### `classify()`

自动分类错误类型。

```python
def classify(
    self,
    error: Exception,
    status_code: Optional[int] = None
) -> ErrorType
```

#### `get_retry_strategy()`

获取重试策略。

```python
def get_retry_strategy(self, error_type: ErrorType) -> RetryStrategy
```

---

## 便捷函数

### `record_exception()`

快速记录异常。

```python
from llm_exception_recorder import record_exception

record_exception(e, context={"model": "gpt-4"})
```
