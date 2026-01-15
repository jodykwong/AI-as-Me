---
stepsCompleted: ['step-01-init', 'step-02-context', 'step-03-decisions', 'step-04-components', 'step-05-migration']
status: complete
inputDocuments:
  - 'prd-v3.0.md'
  - 'product-brief-AI-as-Me-2026-01-15.md'
  - '_bmad-output/project-context.md'
  - 'AI-as-Me_Project_Status_Report.md'
workflowType: 'architecture'
project_name: 'AI-as-Me'
user_name: 'Jody'
date: '2026-01-15'
version: 'v3.0'
---

# Architecture Decision Document - AI-as-Me v3.0

**Author:** Jody  
**Date:** 2026-01-15  
**Version:** v3.0  
**Status:** In Progress

---

## Step 2: 项目上下文分析

### 2.1 现有架构评估

**v2.3 核心组件：**

| 组件 | 文件 | 状态 | v3.0 影响 |
|------|------|------|-----------|
| Agent 主循环 | `core/agent.py` | ✅ 稳定 | 需扩展进化触发 |
| Soul 加载器 | `soul/loader.py` | ✅ 稳定 | 需支持 learned/ |
| 反思引擎 | `reflect/extractor.py` | ⚠️ 基础 | 需重构为进化引擎 |
| RAG 检索 | `rag/retriever.py` | ✅ 稳定 | 可复用 |
| 技能匹配 | `orchestrator/skill_matcher.py` | ✅ 稳定 | 需集成 Skills |
| Kanban API | `kanban/api.py` | ✅ 稳定 | 无需修改 |

### 2.2 关键发现

**1. 反思引擎已存在但功能有限：**
```python
# reflect/extractor.py 现有能力：
- analyze_tasks(): 分析已完成任务
- extract_rules(): 从任务中提取规则
- add_rule(): 写入 rules.md
```
**问题：** 只写入单一 `rules.md`，无 `learned/` 目录支持

**2. Soul 加载器只读：**
```python
# soul/loader.py 现有能力：
- load_all(): 加载 profile/rules/mission
- check_status(): 检查文件状态
```
**问题：** 无写入能力，无 `learned/` 目录支持

**3. Agent 主循环有反思调度：**
```python
# core/agent.py 现有能力：
- _should_reflect(): 检查是否该反思
- _run_reflection(): 执行反思
```
**问题：** 反思只在空闲时触发，非每任务触发

**4. RAG 已有经验存储：**
```python
# rag/retriever.py 现有能力：
- TaskExperience 数据模型
- VectorStore 向量存储
- ExperienceRetriever 检索器
```
**可复用：** 作为 experience/ 的底层存储

### 2.3 架构差距分析

| v3.0 需求 | 现有能力 | 差距 |
|-----------|----------|------|
| soul/rules/learned/ | rules.md 单文件 | 需新增目录结构 |
| 进化闭环 | 反思引擎（基础） | 需重构为完整闭环 |
| experience/ 目录 | RAG VectorStore | 需文件系统映射 |
| Skills 架构 | skill_matcher.py | 需新增 SKILL.md 支持 |
| OpenCode 集成 | 无 | 需新增 .opencode/ |
| 进化日志 | 无 | 需新增 |

### 2.4 技术债务评估

| 债务 | 严重程度 | v3.0 处理 |
|------|----------|-----------|
| 反思引擎耦合 rules.md | 中 | 重构 |
| Soul 加载器只读 | 高 | 扩展 |
| 无进化日志 | 高 | 新增 |
| Skills 调用逻辑不清 | 中 | 明确 |


---

## Step 3: 架构决策

### 3.1 核心架构方案

