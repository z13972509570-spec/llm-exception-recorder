#!/usr/bin/env python3
"""CLI 入口"""
import click
from src.llm_exception_recorder import ExceptionRecorder, get_recorder
from src.llm_exception_recorder.reporters import CLIReporter


@click.group()
def cli():
    """📚 LLM Exception Recorder - 错误记录与统计分析"""
    pass


@cli.command()
@click.option("--days", default=7, help="统计天数")
def stat(days):
    """📊 查看错误统计"""
    recorder = get_recorder()
    stats = recorder.get_stats(days)
    reporter = CLIReporter()
    reporter.show_stats(stats)


@cli.command()
@click.option("--limit", default=10, help="显示条数")
def list(limit):
    """📋 列出最近错误"""
    recorder = get_recorder()
    errors = recorder.list_errors(limit)
    reporter = CLIReporter()
    reporter.show_errors(errors)


@cli.command()
@click.option("--output", default="error_report.md", help="输出文件")
def export(output):
    """📤 导出错误报告"""
    recorder = get_recorder()
    stats = recorder.get_stats(30)
    from src.llm_exception_recorder.reporters import MarkdownReporter
    reporter = MarkdownReporter()
    path = reporter.generate(stats, output)
    click.echo(f"✅ 已导出到: {path}")


if __name__ == "__main__":
    cli()
