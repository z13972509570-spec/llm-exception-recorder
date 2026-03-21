# 📚 LLM Exception Recorder

> 每次大模型 API 异常自动收录规范文档 — 建立 LLM 错误知识库，自动归类、统计、根因分析

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ 核心特性

- 🔴 **自动捕获**：拦截所有 LLM API 异常（OpenAI/Anthropic/Ollama/Google 等）
- 📋 **规范记录**：每次异常生成结构化文档（JSON + Markdown）
- 🏷️ **自动归类**：基于错误类型、状态码、错误信息自动打标签
- 📊 **统计分析**：错误趋势、频率、高发问题一键统计
- 🔍 **根因分析**：AI 自动分析错误根因，给出解决方案
- 🔄 **重试建议**：根据错误类型智能推荐重试策略
- 📤 **多端同步**：支持本地文件 + GitHub Gist + Notion 同步

## 🚀 快速开始

### 安装

```bash
pip install llm-exception-recorder
```

### Python 使用

```python
from llm_exception_recorder import ExceptionRecorder, LLMError

recorder = ExceptionRecorder()

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )
except Exception as e:
    # 自动记录异常
    recorder.record(e, context={"model": "gpt-4", "prompt": "Hello"})
```

### CLI 使用

```bash
# 查看错误统计
llm-err stat

# 查看最近错误
llm-err list --limit 10

# 导出错误报告
llm-err export --format markdown

# 分析根因
llm-err analyze --id <error_id>
```

## 📋 错误文档结构

每次异常自动生成：

```json
{
  "error_id": "err_20260322_061234_abc123",
  "timestamp": "2026-03-22T06:12:34Z",
  "provider": "openai",
  "error_type": "RateLimitError",
  "status_code": 429,
  "message": "Rate limit exceeded",
  "details": {...},
  "context": {
    "model": "gpt-4",
    "tokens": 1500,
    "retry_count": 3
  },
  "tags": ["rate_limit", "quota", "api"],
  "root_cause": "用户 API 调用频率超过限额",
  "solution": "增加重试间隔或升级配额",
  "retry_strategy": {
    "suggestion": "exponential_backoff",
    "max_retries": 5,
    "base_delay": 2
  }
}
```

## 🏷️ 支持的错误类型

| 错误类型 | 描述 | 解决方案 |
|---------|------|---------|
| RateLimitError | 调用频率超限 | 指数退避重试 |
| AuthenticationError | 认证失败 | 检查 API Key |
| InvalidRequestError | 请求参数错误 | 检查请求格式 |
| TimeoutError | 请求超时 | 增加超时时间 |
| APIConnectionError | 连接失败 | 检查网络 |
| InternalServerError | 服务端错误 | 重试 |
| ContentFilterError | 内容被过滤 | 修改提示词 |
| ModelOverloadedError | 模型过载 | 等待后重试 |

## 📊 输出示例

```
📚 LLM Exception Recorder
========================

📈 错误统计 (过去 7 天)

🔴 RateLimitError    ████████████  45%  (23次)
🟠 TimeoutError      ██████        22%  (11次)
🟡 APIConnectionErr ████          18%  (9次)
🟢 InvalidRequestErr██             15%  (8次)

⏱️  平均响应时间: 2.3s
📉  错误率: 12.3%

🔧 建议:
  - 建议增加指数退避重试策略
  - 考虑使用批量 API 减少请求次数
  - 建议配置备用模型
```

## 📁 目录结构

```
llm-exception-recorder/
├── src/
│   └── llm_exception_recorder/
│       ├── __init__.py
│       ├── recorder.py       # 核心记录器
│       ├── classifiers.py   # 错误分类器
│       ├── analyzer.py      # 根因分析
│       ├── reporters.py     # 报告生成
│       └── storage.py       # 本地存储
├── cli/
│   └── main.py              # CLI 入口
├── templates/
│   └── error_template.md    # 错误文档模板
└── tests/
```

## 📄 License

MIT © 2026