```
┌─────────────────────────────────────────────────────────────────┐
│                        AI-as-Me v3.0                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │   Kanban    │───▶│    Agent    │───▶│  Executor   │        │
│  │   System    │    │  Main Loop  │    │   (LLM)     │        │
│  └─────────────┘    └──────┬──────┘    └──────┬──────┘        │
│                            │                   │                │
│                            ▼                   ▼                │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                   Evolution Engine (新增)                │  │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐           │  │
│  │  │ Experience│─▶│  Pattern  │─▶│   Rule    │           │  │
│  │  │ Collector │  │ Recognizer│  │ Generator │           │  │
│  │  └───────────┘  └───────────┘  └─────┬─────┘           │  │
│  └──────────────────────────────────────┼──────────────────┘  │
│                                         ▼                      │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                      Soul System                         │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────────────────────┐ │  │
│  │  │ profile │  │ mission │  │        rules/           │ │  │
│  │  └─────────┘  └─────────┘  │  ├── core/              │ │  │
│  │                            │  └── learned/ (新增)    │ │  │
│  │                            └─────────────────────────┘ │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │   Skills    │    │ Experience  │    │  Evolution  │        │
│  │   (新增)    │    │   (新增)    │    │    Log      │        │
│  └─────────────┘    └─────────────┘    └─────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 目录结构变更

```
AI-as-Me/
├── soul/
│   ├── profile.md
│   ├── mission.md
│   └── rules/                    # 重构：目录化
│       ├── core/                 # 人类定义的核心规则
│       │   └── base.md
│       └── learned/              # 🆕 AI 自创规则
│           └── .gitkeep
├── experience/                   # 🆕 经验存储
│   ├── successes/
│   ├── failures/
│   └── patterns/
├── skills/                       # 🆕 技能定义
│   └── bmad/
│       └── SKILL.md
├── logs/
│   └── evolution.jsonl           # 🆕 进化日志
├── .opencode/                    # 🆕 OpenCode 配置
│   ├── config.yaml
│   └── agents/
│       └── default.md
└── src/ai_as_me/
    ├── evolution/                # 🆕 进化引擎
    │   ├── __init__.py
    │   ├── engine.py
    │   ├── collector.py
    │   ├── recognizer.py
    │   └── generator.py
    └── soul/
        └── loader.py             # 扩展：支持 learned/
```

### 3.3 关键架构决策

#### ADR-1: 进化闭环触发时机

**决策：** 每个任务完成后立即触发进化流程

**理由：**
- 确保 100% 进化闭环完整率
- 经验新鲜时更容易识别模式
- 符合"复利工程"理念

**实现：**
```python
# core/agent.py 修改
def _process_task(self, task_path):
    # ... 执行任务 ...
    if success:
        self._trigger_evolution(task_path, result)  # 新增
```

#### ADR-2: 规则存储格式

**决策：** 每条规则一个 Markdown 文件

**理由：**
- 便于版本控制和追溯
- 支持规则独立管理
- 与 Soul 系统一致

**格式：**
```markdown
# soul/rules/learned/{category}-{timestamp}.md
---
source: task-xxx
created: 2026-01-15
confidence: 0.8
applied_count: 0
---

## 规则内容
当遇到 X 情况时，优先使用 Y 方法。

## 来源
从任务 task-xxx 的成功执行中提取。
```

#### ADR-3: Experience 存储策略

**决策：** 文件系统 + 向量索引双存储

**理由：**
- 文件系统：可读性、可追溯
- 向量索引：快速检索（复用 RAG）

**实现：**
```
experience/successes/task-xxx.json  # 原始数据
rag/vectorstore/                    # 向量索引（已有）
```

#### ADR-4: Skills 调用机制

**决策：** 基于 SKILL.md 的声明式调用

**理由：**
- 与 OpenCode/Claude Code 兼容
- 易于扩展新 Skills
- 触发条件明确

**格式：**
```markdown
# skills/bmad/SKILL.md
---
name: bmad
trigger: 
  - task_type: architecture
  - task_type: planning
  - capability_gap: true
---

## 能力描述
BMad Method 提供完整的软件开发方法论支持。

## 调用方式
加载 _bmad/ 目录下的相关工作流。
```

### 3.4 组件交互流程

```
任务完成
    │
    ▼
┌─────────────────┐
│ ExperienceCollector │  记录到 experience/
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ PatternRecognizer │  识别模式
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  RuleGenerator  │  生成规则
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  SoulWriter     │  写入 soul/rules/learned/
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ EvolutionLogger │  记录到 logs/evolution.jsonl
└─────────────────┘
```

### 3.5 技术选型

| 组件 | 技术 | 理由 |
|------|------|------|
| 进化引擎 | Python 模块 | 与现有代码一致 |
| 规则存储 | Markdown 文件 | 可读性、Git 友好 |
| 经验存储 | JSON + ChromaDB | 复用现有 RAG |
| 进化日志 | JSON Lines | 易于追加和查询 |
| Skills 定义 | Markdown + YAML | 声明式、易扩展 |


---

## Step 4: 组件详细设计

### 4.1 Evolution Engine

#### 4.1.1 ExperienceCollector

```python
# src/ai_as_me/evolution/collector.py

