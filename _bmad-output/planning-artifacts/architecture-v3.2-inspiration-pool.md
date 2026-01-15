# AI-as-Me v3.2 Architecture - 灵感池机制

**文档版本**: 1.0  
**创建日期**: 2026-01-15  
**状态**: Draft

---

## 1. 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI Layer                             │
│  ai-as-me inspiration [add|list|show|mature|convert]        │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Inspiration Module                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Capturer │  │   Pool   │  │Incubator │  │Converter │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       │             │             │             │           │
│       └─────────────┴─────────────┴─────────────┘           │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Storage Layer                             │
│  soul/inspiration/pool.jsonl    soul/inspiration/index.json │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 模块设计

### 2.1 Capturer (灵感捕获器)

```python
class InspirationCapturer:
    """从各种来源捕获灵感."""
    
    TRIGGER_PATTERNS = [
        r"以后(可以|应该|要)",
        r"(想法|灵感|idea)",
        r"TODO[:：]",
        r"或许(可以|应该)",
    ]
    
    def capture_from_text(self, text: str, source: str) -> Optional[Inspiration]
    def capture_from_task(self, task_result: dict) -> Optional[Inspiration]
```

### 2.2 Pool (灵感池)

```python
class InspirationPool:
    """灵感池管理."""
    
    def __init__(self, pool_path: Path):
        self.pool_path = pool_path  # soul/inspiration/pool.jsonl
        
    def add(self, inspiration: Inspiration) -> str  # 返回 ID
    def get(self, id: str) -> Optional[Inspiration]
    def list(self, status: str = None, limit: int = 50) -> List[Inspiration]
    def update(self, id: str, updates: dict) -> bool
    def archive(self, id: str) -> bool
```

### 2.3 Incubator (灵感孵化器)

```python
class InspirationIncubator:
    """灵感孵化和成熟度管理."""
    
    def calculate_maturity(self, inspiration: Inspiration) -> float
    def incubate_all(self) -> List[Inspiration]  # 返回成熟的灵感
    def get_mature(self, threshold: float = 0.8) -> List[Inspiration]
```

### 2.4 Converter (灵感转化器)

```python
class InspirationConverter:
    """将灵感转化为规则/任务/技能."""
    
    def __init__(self, evolution_engine, kanban_api):
        self.evolution_engine = evolution_engine
        self.kanban_api = kanban_api
        
    def to_rule(self, inspiration: Inspiration) -> Path  # 返回规则路径
    def to_task(self, inspiration: Inspiration) -> str   # 返回任务 ID
    def to_skill(self, inspiration: Inspiration) -> Path # 返回技能路径
```

---

## 3. 数据模型

### 3.1 Inspiration

```python
@dataclass
class Inspiration:
    id: str                    # insp_YYYYMMDD_HHMMSS_XXX
    content: str               # 灵感内容
    source: str                # conversation|task|manual
    source_id: Optional[str]   # 关联的对话/任务 ID
    tags: List[str]            # 标签
    priority: str              # low|medium|high
    maturity: float            # 0.0-1.0
    status: str                # incubating|mature|converted|archived
    mentions: int              # 被提及次数
    created_at: datetime
    updated_at: datetime
    converted_to: Optional[str] # 转化后的规则/任务 ID
```

### 3.2 存储格式

**pool.jsonl** (JSON Lines):
```json
{"id":"insp_20260115_203000_001","content":"可以添加语音输入支持","source":"conversation","maturity":0.3,"status":"incubating",...}
{"id":"insp_20260115_204500_002","content":"任务失败时自动重试","source":"task","maturity":0.7,"status":"incubating",...}
```

**index.json** (快速索引):
```json
{
  "total": 42,
  "by_status": {"incubating": 30, "mature": 8, "converted": 4},
  "by_source": {"conversation": 25, "task": 12, "manual": 5},
  "last_updated": "2026-01-15T20:30:00"
}
```

---

## 4. 成熟度算法

```python
def calculate_maturity(inspiration: Inspiration) -> float:
    """计算灵感成熟度 (0.0-1.0)."""
    
    # 时间因素 (最大 0.4)
    age_days = (now - inspiration.created_at).days
    time_score = min(age_days / 7, 1.0) * 0.4
    
    # 提及因素 (最大 0.3)
    mention_score = min(inspiration.mentions / 3, 1.0) * 0.3
    
    # 优先级因素 (最大 0.3)
    priority_map = {"high": 1.0, "medium": 0.5, "low": 0.2}
    priority_score = priority_map[inspiration.priority] * 0.3
    
    return time_score + mention_score + priority_score
```

---

## 5. CLI 命令设计

```bash
# 命令组
ai-as-me inspiration [COMMAND]

# 子命令
ai-as-me inspiration add "想法内容" [--tags tag1,tag2] [--priority high]
ai-as-me inspiration list [--status incubating] [--limit 20]
ai-as-me inspiration show <id>
ai-as-me inspiration mature              # 列出成熟灵感
ai-as-me inspiration convert <id> --to rule|task|skill
ai-as-me inspiration archive <id>
ai-as-me inspiration stats               # 统计信息
```

---

## 6. 集成设计

### 6.1 Agent 集成

```python
# agent.py
class Agent:
    def __init__(self):
        self.capturer = InspirationCapturer()
        
    async def process_message(self, message: str):
        # 处理消息...
        
        # 尝试捕获灵感
        inspiration = self.capturer.capture_from_text(message, "conversation")
        if inspiration:
            self.pool.add(inspiration)
```

### 6.2 Evolution Engine 集成

```python
# converter.py
def to_rule(self, inspiration: Inspiration) -> Path:
    # 构造伪经验
    experience = Experience(
        task_id=inspiration.id,
        description=inspiration.content,
        ...
    )
    
    # 调用现有进化流程
    pattern = self.evolution_engine.recognizer.recognize([experience])
    rule = self.evolution_engine.generator.generate(pattern[0])
    return self.evolution_engine.writer.write(rule)
```

---

## 7. 目录结构

```
soul/
├── rules/
│   ├── core/
│   └── learned/
├── inspiration/           # 新增
│   ├── pool.jsonl        # 灵感数据
│   └── index.json        # 索引
└── ...

src/ai_as_me/
├── inspiration/           # 新增模块
│   ├── __init__.py
│   ├── capturer.py
│   ├── pool.py
│   ├── incubator.py
│   └── converter.py
└── ...
```

---

## 8. 测试策略

| 测试类型 | 覆盖范围 |
|----------|----------|
| 单元测试 | Capturer 模式匹配、成熟度计算 |
| 集成测试 | Pool CRUD、Converter 转化流程 |
| E2E 测试 | CLI 命令完整流程 |

---

**下一步**: 创建 v3.2 Epics & Stories
