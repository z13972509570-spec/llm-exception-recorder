# 使用指南

## 快速开始

### 1. 安装

```bash
pip install llm-exception-recorder
```

### 2. 基础使用

```python
from llm_exception_recorder import ExceptionRecorder

recorder = ExceptionRecorder()

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )
except Exception as e:
    record = recorder.record(e, context={"model": "gpt-4"})
    print(f"错误已记录: {record.error_id}")
    print(f"错误类型: {record.error_type}")
    print(f"建议: {record.retry_strategy.suggestion}")
```

### 3. 装饰器模式

```python
from llm_exception_recorder import record_exception

@record_exception.on_error(provider="openai")
def call_llm(prompt: str):
    return client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
```

### 4. CLI 使用

```bash
# 查看统计
llm-err stat

# 查看最近错误
llm-err list --limit 20

# 导出报告
llm-err export --output report.md
```

## 最佳实践

### 1. 记录完整上下文

```python
recorder.record(e, context={
    "model": "gpt-4",
    "prompt": prompt[:100],  # 截断避免过大
    "tokens": token_count,
    "retry_count": retry_count,
    "request_id": request_id,
})
```

### 2. 结合重试策略

```python
import time

def call_with_retry(prompt, max_retries=5):
    for i in range(max_retries):
        try:
            return client.chat.completions.create(...)
        except Exception as e:
            record = recorder.record(e)
            strategy = record.retry_strategy
            
            if strategy.max_retries == 0:
                raise  # 不可重试的错误
            
            delay = strategy.base_delay * (strategy.backoff_factor ** i)
            time.sleep(min(delay, strategy.max_delay))
    
    raise Exception("Max retries exceeded")
```

### 3. 定期分析

```python
# 每天分析错误趋势
stats = recorder.get_stats(days=1)

if stats.by_type.get("RateLimitError", 0) > 10:
    print("⚠️  限流错误过多，建议降低请求频率")

if stats.by_type.get("TimeoutError", 0) > 5:
    print("⚠️  超时过多，建议增加超时时间")
```

## 集成示例

### OpenAI

```python
from openai import OpenAI
from llm_exception_recorder import ExceptionRecorder

client = OpenAI()
recorder = ExceptionRecorder(provider="openai")

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )
except Exception as e:
    recorder.record(e, context={"model": "gpt-4"})
```

### Anthropic

```python
from anthropic import Anthropic
from llm_exception_recorder import ExceptionRecorder

client = Anthropic()
recorder = ExceptionRecorder(provider="anthropic")

try:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
except Exception as e:
    recorder.record(e, context={"model": "claude-sonnet-4-20250514"})
```
