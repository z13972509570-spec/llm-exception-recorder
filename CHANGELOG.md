# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-03-22

### Added
- 🎉 Initial release
- 🔴 自动捕获 11 种 LLM 错误类型
- 🏷️ 智能分类 + 自动标签提取
- 🔄 重试策略智能推荐
- 📊 错误统计与趋势分析
- 📤 Markdown/JSON 报告导出
- 💻 CLI 工具 (stat/list/export)
- 📚 完整文档 (架构/API/使用/配置)

### Supported Error Types
- RateLimitError
- AuthenticationError
- InvalidRequestError
- TimeoutError
- APIConnectionError
- InternalServerError
- ContentFilterError
- ModelOverloadedError
- ContextLengthExceededError
- QuotaExceededError
- UnknownError
