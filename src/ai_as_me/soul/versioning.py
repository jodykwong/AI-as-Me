"""Rule Versioning - 规则版本管理."""
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, asdict


@dataclass
class RuleVersion:
    """规则版本."""
    version: int
    timestamp: str
    reason: str
    checksum: str


class RuleVersionManager:
    """规则版本管理器."""
    
    def __init__(self, rules_dir: Path = None):
        self.rules_dir = rules_dir or Path("soul/rules")
        self.versions_dir = self.rules_dir / ".versions"
        self.versions_dir.mkdir(parents=True, exist_ok=True)
    
    def save_version(self, rule_path: Path, reason: str = "update") -> int:
        """保存当前版本，返回版本号."""
        if not rule_path.exists():
            return 0
        
        rule_name = rule_path.stem
        version_dir = self.versions_dir / rule_name
        version_dir.mkdir(parents=True, exist_ok=True)
        
        # 获取下一个版本号
        history = self._load_history(rule_name)
        next_version = len(history) + 1
        
        # 复制当前文件
        content = rule_path.read_text(encoding="utf-8")
        version_file = version_dir / f"v{next_version}.md"
        version_file.write_text(content, encoding="utf-8")
        
        # 更新历史
        history.append(RuleVersion(
            version=next_version,
            timestamp=datetime.now().isoformat(),
            reason=reason,
            checksum=str(hash(content))[:8]
        ))
        self._save_history(rule_name, history)
        
        return next_version
    
    def get_history(self, rule_name: str) -> List[RuleVersion]:
        """获取版本历史."""
        return self._load_history(rule_name)
    
    def get_version(self, rule_name: str, version: int) -> Optional[str]:
        """获取特定版本内容."""
        version_file = self.versions_dir / rule_name / f"v{version}.md"
        if version_file.exists():
            return version_file.read_text(encoding="utf-8")
        return None
    
    def diff(self, rule_name: str, v1: int, v2: int) -> dict:
        """对比两个版本."""
        content1 = self.get_version(rule_name, v1) or ""
        content2 = self.get_version(rule_name, v2) or ""
        
        lines1 = content1.splitlines()
        lines2 = content2.splitlines()
        
        added = [l for l in lines2 if l not in lines1]
        removed = [l for l in lines1 if l not in lines2]
        
        return {"v1": v1, "v2": v2, "added": added, "removed": removed}
    
    def rollback(self, rule_path: Path, to_version: int) -> bool:
        """回滚到指定版本."""
        rule_name = rule_path.stem
        content = self.get_version(rule_name, to_version)
        
        if content is None:
            return False
        
        # 先保存当前版本
        if rule_path.exists():
            self.save_version(rule_path, f"before rollback to v{to_version}")
        
        # 写入回滚内容
        rule_path.write_text(content, encoding="utf-8")
        self.save_version(rule_path, f"rollback to v{to_version}")
        
        return True
    
    def _load_history(self, rule_name: str) -> List[RuleVersion]:
        """加载版本历史."""
        history_file = self.versions_dir / rule_name / "history.json"
        if not history_file.exists():
            return []
        
        data = json.loads(history_file.read_text())
        return [RuleVersion(**v) for v in data]
    
    def _save_history(self, rule_name: str, history: List[RuleVersion]):
        """保存版本历史."""
        history_file = self.versions_dir / rule_name / "history.json"
        history_file.parent.mkdir(parents=True, exist_ok=True)
        history_file.write_text(
            json.dumps([asdict(v) for v in history], indent=2, ensure_ascii=False)
        )
