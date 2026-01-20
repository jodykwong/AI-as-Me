"""Inspiration data model."""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional
import json
import uuid


@dataclass
class Inspiration:
    """灵感数据模型."""

    content: str
    source: str = "manual"  # conversation|task|manual
    source_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    priority: str = "medium"  # low|medium|high
    maturity: float = 0.0
    status: str = "incubating"  # incubating|mature|converted|archived
    mentions: int = 0
    id: str = field(
        default_factory=lambda: f"insp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    )
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    converted_to: Optional[str] = None

    def to_dict(self) -> dict:
        """转换为字典."""
        d = asdict(self)
        d["created_at"] = self.created_at.isoformat()
        d["updated_at"] = self.updated_at.isoformat()
        return d

    def to_json(self) -> str:
        """转换为 JSON 字符串."""
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict) -> "Inspiration":
        """从字典创建."""
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return cls(**data)
