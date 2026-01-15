"""Inspiration Incubator - 灵感孵化器."""
from datetime import datetime
from typing import List
from .models import Inspiration
from .pool import InspirationPool


class InspirationIncubator:
    """灵感孵化和成熟度管理."""
    
    def __init__(self, pool: InspirationPool):
        self.pool = pool
        
    def calculate_maturity(self, inspiration: Inspiration) -> float:
        """计算灵感成熟度 (0.0-1.0)."""
        now = datetime.now()
        
        # 时间因素 (最大 0.4)
        age_days = (now - inspiration.created_at).days
        time_score = min(age_days / 7, 1.0) * 0.4
        
        # 提及因素 (最大 0.3)
        mention_score = min(inspiration.mentions / 3, 1.0) * 0.3
        
        # 优先级因素 (最大 0.3)
        priority_map = {"high": 1.0, "medium": 0.5, "low": 0.2}
        priority_score = priority_map.get(inspiration.priority, 0.5) * 0.3
        
        return round(time_score + mention_score + priority_score, 2)
    
    def incubate_all(self) -> List[Inspiration]:
        """孵化所有灵感，返回成熟的灵感."""
        mature_list = []
        
        for insp in self.pool.list(status="incubating", limit=1000):
            new_maturity = self.calculate_maturity(insp)
            updates = {"maturity": new_maturity}
            
            if new_maturity >= 0.8:
                updates["status"] = "mature"
                mature_list.append(insp)
            
            self.pool.update(insp.id, updates)
        
        return mature_list
    
    def get_mature(self, threshold: float = 0.8) -> List[Inspiration]:
        """获取成熟的灵感."""
        return [i for i in self.pool.list(status="mature", limit=100) 
                if i.maturity >= threshold]
