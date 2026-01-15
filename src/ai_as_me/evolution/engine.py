"""Evolution Engine - Story 1.5"""
from pathlib import Path
from .collector import ExperienceCollector
from .recognizer import PatternRecognizer
from .generator import RuleGenerator
from .writer import SoulWriter
from .logger import EvolutionLogger


class EvolutionEngine:
    def __init__(self, config: dict):
        self.collector = ExperienceCollector(
            Path(config['experience_dir']),
            config.get('vector_store')
        )
        self.recognizer = PatternRecognizer(
            config['llm_client'],
            Path(config['experience_dir'])
        )
        self.generator = RuleGenerator(config['llm_client'])
        self.writer = SoulWriter(Path(config['soul_dir']))
        self.logger = EvolutionLogger(Path(config.get('log_path', 'logs/evolution.jsonl')))
    
    def evolve(self, task, result: str, success: bool, duration: float = 0) -> dict:
        """完整进化流程"""
        # 1. 收集经验
        exp = self.collector.collect(task, result, success, duration)
        
        # 2. 获取近期经验
        recent = self.collector.get_recent(limit=10)
        
        # 3. 识别模式
        patterns = self.recognizer.recognize(recent)
        
        # 4. 生成规则
        rules = []
        for p in patterns:
            rule = self.generator.generate(p)
            if rule:
                path = self.writer.write_rule(rule)
                rules.append({"rule": rule, "path": path})
        
        # 5. 记录日志
        rule_objs = [r["rule"] for r in rules]
        self.logger.log(exp, patterns, rule_objs)
        
        return {
            "experience": exp,
            "patterns": patterns,
            "rules": rules
        }
