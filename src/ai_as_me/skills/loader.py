"""Skill Loader - Story 4.3"""
from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass
class Skill:
    name: str
    triggers: list[dict]
    description: str
    invoke_path: str
    version: str


class SkillLoader:
    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
    
    def load_skill(self, name: str) -> Skill | None:
        """加载指定 Skill"""
        skill_file = self.skills_dir / name / "SKILL.md"
        if not skill_file.exists():
            return None
        
        content = skill_file.read_text()
        
        # 解析 YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                description = parts[2].strip()
                
                return Skill(
                    name=frontmatter['name'],
                    triggers=frontmatter.get('triggers', []),
                    description=description,
                    invoke_path=str(skill_file.parent),
                    version=frontmatter.get('version', '1.0')
                )
        
        return None
    
    def list_skills(self) -> list[str]:
        """列出所有可用 Skills"""
        skills = []
        if self.skills_dir.exists():
            for d in self.skills_dir.iterdir():
                if d.is_dir() and (d / "SKILL.md").exists():
                    skills.append(d.name)
        return skills
    
    def should_invoke(self, skill: Skill, task, capability_gap: bool = False) -> bool:
        """判断是否应该调用 Skill"""
        for trigger in skill.triggers:
            # 任务类型匹配
            if 'task_type' in trigger:
                task_type = getattr(task, 'type', None)
                if task_type == trigger['task_type']:
                    return True
            
            # 能力缺口触发
            if 'capability_gap' in trigger and trigger['capability_gap']:
                if capability_gap:
                    return True
        
        return False
