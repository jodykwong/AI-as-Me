"""Kanban Task Models - Vibe-Kanban."""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum
import re


class TaskStatus(str, Enum):
    INBOX = "inbox"
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class TaskPriority(str, Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class TaskClarification(BaseModel):
    goal: str = ""
    acceptance_criteria: List[str] = []
    tool: Optional[str] = None
    time_estimate: Optional[str] = None
    context: Optional[str] = None


class Task(BaseModel):
    id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.INBOX
    priority: TaskPriority = TaskPriority.P2
    clarified: bool = False
    clarification: TaskClarification = Field(default_factory=TaskClarification)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    def to_markdown(self) -> str:
        criteria = "\n".join(f"- [ ] {c}" for c in self.clarification.acceptance_criteria) or "- [ ] 待定义"
        
        return f"""---
id: {self.id}
created: {self.created_at.isoformat()}
updated: {self.updated_at.isoformat()}
status: {self.status.value}
priority: {self.priority.value}
clarified: {str(self.clarified).lower()}
---

# {self.title}

## 📝 描述
{self.description}

## 🎯 目标
{self.clarification.goal or "[待澄清]"}

## ✅ 验收标准
{criteria}

## 🔧 工具选择
{self.clarification.tool or "[待配置]"}

## ⏱️ 时间估算
{self.clarification.time_estimate or "[待评估]"}

## 📎 上下文
{self.clarification.context or "[无]"}
"""

    @classmethod
    def from_markdown(cls, content: str) -> "Task":
        fm_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not fm_match:
            raise ValueError("Invalid task format")
        
        fm_text = fm_match.group(1)
        body = content[fm_match.end():]
        
        def get_fm(key: str, default: str = "") -> str:
            m = re.search(rf'^{key}:\s*(.+)$', fm_text, re.MULTILINE)
            return m.group(1).strip() if m else default
        
        def get_section(name: str) -> str:
            pattern = rf'## [^\n]*{name}[^\n]*\n(.*?)(?=\n## |\Z)'
            m = re.search(pattern, body, re.DOTALL)
            text = m.group(1).strip() if m else ""
            return "" if text in ["[待澄清]", "[待配置]", "[待评估]", "[无]"] else text
        
        title_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
        criteria_text = get_section("验收标准")
        criteria = [c for c in re.findall(r'- \[[ x]\] (.+)', criteria_text) if c != "待定义"]
        
        return cls(
            id=get_fm("id"),
            title=title_match.group(1) if title_match else "Untitled",
            description=get_section("描述"),
            status=TaskStatus(get_fm("status", "inbox")),
            priority=TaskPriority(get_fm("priority", "P2")),
            clarified=get_fm("clarified", "false").lower() == "true",
            clarification=TaskClarification(
                goal=get_section("目标"),
                acceptance_criteria=criteria,
                tool=get_section("工具") or None,
                time_estimate=get_section("时间") or None,
                context=get_section("上下文") or None
            ),
            created_at=datetime.fromisoformat(get_fm("created")) if get_fm("created") else datetime.now(),
            updated_at=datetime.fromisoformat(get_fm("updated")) if get_fm("updated") else datetime.now()
        )


class TaskCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=2000)
    priority: TaskPriority = TaskPriority.P2


class TaskClarifyRequest(BaseModel):
    goal: str = Field(..., min_length=1)
    acceptance_criteria: List[str] = Field(default_factory=list)
    tool: Optional[str] = None
    time_estimate: Optional[str] = None
    context: Optional[str] = None


class TaskMoveRequest(BaseModel):
    to_status: TaskStatus
