"""报告生成器"""
import json
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


class CLIReporter:
    """CLI 报告输出"""

    def __init__(self):
        self.console = Console()

    def show_stats(self, stats):
        """显示统计信息"""
        if stats.total_errors == 0:
            self.console.print("\n✅ [green]暂无错误记录[/]\n")
            return

        self.console.print(f"\n📊 [bold]错误统计 (过去 7 天)[/]\n")

        # 摘要
        table = Table(show_header=False)
        table.add_column("指标", style="cyan")
        table.add_column("数值", style="green")
        table.add_row("总错误数", str(stats.total_errors))
        if stats.avg_response_time:
            table.add_row("平均响应时间", f"{stats.avg_response_time:.2f}s")
        if stats.error_rate:
            table.add_row("错误率", f"{stats.error_rate*100:.1f}%")
        self.console.print(table)

        # 按类型
        self.console.print("\n[bold]按错误类型:[/]")
        for item in stats.top_errors:
            self.console.print(f"  • {item['type']}: {item['count']}")

    def show_errors(self, errors: list):
        """显示错误列表"""
        if not errors:
            self.console.print("[yellow]暂无错误记录[/]")
            return

        self.console.print(f"\n📋 [bold]最近 {len(errors)} 条错误[/]\n")

        for e in errors:
            ts = e.get("timestamp", "")[:19]
            et = e.get("error_type", "Unknown")
            msg = e.get("message", "")[:60]
            
            self.console.print(f"  [{ts}] {et}")
            self.console.print(f"    {msg}...\n")


class MarkdownReporter:
    """Markdown 报告生成"""

    def generate(self, stats, output: str = "error_report.md"):
        md = f"""# LLM 错误统计报告

生成时间: {stats.timestamp if hasattr(stats, 'timestamp') else ''}

## 概览

- **总错误数**: {stats.total_errors}
- **错误类型数**: {len(stats.by_type)}
- **服务商数**: {len(stats.by_provider)}

## 按错误类型

| 类型 | 数量 |
|------|------|
"""
        for item in stats.top_errors:
            md += f"| {item['type']} | {item['count']} |\n"

        Path(output).write_text(md, encoding="utf-8")
        return output
