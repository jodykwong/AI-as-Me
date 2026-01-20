"""Reflection and rule extraction engine."""

from pathlib import Path
from typing import List, Dict, Optional
import re


class ReflectionEngine:
    """Analyze completed tasks and extract rules."""

    def __init__(self, llm_client, done_dir: Path, rules_file: Path):
        """Initialize reflection engine.

        Args:
            llm_client: LLMClient instance
            done_dir: Directory with completed tasks
            rules_file: Path to rules.md
        """
        self.llm_client = llm_client
        self.done_dir = done_dir
        self.rules_file = rules_file

    def analyze_tasks(self, last_n: Optional[int] = None) -> List[Dict]:
        """Analyze completed tasks.

        Args:
            last_n: Analyze only last N tasks

        Returns:
            List of task analysis dicts
        """
        # Get completed tasks
        task_files = sorted(self.done_dir.glob("*.md"))

        if last_n:
            task_files = task_files[-last_n:]

        analyses = []

        for task_file in task_files:
            # Skip result files
            if "-result" in task_file.name:
                continue

            content = task_file.read_text()

            # Find corresponding result file
            result_file = task_file.parent / f"{task_file.stem}-result.md"
            result_content = ""

            if result_file.exists():
                result_content = result_file.read_text()

            analyses.append(
                {
                    "task_file": task_file.name,
                    "task_content": content,
                    "result_content": result_content,
                }
            )

        return analyses

    def extract_rules(self, analyses: List[Dict]) -> List[Dict]:
        """Extract potential rules from task analyses.

        Args:
            analyses: List of task analysis dicts

        Returns:
            List of extracted rule dicts with content, source, confidence
        """
        if not analyses:
            return []

        # Build prompt for rule extraction
        task_summaries = []
        for i, analysis in enumerate(analyses, 1):
            task_summaries.append(f"Task {i}: {analysis['task_file']}")

        prompt = f"""Analyze these {len(analyses)} completed tasks and extract 1-3 general decision rules or patterns.

Tasks analyzed:
{chr(10).join(task_summaries)}

Extract rules that:
1. Are generalizable (not task-specific)
2. Reflect decision-making patterns
3. Can guide future task execution

Format each rule as:
- [Category] Rule description

Categories: Communication, Technical, Work, Life, AI Development

Return only the rules, one per line."""

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that extracts decision rules from task patterns.",
            },
            {"role": "user", "content": prompt},
        ]

        response = self.llm_client.chat(messages, max_retries=2)

        if not response:
            return []

        # Parse rules
        rules = []
        for line in response.split("\n"):
            line = line.strip()
            if line.startswith("-"):
                # Extract category and rule
                match = re.match(r"-\s*\[([^\]]+)\]\s*(.+)", line)
                if match:
                    category = match.group(1)
                    rule_text = match.group(2)

                    rules.append(
                        {
                            "category": category,
                            "content": rule_text,
                            "source": f"Extracted from {len(analyses)} tasks",
                            "confidence": "medium",  # Simple heuristic
                        }
                    )

        return rules[:3]  # Max 3 rules

    def add_rule(self, rule: Dict):
        """Add a rule to rules.md.

        Args:
            rule: Rule dict with category, content, source
        """
        from datetime import datetime

        # Read existing rules
        if self.rules_file.exists():
            content = self.rules_file.read_text()
        else:
            content = "# Decision Rules\n\n"

        # Find or create category section
        category = rule["category"]
        category_header = f"## {category} Rules"

        if category_header not in content:
            # Add new category
            content += f"\n{category_header}\n"

        # Add rule
        date = datetime.now().strftime("%Y-%m-%d")
        rule_line = f"- {rule['content']} (learned {date}, {rule['source']})\n"

        # Insert after category header
        lines = content.split("\n")
        new_lines = []
        inserted = False

        for i, line in enumerate(lines):
            new_lines.append(line)
            if line == category_header and not inserted:
                # Find next line that's not a comment
                j = i + 1
                while j < len(lines) and lines[j].strip().startswith("<!--"):
                    new_lines.append(lines[j])
                    j += 1
                new_lines.append(rule_line.rstrip())
                inserted = True

        self.rules_file.write_text("\n".join(new_lines))