@dataclass
class Experience:
    task_id: str
    description: str
    tool_used: str
    result: str
    success: bool
    duration: float
    timestamp: datetime

class ExperienceCollector:
    def __init__(self, experience_dir: Path, vector_store: VectorStore):
        self.experience_dir = experience_dir
        self.vector_store = vector_store
    
    def collect(self, task: Task, result: str, success: bool) -> Experience:
        """任务完成后收集经验"""
        exp = Experience(...)
        self._save_to_file(exp)      # 文件存储
        self._index_to_vector(exp)   # 向量索引
        return exp
```

#### 4.1.2 PatternRecognizer

```python
# src/ai_as_me/evolution/recognizer.py

@dataclass
class Pattern:
    pattern_id: str
    description: str
    frequency: int
    source_tasks: list[str]
    confidence: float

class PatternRecognizer:
    def __init__(self, llm_client, experience_dir: Path):
        self.llm = llm_client
        self.experience_dir = experience_dir
    
    def recognize(self, recent_experiences: list[Experience]) -> list[Pattern]:
        """从近期经验中识别模式"""
        # 使用 LLM 分析经验，提取可复用模式
        prompt = self._build_prompt(recent_experiences)
        return self._parse_patterns(self.llm.chat(prompt))
```

#### 4.1.3 RuleGenerator

```python
# src/ai_as_me/evolution/generator.py

@dataclass
class GeneratedRule:
    rule_id: str
    category: str
    content: str
    source_pattern: str
    confidence: float
    metadata: dict

class RuleGenerator:
    def __init__(self, llm_client):
        self.llm = llm_client
    
    def generate(self, pattern: Pattern) -> GeneratedRule | None:
        """从模式生成规则"""
        if pattern.confidence < 0.6:
            return None  # 置信度不足，不生成
        
        prompt = self._build_prompt(pattern)
        return self._parse_rule(self.llm.chat(prompt))
```

#### 4.1.4 SoulWriter

```python
# src/ai_as_me/evolution/writer.py

class SoulWriter:
    def __init__(self, soul_dir: Path):
        self.learned_dir = soul_dir / "rules" / "learned"
        self.learned_dir.mkdir(parents=True, exist_ok=True)
    
    def write_rule(self, rule: GeneratedRule) -> Path:
        """写入规则到 learned/ 目录"""
        filename = f"{rule.category}-{rule.rule_id}.md"
        path = self.learned_dir / filename
        path.write_text(self._format_rule(rule))
        return path
```

#### 4.1.5 EvolutionEngine (主入口)

```python
# src/ai_as_me/evolution/engine.py

class EvolutionEngine:
    def __init__(self, config: dict):
        self.collector = ExperienceCollector(...)
        self.recognizer = PatternRecognizer(...)
        self.generator = RuleGenerator(...)
        self.writer = SoulWriter(...)
        self.logger = EvolutionLogger(...)
    
    def evolve(self, task: Task, result: str, success: bool) -> dict:
        """完整进化流程"""
        # 1. 收集经验
        exp = self.collector.collect(task, result, success)
        
        # 2. 获取近期经验
        recent = self.collector.get_recent(limit=10)
        
        # 3. 识别模式
        patterns = self.recognizer.recognize(recent)
        
        # 4. 生成规则
        rules = []
        for p in patterns:
            rule = self.generator.generate(p)
            if rule:
                self.writer.write_rule(rule)
                rules.append(rule)
        
        # 5. 记录日志
        self.logger.log(exp, patterns, rules)
        
        return {"experience": exp, "patterns": patterns, "rules": rules}
```

### 4.2 Soul System 扩展

```python
# src/ai_as_me/soul/loader.py 扩展

