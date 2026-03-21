"""本地存储"""
import json
import os
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timedelta
from .models import ErrorRecord, ErrorStats


class ErrorStorage:
    """错误记录本地存储"""

    def __init__(self, storage_dir: str = "./.llm_errors"):
        self.storage_dir = Path(storage_dir)
        self.errors_file = self.storage_dir / "errors.json"
        self._ensure_storage()

    def _ensure_storage(self):
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        if not self.errors_file.exists():
            self.errors_file.write_text("[]", encoding="utf-8")

    def save(self, record: ErrorRecord):
        """保存错误记录"""
        errors = self.load_all()
        errors.append(record.to_dict())
        
        with open(self.errors_file, "w", encoding="utf-8") as f:
            json.dump(errors, f, indent=2, ensure_ascii=False)

    def load_all(self) -> List[dict]:
        """加载所有错误记录"""
        try:
            with open(self.errors_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def load_recent(self, days: int = 7) -> List[ErrorRecord]:
        """加载最近 N 天的错误"""
        cutoff = datetime.now() - timedelta(days=days)
        errors = self.load_all()
        
        recent = []
        for e in errors:
            ts = e.get("timestamp", "")
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                if dt.replace(tzinfo=None) >= cutoff:
                    recent.append(e)
            except:
                pass
        
        return recent

    def get_stats(self, days: int = 7) -> ErrorStats:
        """统计错误"""
        errors = self.load_recent(days)
        
        stats = ErrorStats(total_errors=len(errors))
        
        # 按类型统计
        for e in errors:
            et = e.get("error_type", "Unknown")
            stats.by_type[et] = stats.by_type.get(et, 0) + 1
            
            provider = e.get("provider", "unknown")
            stats.by_provider[provider] = stats.by_provider.get(provider, 0) + 1
        
        # 排序取前 5
        stats.top_errors = sorted(
            [{"type": k, "count": v} for k, v in stats.by_type.items()],
            key=lambda x: -x["count"]
        )[:5]
        
        return stats
