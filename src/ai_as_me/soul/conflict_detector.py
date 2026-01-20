"""Conflict Detector - 规则冲突检测器."""

from pathlib import Path
from typing import List, Dict
import re


class Conflict:
    """冲突对象."""

    def __init__(
        self, conflict_type: str, core_rule: str, learned_rule: str, reason: str
    ):
        self.type = conflict_type
        self.core_rule = core_rule
        self.learned_rule = learned_rule
        self.reason = reason


class ConflictDetector:
    """规则冲突检测器."""

    def __init__(self, soul_dir: Path = None):
        self.soul_dir = soul_dir or Path("soul/rules")
        self.core_dir = self.soul_dir / "core"
        self.learned_dir = self.soul_dir / "learned"

    async def scan(self) -> List[Conflict]:
        """扫描所有规则，返回冲突列表."""
        conflicts = []

        # 加载所有规则
        core_rules = self._load_rules(self.core_dir)
        learned_rules = self._load_rules(self.learned_dir)

        # 检测冲突
        for learned_file, learned_content in learned_rules.items():
            for core_file, core_content in core_rules.items():
                # 检测直接矛盾
                contradiction = self._detect_contradiction(
                    core_content, learned_content, core_file, learned_file
                )
                if contradiction:
                    conflicts.append(contradiction)

                # 检测优先级覆盖
                override = self._detect_priority_override(
                    core_content, learned_content, core_file, learned_file
                )
                if override:
                    conflicts.append(override)

        return conflicts

    def _load_rules(self, directory: Path) -> Dict[str, str]:
        """加载目录下所有规则文件."""
        rules = {}
        if not directory.exists():
            return rules

        for rule_file in directory.rglob("*.md"):
            try:
                rules[str(rule_file)] = rule_file.read_text()
            except Exception:
                pass  # 跳过无法读取的文件

        return rules

    def _detect_contradiction(
        self, core_content: str, learned_content: str, core_file: str, learned_file: str
    ) -> Conflict | None:
        """检测直接矛盾."""
        # 关键词匹配：禁止 vs 使用
        forbidden_patterns = [
            (r"禁止[^\n]*?(\S+)", r"使用[^\n]*?\1"),
            (r"不要[^\n]*?(\S+)", r"应该[^\n]*?\1"),
            (r"避免[^\n]*?(\S+)", r"优先[^\n]*?\1"),
        ]

        for forbid_pattern, use_pattern in forbidden_patterns:
            forbid_match = re.search(forbid_pattern, core_content)
            if forbid_match:
                target = forbid_match.group(1)
                # 直接检查 learned 是否包含相同目标词
                if target in learned_content and re.search(
                    r"使用|应该|优先", learned_content
                ):
                    return Conflict(
                        conflict_type="contradiction",
                        core_rule=core_file,
                        learned_rule=learned_file,
                        reason=f"Core 禁止 '{target}'，但 Learned 建议使用",
                    )

        return None

    def _detect_priority_override(
        self, core_content: str, learned_content: str, core_file: str, learned_file: str
    ) -> Conflict | None:
        """检测优先级覆盖."""
        # 检测关键规则标记
        if "# 关键规则" in core_content or "# CRITICAL" in core_content:
            # 简单检测：learned 是否试图修改相同主题
            core_topics = set(re.findall(r"##\s+(.+)", core_content))
            learned_topics = set(re.findall(r"##\s+(.+)", learned_content))

            overlap = core_topics & learned_topics
            if overlap:
                return Conflict(
                    conflict_type="priority_override",
                    core_rule=core_file,
                    learned_rule=learned_file,
                    reason=f"Learned 试图覆盖关键规则主题: {', '.join(overlap)}",
                )

        return None
