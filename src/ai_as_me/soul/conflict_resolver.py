"""Conflict Resolver - 冲突处理器."""

import json
from pathlib import Path
from datetime import datetime


class ConflictResolver:
    """冲突处理器."""

    def __init__(self, log_file: Path = None):
        self.log_file = log_file or Path("logs/rule-conflicts.jsonl")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    async def auto_resolve(self, conflict) -> dict:
        """自动处理冲突：降级 learned rule."""
        resolution = {
            "action": "downgrade_learned",
            "reason": "Core rules 优先",
            "timestamp": datetime.now().isoformat(),
        }

        # 记录日志
        await self.log_conflict(conflict, resolution)

        return resolution

    async def log_conflict(self, conflict, resolution: dict = None):
        """记录冲突到日志."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "conflict_type": conflict.type,
            "core_rule": conflict.core_rule,
            "learned_rule": conflict.learned_rule,
            "reason": conflict.reason,
            "resolution": resolution.get("action") if resolution else "pending",
            "auto_resolved": resolution is not None,
        }

        # 追加到 JSON Lines 文件
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
