"""Inspiration Pool - 灵感池管理."""

import json
import fcntl
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from .models import Inspiration


class InspirationPool:
    """灵感池管理器."""

    def __init__(self, pool_dir: Path = None):
        self.pool_dir = pool_dir or Path("soul/inspiration")
        self.pool_file = self.pool_dir / "pool.jsonl"
        self.index_file = self.pool_dir / "index.json"
        self.pool_dir.mkdir(parents=True, exist_ok=True)
        self._cache: List[Inspiration] = []
        self._cache_valid = False

    def add(self, inspiration: Inspiration) -> str:
        """添加灵感，返回 ID."""
        with open(self.pool_file, "a", encoding="utf-8") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(inspiration.to_json() + "\n")
            fcntl.flock(f, fcntl.LOCK_UN)
        self._cache_valid = False
        self._update_index()
        return inspiration.id

    def get(self, id: str) -> Optional[Inspiration]:
        """获取单个灵感."""
        for insp in self._load_all():
            if insp.id == id:
                return insp
        return None

    def list(self, status: str = None, limit: int = 50) -> List[Inspiration]:
        """列出灵感."""
        all_insp = self._load_all()
        if status:
            all_insp = [i for i in all_insp if i.status == status]
        return all_insp[:limit]

    def update(self, id: str, updates: dict) -> bool:
        """更新灵感."""
        all_insp = self._load_all()
        updated = False

        for insp in all_insp:
            if insp.id == id:
                for k, v in updates.items():
                    if hasattr(insp, k):
                        setattr(insp, k, v)
                insp.updated_at = datetime.now()
                updated = True
                break

        if updated:
            self._save_all(all_insp)
            self._update_index()
        return updated

    def archive(self, id: str) -> bool:
        """归档灵感."""
        return self.update(id, {"status": "archived"})

    def _load_all(self) -> List[Inspiration]:
        """加载所有灵感（带缓存）."""
        if self._cache_valid:
            return self._cache

        if not self.pool_file.exists():
            return []

        inspirations = []
        for line in self.pool_file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                inspirations.append(Inspiration.from_dict(json.loads(line)))

        self._cache = inspirations
        self._cache_valid = True
        return inspirations

    def _save_all(self, inspirations: List[Inspiration]):
        """保存所有灵感（带文件锁）."""
        with open(self.pool_file, "w", encoding="utf-8") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            for insp in inspirations:
                f.write(insp.to_json() + "\n")
            fcntl.flock(f, fcntl.LOCK_UN)
        self._cache = inspirations
        self._cache_valid = True

    def _update_index(self):
        """更新索引."""
        all_insp = self._load_all()

        by_status = {}
        by_source = {}
        for insp in all_insp:
            by_status[insp.status] = by_status.get(insp.status, 0) + 1
            by_source[insp.source] = by_source.get(insp.source, 0) + 1

        index = {
            "total": len(all_insp),
            "by_status": by_status,
            "by_source": by_source,
            "last_updated": datetime.now().isoformat(),
        }

        self.index_file.write_text(json.dumps(index, indent=2, ensure_ascii=False))

    def get_stats(self) -> dict:
        """获取统计信息."""
        if self.index_file.exists():
            return json.loads(self.index_file.read_text())
        return {"total": 0, "by_status": {}, "by_source": {}}

    # API 别名
    def get_inspiration(self, id: str) -> Optional[Inspiration]:
        """获取单个灵感（API 别名）."""
        return self.get(id)

    def list_inspirations(
        self, status: str = None, min_maturity: float = None, limit: int = 50
    ) -> List[Inspiration]:
        """列表灵感（API 别名）."""
        inspirations = self.list(status=status, limit=limit)
        if min_maturity is not None:
            inspirations = [i for i in inspirations if i.maturity >= min_maturity]
        return inspirations
