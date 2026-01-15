"""Stats Calculator - 统计计算器."""
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict


class StatsCalculator:
    """进化统计计算器."""
    
    def __init__(self, evolution_log: Path = None, experience_dir: Path = None):
        self.evolution_log = evolution_log or Path("logs/evolution.jsonl")
        self.experience_dir = experience_dir or Path("experience")
        
    def calculate_application_frequency(self, days: int = 7) -> Dict[str, float]:
        """计算规则应用频率（次/天）."""
        if not self.evolution_log.exists():
            return {}
        
        cutoff = datetime.now() - timedelta(days=days)
        rule_counts = defaultdict(int)
        
        for line in self.evolution_log.read_text().splitlines():
            try:
                entry = json.loads(line)
                timestamp = datetime.fromisoformat(entry.get("timestamp", ""))
                
                if timestamp >= cutoff and entry.get("event") == "rule_applied":
                    rule_id = entry.get("rule_id", "unknown")
                    rule_counts[rule_id] += 1
            except:
                continue
        
        # 计算频率（次/天）
        return {rule: count / days for rule, count in rule_counts.items()}
    
    def calculate_effectiveness_score(self, rule_id: str = None) -> Dict[str, float]:
        """计算规则有效性评分（应用后成功率变化）."""
        if not self.evolution_log.exists():
            return {}
        
        # 简化实现：对比应用规则前后的任务成功率
        scores = {}
        
        for line in self.evolution_log.read_text().splitlines():
            try:
                entry = json.loads(line)
                if entry.get("event") == "rule_generated":
                    rid = entry.get("rule_id")
                    if rule_id and rid != rule_id:
                        continue
                    
                    # 模拟有效性评分（实际应从 experience 计算）
                    scores[rid] = entry.get("effectiveness_score", 0.0)
            except:
                continue
        
        return scores
    
    def calculate_pattern_accuracy(self) -> float:
        """计算模式识别准确率（模式→规则转化率）."""
        if not self.evolution_log.exists():
            return 0.0
        
        patterns_identified = 0
        rules_generated = 0
        
        for line in self.evolution_log.read_text().splitlines():
            try:
                entry = json.loads(line)
                if entry.get("event") == "pattern_recognized":
                    patterns_identified += 1
                elif entry.get("event") == "rule_generated":
                    rules_generated += 1
            except:
                continue
        
        if patterns_identified == 0:
            return 0.0
        
        return rules_generated / patterns_identified
    
    def get_detailed_stats(self, days: int = 7) -> dict:
        """获取详细统计."""
        return {
            "application_frequency": self.calculate_application_frequency(days),
            "effectiveness_scores": self.calculate_effectiveness_score(),
            "pattern_accuracy": self.calculate_pattern_accuracy(),
            "time_range_days": days
        }
    
    def get_rule_stats(self, rule_id: str) -> dict:
        """获取单条规则统计."""
        freq = self.calculate_application_frequency()
        effectiveness = self.calculate_effectiveness_score(rule_id)
        
        return {
            "rule_id": rule_id,
            "application_frequency": freq.get(rule_id, 0.0),
            "effectiveness_score": effectiveness.get(rule_id, 0.0),
            "last_applied": self._get_last_applied(rule_id)
        }
    
    def _get_last_applied(self, rule_id: str) -> str:
        """获取规则最后应用时间."""
        if not self.evolution_log.exists():
            return "never"
        
        last_time = None
        for line in self.evolution_log.read_text().splitlines():
            try:
                entry = json.loads(line)
                if entry.get("event") == "rule_applied" and entry.get("rule_id") == rule_id:
                    last_time = entry.get("timestamp")
            except:
                continue
        
        return last_time or "never"