class SoulLoader:
    def __init__(self, soul_dir: Path):
        # ... 现有代码 ...
        self.rules_dir = soul_dir / "rules"
        self.core_rules_dir = self.rules_dir / "core"
        self.learned_rules_dir = self.rules_dir / "learned"
    
    def load_all_rules(self) -> str:
        """加载所有规则（core + learned）"""
        rules = []
        
        # 加载 core 规则
        for f in self.core_rules_dir.glob("*.md"):
            rules.append(f"## Core: {f.stem}\n{f.read_text()}")
        
        # 加载 learned 规则
        for f in self.learned_rules_dir.glob("*.md"):
            rules.append(f"## Learned: {f.stem}\n{f.read_text()}")
        
        return "\n\n".join(rules)
    
    def migrate_rules(self):
        """迁移旧 rules.md 到新结构"""
        old_rules = self.soul_dir / "rules.md"
        if old_rules.exists():
            self.core_rules_dir.mkdir(parents=True, exist_ok=True)
            (self.core_rules_dir / "base.md").write_text(old_rules.read_text())
```

### 4.3 Skills 架构

```python
# src/ai_as_me/skills/loader.py

@dataclass
class Skill:
    name: str
    triggers: list[dict]
    description: str
    invoke_path: str

class SkillLoader:
    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
    
    def load_skill(self, name: str) -> Skill | None:
        """加载指定 Skill"""
        skill_file = self.skills_dir / name / "SKILL.md"
        if not skill_file.exists():
            return None
        return self._parse_skill(skill_file)
    
    def should_invoke(self, skill: Skill, task: Task) -> bool:
        """判断是否应该调用 Skill"""
        for trigger in skill.triggers:
            if self._match_trigger(trigger, task):
                return True
        return False
```

### 4.4 Evolution Logger

```python
# src/ai_as_me/evolution/logger.py

class EvolutionLogger:
    def __init__(self, log_path: Path):
        self.log_path = log_path
    
    def log(self, exp: Experience, patterns: list, rules: list):
        """记录进化事件"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": exp.task_id,
            "experience_recorded": True,
            "patterns_found": len(patterns),
            "rules_generated": len(rules),
            "rule_ids": [r.rule_id for r in rules]
        }
        
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
```

### 4.5 Agent 集成点

```python
# src/ai_as_me/core/agent.py 修改

class Agent:
    def __init__(self, ...):
        # ... 现有代码 ...
        self.evolution_engine = EvolutionEngine(config)
    
    def _process_task(self, task_path: Path):
        # ... 现有执行逻辑 ...
        
        if success:
            # 🆕 触发进化
            evolution_result = self.evolution_engine.evolve(
                task, result, success=True
            )
            if evolution_result["rules"]:
                print(f"  🧬 进化: 生成 {len(evolution_result['rules'])} 条新规则")
```

### 4.6 OpenCode 配置

```yaml
# .opencode/config.yaml
version: 1
project:
  name: AI-as-Me
  type: python

agents:
  default:
    system_prompt: |
      你是 AI-as-Me，一个能自我进化的 AI 代理。
      
      加载以下 Soul 文件：
      - soul/profile.md
      - soul/mission.md
      - soul/rules/core/*.md
      - soul/rules/learned/*.md

commands:
  soul-check:
    description: 检查 Soul 状态
    script: python -m ai_as_me.cli soul status
  
  evolve:
    description: 手动触发进化反思
    script: python -m ai_as_me.cli evolve --force
```


---

## Step 5: 迁移策略

### 5.1 Soul 目录迁移

```bash
# 迁移脚本逻辑
soul/rules.md → soul/rules/core/base.md
soul/rules/learned/ → 新建（空）
```

### 5.2 兼容性保证

- 旧 `rules.md` 保留为备份
- `SoulLoader.load_all()` 兼容新旧结构
- 首次运行自动迁移

---

## 总结

### 架构完成状态

| 步骤 | 状态 |
|------|------|
| Step 1: 初始化 | ✅ |
| Step 2: 上下文分析 | ✅ |
| Step 3: 架构决策 | ✅ |
| Step 4: 组件设计 | ✅ |
| Step 5: 迁移策略 | ✅ |

### 实现优先级

| 优先级 | 组件 | 预估工作量 |
|--------|------|-----------|
| P0 | Evolution Engine | 3-4 天 |
| P0 | Soul rules/learned/ | 1 天 |
| P1 | Experience 目录 | 1 天 |
| P1 | Skills 架构 | 2 天 |
| P1 | OpenCode 配置 | 0.5 天 |
| P1 | 进化日志 | 0.5 天 |

**总预估：8-9 天**

---

**文档状态：** 完成  
**下一步：** 生成 Epics & Stories
