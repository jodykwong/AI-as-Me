"""Rule Generator - Story 1.3"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class GeneratedRule:
    rule_id: str
    category: str
    content: str
    source_pattern: str
    confidence: float
    created_at: datetime
    metadata: dict

    def to_markdown(self) -> str:
        return f"""---
source: {self.source_pattern}
created: {self.created_at.strftime('%Y-%m-%d')}
confidence: {self.confidence}
applied_count: 0
---

# {self.category} 规则

## 规则内容

{self.content}

## 来源

从模式 {self.source_pattern} 提取。

## 元数据

- 置信度: {self.confidence}
- 创建时间: {self.created_at.isoformat()}
"""


class RuleGenerator:
    def __init__(self, llm_client):
        self.llm = llm_client

    def generate(self, pattern) -> GeneratedRule | None:
        """从模式生成规则"""
        if pattern.confidence < 0.6:
            return None

        prompt = self._build_prompt(pattern)

        try:
            response = self.llm.chat(
                [
                    {
                        "role": "system",
                        "content": "你是规则生成专家，将模式转化为可执行的决策规则。",
                    },
                    {"role": "user", "content": prompt},
                ]
            )

            return self._parse_rule(response, pattern)
        except Exception as e:
            print(f"Rule generation failed: {e}")
            return None

    def _build_prompt(self, pattern) -> str:
        return f"""基于以下模式生成一条决策规则：

模式类别: {pattern.category}
模式描述: {pattern.description}
置信度: {pattern.confidence}

生成规则要求：
1. 明确的触发条件
2. 具体的行动建议
3. 简洁清晰（1-2 句话）

格式：
当 [触发条件] 时，[行动建议]。"""

    def _parse_rule(self, response: str, pattern) -> GeneratedRule:
        rule_id = f"rule-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        return GeneratedRule(
            rule_id=rule_id,
            category=pattern.category,
            content=response.strip(),
            source_pattern=pattern.pattern_id,
            confidence=pattern.confidence,
            created_at=datetime.now(),
            metadata={
                "source_tasks": pattern.source_tasks,
                "frequency": pattern.frequency,
            },
        )
