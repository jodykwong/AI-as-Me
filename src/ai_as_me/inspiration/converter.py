"""Inspiration Converter - 灵感转化器."""
from pathlib import Path
from datetime import datetime
from .models import Inspiration
from .pool import InspirationPool


class InspirationConverter:
    """将灵感转化为规则/任务."""
    
    def __init__(self, pool: InspirationPool):
        self.pool = pool
        self.rules_dir = Path("soul/rules/learned")
        self.rules_dir.mkdir(parents=True, exist_ok=True)
        
    def to_rule(self, inspiration: Inspiration) -> Path:
        """将灵感转化为规则."""
        rule_name = f"insp_{inspiration.id.split('_')[-1]}"
        rule_path = self.rules_dir / f"{rule_name}.md"
        
        rule_content = f"""# {rule_name}

## 来源
- 灵感 ID: {inspiration.id}
- 创建时间: {inspiration.created_at.isoformat()}
- 成熟度: {inspiration.maturity}

## 规则内容
{inspiration.content}

## 标签
{', '.join(inspiration.tags)}

---
*由灵感池自动转化于 {datetime.now().isoformat()}*
"""
        try:
            rule_path.write_text(rule_content, encoding="utf-8")
        except IOError as e:
            raise RuntimeError(f"写入规则文件失败: {e}")
        
        # 更新灵感状态
        self.pool.update(inspiration.id, {
            "status": "converted",
            "converted_to": str(rule_path)
        })
        
        return rule_path
    
    def to_task(self, inspiration: Inspiration) -> str:
        """将灵感转化为任务（返回任务描述）."""
        task_desc = f"[灵感转化] {inspiration.content}"
        
        self.pool.update(inspiration.id, {
            "status": "converted",
            "converted_to": f"task:{task_desc[:50]}"
        })
        
        return task_desc
