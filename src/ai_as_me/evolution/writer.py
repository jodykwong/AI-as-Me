"""Soul Writer - Story 1.4"""

from pathlib import Path


class SoulWriter:
    def __init__(self, soul_dir: Path):
        self.learned_dir = soul_dir / "rules" / "learned"
        self.learned_dir.mkdir(parents=True, exist_ok=True)

    def write_rule(self, rule) -> Path:
        """写入规则到 learned/ 目录"""
        filename = f"{rule.category}-{rule.rule_id}.md"
        path = self.learned_dir / filename

        content = rule.to_markdown()
        path.write_text(content)

        return path

    def list_rules(self) -> list[Path]:
        """列出所有学习的规则"""
        return sorted(self.learned_dir.glob("*.md"))

    def count_rules(self) -> int:
        """统计规则数量"""
        return len(self.list_rules())
