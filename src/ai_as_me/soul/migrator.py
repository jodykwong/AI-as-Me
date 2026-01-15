"""Soul Migrator - Story 2.1"""
from pathlib import Path
import shutil


class SoulMigrator:
    def __init__(self, soul_dir: Path):
        self.soul_dir = soul_dir
        self.old_rules = soul_dir / "rules.md"
        self.rules_dir = soul_dir / "rules"
        self.core_dir = self.rules_dir / "core"
        self.learned_dir = self.rules_dir / "learned"
    
    def migrate(self):
        """迁移 Soul 目录到 v3.0 结构"""
        # 创建目录
        self.core_dir.mkdir(parents=True, exist_ok=True)
        self.learned_dir.mkdir(parents=True, exist_ok=True)
        
        # 迁移 rules.md
        if self.old_rules.exists():
            # 备份
            backup = self.soul_dir / "rules.md.backup"
            if not backup.exists():
                shutil.copy(self.old_rules, backup)
            
            # 迁移到 core/base.md
            new_path = self.core_dir / "base.md"
            shutil.copy(self.old_rules, new_path)
            self.old_rules.unlink()  # 删除旧文件
            
            print(f"✓ 迁移完成: rules.md → rules/core/base.md")
            print(f"✓ 备份保存: rules.md.backup")
        else:
            print("ℹ️  rules.md 不存在或已迁移")
        
        # 创建 .gitkeep
        (self.learned_dir / ".gitkeep").touch()
        
        return True
