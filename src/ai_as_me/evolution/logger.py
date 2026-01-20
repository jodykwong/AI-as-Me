"""Evolution Logger - Story 5.1"""

from pathlib import Path
import json
from datetime import datetime, timedelta


class EvolutionLogger:
    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, exp, patterns: list, rules: list):
        """记录进化事件"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": exp.task_id,
            "experience_recorded": True,
            "patterns_found": len(patterns),
            "rules_generated": len(rules),
            "rule_ids": [r.rule_id for r in rules] if rules else [],
            "rule_categories": [r.category for r in rules] if rules else [],
        }

        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def get_stats(self, days: int = 7) -> dict:
        """获取最近 N 天的统计"""
        cutoff = datetime.now() - timedelta(days=days)

        total_rules = 0
        total_patterns = 0
        total_experiences = 0

        if not self.log_path.exists():
            return {
                "total_rules": 0,
                "total_patterns": 0,
                "total_experiences": 0,
                "days": days,
            }

        with open(self.log_path) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    entry_time = datetime.fromisoformat(entry["timestamp"])
                    if entry_time >= cutoff:
                        total_rules += entry.get("rules_generated", 0)
                        total_patterns += entry.get("patterns_found", 0)
                        total_experiences += 1
                except Exception:
                    continue

        return {
            "total_rules": total_rules,
            "total_patterns": total_patterns,
            "total_experiences": total_experiences,
            "days": days,
        }

    def get_recent_events(self, limit: int = 10) -> list[dict]:
        """获取最近的进化事件"""
        events = []

        if not self.log_path.exists():
            return events

        with open(self.log_path) as f:
            lines = f.readlines()

        for line in reversed(lines[-limit:]):
            try:
                events.append(json.loads(line))
            except Exception:
                continue

        return events
