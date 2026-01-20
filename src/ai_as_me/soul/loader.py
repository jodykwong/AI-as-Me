"""Soul file loader."""

from pathlib import Path
from typing import Dict, Optional


def load_soul_context(soul_dir: Path) -> Optional[str]:
    """快速加载Soul上下文的便捷函数.

    Args:
        soul_dir: Soul目录路径

    Returns:
        合并的Soul上下文字符串，如果没有文件则返回None
    """
    loader = SoulLoader(soul_dir)
    return loader.load_all()


class SoulLoader:
    """Load and manage soul files."""

    def __init__(self, soul_dir: Path):
        self.soul_dir = soul_dir
        self.profile_file = soul_dir / "profile.md"
        self.rules_file = soul_dir / "rules.md"  # 兼容旧版
        self.mission_file = soul_dir / "mission.md"

        # v3.0 新增
        self.rules_dir = soul_dir / "rules"
        self.core_rules_dir = self.rules_dir / "core"
        self.learned_rules_dir = self.rules_dir / "learned"

    def initialize(self):
        """Initialize soul directory with template files."""
        self.soul_dir.mkdir(exist_ok=True)

        # Create profile.md template
        if not self.profile_file.exists():
            self.profile_file.write_text(
                """# Personal Profile

## Background
<!-- Your professional background, education, experience -->

## Expertise
<!-- Your areas of expertise and skills -->

## Communication Style
<!-- How you prefer to communicate (formal/casual, concise/detailed, etc.) -->

## Language Preference
<!-- Preferred language(s) for communication -->

## Personality Traits
<!-- Key personality traits that should be reflected -->
"""
            )
            self.profile_file.chmod(0o600)

        # Create rules.md template
        if not self.rules_file.exists():
            self.rules_file.write_text(
                """# Decision Rules

## Communication Rules
<!-- Rules about how to communicate -->
- Example: Always be concise and direct

## Technical Rules
<!-- Rules about technical decisions -->
- Example: Prefer Python for scripting tasks

## Work Rules
<!-- Rules about work habits and preferences -->
- Example: Focus on one task at a time

## Life Rules
<!-- Personal life rules and values -->
- Example: Prioritize health and family
"""
            )
            self.rules_file.chmod(0o600)

        # Create mission.md template
        if not self.mission_file.exists():
            self.mission_file.write_text(
                """# Mission & Goals

## Core Mission
<!-- Your overarching mission or purpose -->

## Short-term Goals (3-6 months)
<!-- Immediate goals and objectives -->
- 

## Long-term Goals (1-3 years)
<!-- Future aspirations and targets -->
- 

## Values
<!-- Core values that guide decisions -->
- 
"""
            )
            self.mission_file.chmod(0o600)

    def check_status(self) -> Dict[str, bool]:
        """Check which soul files exist.

        Returns:
            Dict with existence status for each file
        """
        return {
            "profile": self.profile_file.exists(),
            "rules": self.rules_file.exists(),
            "mission": self.mission_file.exists(),
        }

    def load_all(self) -> Optional[str]:
        """Load all soul files into a single context string.

        Returns:
            Combined soul context or None if files don't exist
        """
        # 自动迁移检查
        if self.rules_file.exists() and not self.rules_dir.exists():
            from ai_as_me.soul.migrator import SoulMigrator

            migrator = SoulMigrator(self.soul_dir)
            migrator.migrate()

        parts = []

        if self.profile_file.exists():
            parts.append(f"# Profile\n{self.profile_file.read_text()}")

        # 加载规则（新结构优先）
        rules_content = self.load_all_rules()
        if rules_content:
            parts.append(f"# Rules\n{rules_content}")

        if self.mission_file.exists():
            parts.append(f"# Mission\n{self.mission_file.read_text()}")

        return "\n\n".join(parts) if parts else None

    def load_all_rules(self) -> str:
        """加载所有规则（core + learned）"""
        rules = []

        # 加载 core 规则
        if self.core_rules_dir.exists():
            for f in sorted(self.core_rules_dir.glob("*.md")):
                rules.append(f"## Core Rule: {f.stem}\n{f.read_text()}")

        # 加载 learned 规则
        if self.learned_rules_dir.exists():
            for f in sorted(self.learned_rules_dir.glob("*.md")):
                rules.append(f"## Learned Rule: {f.stem}\n{f.read_text()}")

        # 兼容旧版 rules.md
        if not rules and self.rules_file.exists():
            rules.append(self.rules_file.read_text())

        return "\n\n".join(rules) if rules else "# No rules defined"

    def list_rules(self) -> Dict[str, list]:
        """列表所有规则（API 用）"""
        from datetime import datetime

        core_rules = []
        learned_rules = []

        # Core 规则
        if self.core_rules_dir.exists():
            for f in sorted(self.core_rules_dir.glob("*.md")):
                stat = f.stat()
                core_rules.append(
                    {
                        "id": f.stem,
                        "category": "core",
                        "content": f.read_text()[:200] + "...",
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    }
                )

        # Learned 规则
        if self.learned_rules_dir.exists():
            for f in sorted(self.learned_rules_dir.glob("*.md")):
                stat = f.stat()
                content = f.read_text()
                # 尝试解析 confidence
                confidence = 0.0
                for line in content.split("\n"):
                    if "confidence:" in line.lower():
                        try:
                            confidence = float(line.split(":")[-1].strip())
                        except:
                            pass

                learned_rules.append(
                    {
                        "id": f.stem,
                        "category": "learned",
                        "content": content[:200] + "...",
                        "confidence": confidence,
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    }
                )

        return {"core": core_rules, "learned": learned_rules}
