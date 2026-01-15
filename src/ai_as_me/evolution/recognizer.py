"""Pattern Recognizer - Story 1.2"""
from dataclasses import dataclass
from pathlib import Path
import json
import re


@dataclass
class Pattern:
    pattern_id: str
    description: str
    frequency: int
    source_tasks: list[str]
    confidence: float
    category: str
    
    def to_dict(self):
        return {
            "pattern_id": self.pattern_id,
            "description": self.description,
            "frequency": self.frequency,
            "source_tasks": self.source_tasks,
            "confidence": self.confidence,
            "category": self.category
        }


class PatternRecognizer:
    def __init__(self, llm_client, experience_dir: Path):
        self.llm = llm_client
        self.patterns_dir = experience_dir / "patterns"
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
    
    def recognize(self, experiences: list) -> list[Pattern]:
        """从经验中识别模式"""
        if len(experiences) < 3:
            return []
        
        prompt = self._build_prompt(experiences)
        
        try:
            response = self.llm.chat([
                {"role": "system", "content": "你是模式识别专家，从任务执行历史中提取可复用模式。"},
                {"role": "user", "content": prompt}
            ])
            
            patterns = self._parse_patterns(response, experiences)
            
            # 保存模式
            for p in patterns:
                file_path = self.patterns_dir / f"{p.pattern_id}.json"
                file_path.write_text(json.dumps(p.to_dict(), indent=2))
            
            return patterns
        except Exception as e:
            print(f"Pattern recognition failed: {e}")
            return []
    
    def _build_prompt(self, experiences: list) -> str:
        exp_summaries = []
        for i, exp in enumerate(experiences, 1):
            status = "✓" if exp.success else "✗"
            exp_summaries.append(
                f"{i}. [{status}] {exp.description[:100]} (工具: {exp.tool_used})"
            )
        
        return f"""分析以下 {len(experiences)} 个任务执行记录，识别可复用的模式：

{chr(10).join(exp_summaries)}

请识别 1-2 个模式，每个模式包含：
1. 模式描述（简洁明确）
2. 适用场景
3. 建议的处理方式
4. 置信度（0.0-1.0）

格式：
[类别] 模式描述 | 置信度: X.X
适用场景: ...
建议: ..."""
    
    def _parse_patterns(self, response: str, experiences: list) -> list[Pattern]:
        patterns = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('['):
                match = re.match(r'\[([^\]]+)\]\s*(.+?)\s*\|\s*置信度:\s*([\d.]+)', line)
                if match:
                    category = match.group(1)
                    description = match.group(2)
                    confidence = float(match.group(3))
                    
                    if confidence >= 0.6:
                        pattern_id = f"pattern-{len(patterns)+1}"
                        patterns.append(Pattern(
                            pattern_id=pattern_id,
                            description=description,
                            frequency=len(experiences),
                            source_tasks=[e.task_id for e in experiences],
                            confidence=confidence,
                            category=category
                        ))
        
        return patterns
