---
version: v3.0
status: complete
date: 2026-01-15
source: architecture-v3.0.md, prd-v3.0.md
---

# Epics & Stories - AI-as-Me v3.0

## Epic 1: 进化引擎核心 (P0)

**目标：** 实现完整的 experience → pattern → rule 进化闭环

### Story 1.1: Experience Collector
**优先级：** P0  
**预估：** 4h  
**依赖：** 无

**任务分解：**
1. 定义 `Experience` 数据类（0.5h）
2. 实现 `collect()` 方法（2h）
3. 实现 `get_recent()` 方法（1h）
4. 单元测试（0.5h）

**验收标准：**
- [ ] `Experience` 数据类定义
- [ ] 任务完成后自动收集经验
- [ ] 经验保存到 `experience/successes/` 或 `experience/failures/`
- [ ] 经验索引到向量存储（复用 RAG）
- [ ] 测试覆盖率 >80%

**实现代码：**
```python
# src/ai_as_me/evolution/collector.py
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json

@dataclass
class Experience:
    task_id: str
    description: str
    tool_used: str
    result: str
    success: bool
    duration: float
    timestamp: datetime
    
    def to_dict(self):
        d = asdict(self)
        d['timestamp'] = self.timestamp.isoformat()
        return d

class ExperienceCollector:
    def __init__(self, experience_dir: Path, vector_store):
        self.experience_dir = experience_dir
        self.vector_store = vector_store
        self.successes_dir = experience_dir / "successes"
        self.failures_dir = experience_dir / "failures"
        self.successes_dir.mkdir(parents=True, exist_ok=True)
        self.failures_dir.mkdir(parents=True, exist_ok=True)
    
    def collect(self, task, result: str, success: bool, duration: float = 0) -> Experience:
        exp = Experience(
            task_id=task.id,
            description=task.description,
            tool_used=getattr(task, 'tool', 'unknown'),
            result=result[:500],  # 截断
            success=success,
            duration=duration,
            timestamp=datetime.now()
        )
        
        # 保存到文件
        target_dir = self.successes_dir if success else self.failures_dir
        file_path = target_dir / f"{exp.task_id}.json"
        file_path.write_text(json.dumps(exp.to_dict(), indent=2))
        
        # 索引到向量存储
        from ai_as_me.rag.retriever import TaskExperience
        rag_exp = TaskExperience(
            task_id=exp.task_id,
            description=exp.description,
            tool_used=exp.tool_used,
            result_summary=exp.result,
            success=exp.success,
            user_feedback=None,
            created_at=exp.timestamp
        )
        self.vector_store.add(rag_exp)
        
        return exp
    
    def get_recent(self, limit: int = 10) -> list[Experience]:
        all_files = sorted(
            list(self.successes_dir.glob("*.json")) + 
            list(self.failures_dir.glob("*.json")),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        experiences = []
        for f in all_files[:limit]:
            data = json.loads(f.read_text())
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
            experiences.append(Experience(**data))
        
        return experiences
```

**测试用例：**
```python
# tests/unit/test_experience_collector.py
def test_collect_success():
    collector = ExperienceCollector(tmp_path, mock_vector_store)
    exp = collector.collect(task, "result", success=True)
    assert exp.success
    assert (tmp_path / "successes" / f"{task.id}.json").exists()

def test_get_recent():
    experiences = collector.get_recent(limit=5)
    assert len(experiences) <= 5
```

---

### Story 1.2: Pattern Recognizer
**优先级：** P0  
**预估：** 6h  
**依赖：** Story 1.1

**任务分解：**
1. 定义 `Pattern` 数据类（0.5h）
2. 实现 LLM prompt 构建（1h）
3. 实现模式识别逻辑（3h）
4. 实现置信度评估（1h）
5. 单元测试（0.5h）

**验收标准：**
- [ ] `Pattern` 数据类定义
- [ ] 从近期经验中识别模式（LLM 辅助）
- [ ] 模式置信度评估 >0.6
- [ ] 模式保存到 `experience/patterns/`
- [ ] 测试覆盖率 >80%

**实现代码：**
```python
# src/ai_as_me/evolution/recognizer.py
from dataclasses import dataclass
from pathlib import Path
import json

@dataclass
class Pattern:
    pattern_id: str
    description: str
    frequency: int
    source_tasks: list[str]
    confidence: float
    category: str
    
    def to_dict(self):
        return {
            "pattern_id": self.pattern_id,
            "description": self.description,
            "frequency": self.frequency,
            "source_tasks": self.source_tasks,
            "confidence": self.confidence,
            "category": self.category
        }

class PatternRecognizer:
    def __init__(self, llm_client, experience_dir: Path):
        self.llm = llm_client
        self.patterns_dir = experience_dir / "patterns"
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
    
    def recognize(self, experiences: list) -> list[Pattern]:
        if len(experiences) < 3:
            return []  # 经验太少，无法识别模式
        
        prompt = self._build_prompt(experiences)
        response = self.llm.chat([
            {"role": "system", "content": "你是模式识别专家，从任务执行历史中提取可复用模式。"},
            {"role": "user", "content": prompt}
        ])
        
        patterns = self._parse_patterns(response, experiences)
        
        # 保存模式
        for p in patterns:
            file_path = self.patterns_dir / f"{p.pattern_id}.json"
            file_path.write_text(json.dumps(p.to_dict(), indent=2))
        
        return patterns
    
    def _build_prompt(self, experiences: list) -> str:
        exp_summaries = []
        for i, exp in enumerate(experiences, 1):
            status = "✓" if exp.success else "✗"
            exp_summaries.append(
                f"{i}. [{status}] {exp.description[:100]} (工具: {exp.tool_used})"
            )
        
        return f"""分析以下 {len(experiences)} 个任务执行记录，识别可复用的模式：

{chr(10).join(exp_summaries)}

请识别 1-2 个模式，每个模式包含：
1. 模式描述（简洁明确）
2. 适用场景
3. 建议的处理方式
4. 置信度（0.0-1.0）

格式：
[类别] 模式描述 | 置信度: X.X
适用场景: ...
建议: ..."""
    
    def _parse_patterns(self, response: str, experiences: list) -> list[Pattern]:
        patterns = []
        lines = response.strip().split('\n')
        
        current_pattern = None
        for line in lines:
            line = line.strip()
            if line.startswith('['):
                # 解析模式头
                import re
                match = re.match(r'\[([^\]]+)\]\s*(.+?)\s*\|\s*置信度:\s*([\d.]+)', line)
                if match:
                    category = match.group(1)
                    description = match.group(2)
                    confidence = float(match.group(3))
                    
                    if confidence >= 0.6:  # 置信度阈值
                        pattern_id = f"pattern-{len(patterns)+1}"
                        current_pattern = Pattern(
                            pattern_id=pattern_id,
                            description=description,
                            frequency=len(experiences),
                            source_tasks=[e.task_id for e in experiences],
                            confidence=confidence,
                            category=category
                        )
                        patterns.append(current_pattern)
        
        return patterns
```

---

### Story 1.3: Rule Generator
**优先级：** P0  
**预估：** 4h  
**依赖：** Story 1.2

**任务分解：**
1. 定义 `GeneratedRule` 数据类（0.5h）
2. 实现规则生成 prompt（1h）
3. 实现规则生成逻辑（2h）
4. 单元测试（0.5h）

**验收标准：**
- [ ] `GeneratedRule` 数据类定义
- [ ] 从模式生成规则（LLM 辅助）
- [ ] 规则格式化为 Markdown
- [ ] 置信度阈值过滤（<0.6 不生成）
- [ ] 测试覆盖率 >80%

**实现代码：**
```python
# src/ai_as_me/evolution/generator.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class GeneratedRule:
    rule_id: str
    category: str
    content: str
    source_pattern: str
    confidence: float
    created_at: datetime
    metadata: dict
    
    def to_markdown(self) -> str:
        return f"""---
source: {self.source_pattern}
created: {self.created_at.strftime('%Y-%m-%d')}
confidence: {self.confidence}
applied_count: 0
---

# {self.category} 规则

## 规则内容

{self.content}

## 来源

从模式 {self.source_pattern} 提取。

## 元数据

- 置信度: {self.confidence}
- 创建时间: {self.created_at.isoformat()}
"""

class RuleGenerator:
    def __init__(self, llm_client):
        self.llm = llm_client
    
    def generate(self, pattern) -> GeneratedRule | None:
        if pattern.confidence < 0.6:
            return None
        
        prompt = self._build_prompt(pattern)
        response = self.llm.chat([
            {"role": "system", "content": "你是规则生成专家，将模式转化为可执行的决策规则。"},
            {"role": "user", "content": prompt}
        ])
        
        return self._parse_rule(response, pattern)
    
    def _build_prompt(self, pattern) -> str:
        return f"""基于以下模式生成一条决策规则：

模式类别: {pattern.category}
模式描述: {pattern.description}
置信度: {pattern.confidence}

生成规则要求：
1. 明确的触发条件
2. 具体的行动建议
3. 简洁清晰（1-2 句话）

格式：
当 [触发条件] 时，[行动建议]。"""
    
    def _parse_rule(self, response: str, pattern) -> GeneratedRule:
        rule_id = f"rule-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return GeneratedRule(
            rule_id=rule_id,
            category=pattern.category,
            content=response.strip(),
            source_pattern=pattern.pattern_id,
            confidence=pattern.confidence,
            created_at=datetime.now(),
            metadata={
                "source_tasks": pattern.source_tasks,
                "frequency": pattern.frequency
            }
        )
```

---

### Story 1.4: Soul Writer
**优先级：** P0  
**预估：** 2h  
**依赖：** Story 2.1 (Soul 目录重构)

**任务分解：**
1. 实现 `write_rule()` 方法（1h）
2. 实现规则格式化（0.5h）
3. 单元测试（0.5h）

**验收标准：**
- [ ] 创建 `soul/rules/learned/` 目录
- [ ] 规则写入为独立 Markdown 文件
- [ ] 文件命名：`{category}-{timestamp}.md`
- [ ] 包含元数据（source, confidence, created）
- [ ] 测试覆盖率 >80%

**实现代码：**
```python
# src/ai_as_me/evolution/writer.py
from pathlib import Path

class SoulWriter:
    def __init__(self, soul_dir: Path):
        self.learned_dir = soul_dir / "rules" / "learned"
        self.learned_dir.mkdir(parents=True, exist_ok=True)
    
    def write_rule(self, rule) -> Path:
        filename = f"{rule.category}-{rule.rule_id}.md"
        path = self.learned_dir / filename
        
        content = rule.to_markdown()
        path.write_text(content)
        
        return path
    
    def list_rules(self) -> list[Path]:
        return sorted(self.learned_dir.glob("*.md"))
    
    def count_rules(self) -> int:
        return len(self.list_rules())
```

---

### Story 1.5: Evolution Engine 集成
**优先级：** P0  
**预估：** 4h  
**依赖：** Story 1.1-1.4

**任务分解：**
1. 实现 `EvolutionEngine` 主类（2h）
2. 集成到 `Agent._process_task()`（1h）
3. 集成测试（1h）

**验收标准：**
- [ ] `EvolutionEngine` 主类实现
- [ ] 编排完整进化流程
- [ ] 集成到 `Agent._process_task()`
- [ ] 每任务完成后自动触发
- [ ] 端到端测试通过

**实现代码：**
```python
# src/ai_as_me/evolution/engine.py
from pathlib import Path

class EvolutionEngine:
    def __init__(self, config: dict):
        self.collector = ExperienceCollector(
            Path(config['experience_dir']),
            config['vector_store']
        )
        self.recognizer = PatternRecognizer(
            config['llm_client'],
            Path(config['experience_dir'])
        )
        self.generator = RuleGenerator(config['llm_client'])
        self.writer = SoulWriter(Path(config['soul_dir']))
    
    def evolve(self, task, result: str, success: bool, duration: float = 0) -> dict:
        # 1. 收集经验
        exp = self.collector.collect(task, result, success, duration)
        
        # 2. 获取近期经验
        recent = self.collector.get_recent(limit=10)
        
        # 3. 识别模式
        patterns = self.recognizer.recognize(recent)
        
        # 4. 生成规则
        rules = []
        for p in patterns:
            rule = self.generator.generate(p)
            if rule:
                path = self.writer.write_rule(rule)
                rules.append({"rule": rule, "path": path})
        
        return {
            "experience": exp,
            "patterns": patterns,
            "rules": rules
        }
```

**Agent 集成：**
```python
# src/ai_as_me/core/agent.py 修改
def _process_task(self, task_path: Path):
    # ... 现有执行逻辑 ...
    
    if success and self.evolution_engine:
        # 触发进化
        start_time = time.time()
        evolution_result = self.evolution_engine.evolve(
            task, result, success=True, duration=time.time() - start_time
        )
        
        if evolution_result["rules"]:
            print(f"  🧬 进化: 生成 {len(evolution_result['rules'])} 条新规则")
            for r in evolution_result["rules"]:
                print(f"     - [{r['rule'].category}] {r['rule'].content[:50]}...")
```

---

## Epic 2: Soul 系统扩展 (P0)

**目标：** 支持 rules/ 目录结构和 learned/ 规则加载

### Story 2.1: Soul 目录重构
**优先级：** P0  
**预估：** 2h  
**依赖：** 无

**任务分解：**
1. 创建目录结构（0.5h）
2. 编写迁移脚本（1h）
3. 测试迁移（0.5h）

**验收标准：**
- [ ] 创建 `soul/rules/core/` 目录
- [ ] 创建 `soul/rules/learned/` 目录
- [ ] 迁移脚本：`rules.md` → `rules/core/base.md`
- [ ] 保留 `rules.md` 作为备份

**实现代码：**
```python
# src/ai_as_me/soul/migrator.py
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
        # 创建目录
        self.core_dir.mkdir(parents=True, exist_ok=True)
        self.learned_dir.mkdir(parents=True, exist_ok=True)
        
        # 迁移 rules.md
        if self.old_rules.exists():
            # 备份
            backup = self.soul_dir / "rules.md.backup"
            shutil.copy(self.old_rules, backup)
            
            # 迁移到 core/base.md
            new_path = self.core_dir / "base.md"
            shutil.move(self.old_rules, new_path)
            
            print(f"✓ 迁移完成: rules.md → rules/core/base.md")
            print(f"✓ 备份保存: rules.md.backup")
        
        # 创建 .gitkeep
        (self.learned_dir / ".gitkeep").touch()
```

**CLI 命令：**
```python
# src/ai_as_me/cli_main.py 添加
@cli.command()
def migrate_soul():
    """迁移 Soul 目录到 v3.0 结构"""
    from ai_as_me.soul.migrator import SoulMigrator
    migrator = SoulMigrator(Path("soul"))
    migrator.migrate()
```

---

### Story 2.2: SoulLoader 扩展
**优先级：** P0  
**预估：** 2h  
**依赖：** Story 2.1

**任务分解：**
1. 实现 `load_all_rules()` 方法（1h）
2. 兼容旧结构（0.5h）
3. 单元测试（0.5h）

**验收标准：**
- [ ] `load_all_rules()` 加载 core + learned
- [ ] 兼容旧 `rules.md` 结构
- [ ] 首次运行自动迁移
- [ ] 测试覆盖率 >80%

**实现代码：**
```python
# src/ai_as_me/soul/loader.py 扩展
class SoulLoader:
    def __init__(self, soul_dir: Path):
        # ... 现有代码 ...
        self.rules_dir = soul_dir / "rules"
        self.core_rules_dir = self.rules_dir / "core"
        self.learned_rules_dir = self.rules_dir / "learned"
        self.old_rules_file = soul_dir / "rules.md"
    
    def load_all_rules(self) -> str:
        """加载所有规则（core + learned）"""
        # 检查是否需要迁移
        if self.old_rules_file.exists() and not self.rules_dir.exists():
            from ai_as_me.soul.migrator import SoulMigrator
            migrator = SoulMigrator(self.soul_dir)
            migrator.migrate()
        
        rules = []
        
        # 加载 core 规则
        if self.core_rules_dir.exists():
            for f in sorted(self.core_rules_dir.glob("*.md")):
                rules.append(f"## Core Rule: {f.stem}\n{f.read_text()}")
        
        # 加载 learned 规则
        if self.learned_rules_dir.exists():
            for f in sorted(self.learned_rules_dir.glob("*.md")):
                rules.append(f"## Learned Rule: {f.stem}\n{f.read_text()}")
        
        return "\n\n".join(rules) if rules else "# No rules defined"
    
    def load_all(self) -> str:
        """加载完整 Soul 上下文"""
        parts = []
        
        if self.profile_file.exists():
            parts.append(f"# Profile\n{self.profile_file.read_text()}")
        
        parts.append(f"# Rules\n{self.load_all_rules()}")
        
        if self.mission_file.exists():
            parts.append(f"# Mission\n{self.mission_file.read_text()}")
        
        return "\n\n".join(parts)
```

---

## Epic 3: Experience 目录 (P1)

**目标：** 结构化存储执行经验

### Story 3.1: Experience 目录结构
**优先级：** P1  
**预估：** 1h  
**依赖：** 无

**任务分解：**
1. 创建目录结构（0.5h）
2. 添加 README（0.5h）

**验收标准：**
- [ ] 创建 `experience/successes/`
- [ ] 创建 `experience/failures/`
- [ ] 创建 `experience/patterns/`
- [ ] `.gitkeep` 文件
- [ ] README.md 说明

**实现：**
```bash
mkdir -p experience/{successes,failures,patterns}
touch experience/{successes,failures,patterns}/.gitkeep
```

```markdown
# experience/README.md
# Experience 目录

存储任务执行经验和识别的模式。

## 目录结构

- `successes/` - 成功执行的任务经验
- `failures/` - 失败的任务经验
- `patterns/` - 识别出的可复用模式

## 文件格式

所有文件使用 JSON 格式，文件名为 `{task_id}.json`。
```

---

### Story 3.2: Experience 文件格式
**优先级：** P1  
**预估：** 1h  
**依赖：** Story 3.1

**验收标准：**
- [ ] JSON 格式定义
- [ ] 包含：task_id, description, tool, result, success, timestamp
- [ ] 文件命名：`{task_id}.json`
- [ ] Schema 文档

**格式定义：**
```json
{
  "task_id": "task-20260115-001",
  "description": "实现 Experience Collector",
  "tool_used": "claude_code",
  "result": "成功实现，测试通过",
  "success": true,
  "duration": 3600.5,
  "timestamp": "2026-01-15T19:00:00+08:00"
}
```

---

## Epic 4: Skills 架构 (P1)

**目标：** 实现 Skills 调用机制

### Story 4.1: SKILL.md 格式定义
**优先级：** P1  
**预估：** 1h  
**依赖：** 无

**验收标准：**
- [ ] YAML frontmatter 定义（name, triggers）
- [ ] 能力描述部分
- [ ] 调用方式说明
- [ ] 格式文档

**格式定义：**
```markdown
# skills/SKILL_FORMAT.md
---
name: skill_name
triggers:
  - task_type: architecture
  - task_type: planning
  - capability_gap: true
version: 1.0
---

# Skill Name

## 能力描述

描述这个 Skill 提供的能力。

## 触发条件

- 任务类型为 architecture 或 planning
- 检测到能力缺口时

## 调用方式

说明如何调用这个 Skill。
```

---

### Story 4.2: BMad Skill 创建
**优先级：** P1  
**预估：** 2h  
**依赖：** Story 4.1

**验收标准：**
- [ ] 创建 `skills/bmad/SKILL.md`
- [ ] 定义触发条件（architecture, planning, capability_gap）
- [ ] 关联 `_bmad/` 目录
- [ ] 使用说明

**实现：**
```markdown
# skills/bmad/SKILL.md
---
name: bmad
triggers:
  - task_type: architecture
  - task_type: planning
  - capability_gap: true
version: 1.0
---

# BMad Method Skill

## 能力描述

BMad Method 提供完整的软件开发方法论支持，包括：
- 产品分析（Product Brief）
- 需求规划（PRD）
- 架构设计（Architecture）
- 任务分解（Epics & Stories）

## 触发条件

1. 任务类型为 architecture 或 planning
2. 检测到能力缺口（现有工具无法处理）

## 调用方式

加载 `_bmad/` 目录下的相关工作流：
- `_bmad/bmm/workflows/1-analysis/` - 产品分析
- `_bmad/bmm/workflows/2-plan-workflows/` - 需求规划
- `_bmad/bmm/workflows/3-solutioning/` - 架构设计
```

---

### Story 4.3: SkillLoader 实现
**优先级：** P1  
**预估：** 3h  
**依赖：** Story 4.1, 4.2

**任务分解：**
1. 实现 `SkillLoader` 类（1.5h）
2. 集成到 `SkillMatcher`（1h）
3. 单元测试（0.5h）

**验收标准：**
- [ ] 加载 SKILL.md 文件
- [ ] 解析触发条件
- [ ] `should_invoke()` 判断逻辑
- [ ] 集成到 SkillMatcher
- [ ] 测试覆盖率 >80%

**实现代码：**
```python
# src/ai_as_me/skills/loader.py
from dataclasses import dataclass
from pathlib import Path
import yaml

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
        skill_file = self.skills_dir / name / "SKILL.md"
        if not skill_file.exists():
            return None
        
        content = skill_file.read_text()
        
        # 解析 YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            frontmatter = yaml.safe_load(parts[1])
            description = parts[2].strip()
            
            return Skill(
                name=frontmatter['name'],
                triggers=frontmatter.get('triggers', []),
                description=description,
                invoke_path=str(skill_file.parent)
            )
        
        return None
    
    def should_invoke(self, skill: Skill, task, capability_gap: bool = False) -> bool:
        for trigger in skill.triggers:
            if 'task_type' in trigger:
                if hasattr(task, 'type') and task.type == trigger['task_type']:
                    return True
            if 'capability_gap' in trigger and trigger['capability_gap']:
                if capability_gap:
                    return True
        return False
```

**集成到 SkillMatcher：**
```python
# src/ai_as_me/orchestrator/skill_matcher.py 扩展
class SkillMatcher:
    def __init__(self, config_path: Path, db_path: str):
        # ... 现有代码 ...
        self.skill_loader = SkillLoader(Path("skills"))
    
    def match_with_skills(self, task_description: str):
        # 1. 尝试常规工具匹配
        tool = self.match(task_description)
        
        # 2. 检测能力缺口
        gap = self.detect_capability_gap(task_description)
        
        # 3. 如果有缺口，尝试 Skills
        if gap:
            bmad_skill = self.skill_loader.load_skill("bmad")
            if bmad_skill and self.skill_loader.should_invoke(bmad_skill, task, gap):
                return {"tool": tool, "skill": "bmad", "capability_gap": True}
        
        return {"tool": tool, "skill": None, "capability_gap": False}
```

---

## Epic 5: 进化日志 (P1)

**目标：** 记录和追踪进化过程

### Story 5.1: Evolution Logger
**优先级：** P1  
**预估：** 2h  
**依赖：** Epic 1

**任务分解：**
1. 实现 `EvolutionLogger` 类（1h）
2. 集成到 `EvolutionEngine`（0.5h）
3. 单元测试（0.5h）

**验收标准：**
- [ ] 创建 `logs/evolution.jsonl`
- [ ] 记录：timestamp, task_id, patterns_found, rules_generated
- [ ] JSON Lines 格式
- [ ] 测试覆盖率 >80%

**实现代码：**
```python
# src/ai_as_me/evolution/logger.py
from pathlib import Path
import json
from datetime import datetime

class EvolutionLogger:
    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def log(self, exp, patterns: list, rules: list):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": exp.task_id,
            "experience_recorded": True,
            "patterns_found": len(patterns),
            "rules_generated": len(rules),
            "rule_ids": [r.rule_id for r in rules],
            "rule_categories": [r.category for r in rules]
        }
        
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
    
    def get_stats(self, days: int = 7) -> dict:
        """获取最近 N 天的统计"""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)
        
        total_rules = 0
        total_patterns = 0
        
        if not self.log_path.exists():
            return {"total_rules": 0, "total_patterns": 0}
        
        with open(self.log_path) as f:
            for line in f:
                entry = json.loads(line)
                entry_time = datetime.fromisoformat(entry['timestamp'])
                if entry_time >= cutoff:
                    total_rules += entry['rules_generated']
                    total_patterns += entry['patterns_found']
        
        return {
            "total_rules": total_rules,
            "total_patterns": total_patterns,
            "days": days
        }
```

---

### Story 5.2: 进化统计 CLI
**优先级：** P2  
**预估：** 2h  
**依赖：** Story 5.1

**验收标准：**
- [ ] `ai-as-me evolve stats` 命令
- [ ] 显示：总规则数、本周新增、应用次数
- [ ] 格式化输出

**实现代码：**
```python
# src/ai_as_me/cli_main.py 添加
@cli.group()
def evolve():
    """进化相关命令"""
    pass

@evolve.command()
@click.option('--days', default=7, help='统计天数')
def stats(days):
    """显示进化统计"""
    from ai_as_me.evolution.logger import EvolutionLogger
    logger = EvolutionLogger(Path("logs/evolution.jsonl"))
    stats = logger.get_stats(days)
    
    click.echo(f"📊 进化统计（最近 {days} 天）")
    click.echo(f"  规则生成: {stats['total_rules']} 条")
    click.echo(f"  模式识别: {stats['total_patterns']} 个")
```

---

## Epic 6: OpenCode 集成 (P1)

**目标：** 完善 MVP 工具栈

### Story 6.1: OpenCode 配置
**优先级：** P1  
**预估：** 2h  
**依赖：** 无

**任务分解：**
1. 创建 `.opencode/config.yaml`（1h）
2. 定义自定义命令（0.5h）
3. 测试验证（0.5h）

**验收标准：**
- [ ] 创建 `.opencode/config.yaml`
- [ ] 定义 default agent（加载 Soul）
- [ ] 自定义命令：soul-check, evolve
- [ ] 配置验证通过

**实现：**
```yaml
# .opencode/config.yaml
version: 1
project:
  name: AI-as-Me
  type: python
  description: 自进化 AI 数字分身系统

agents:
  default:
    system_prompt: |
      你是 AI-as-Me，一个能自我进化的 AI 代理。
      
      你的 Soul（灵魂）包含：
      - Profile: soul/profile.md
      - Mission: soul/mission.md
      - Core Rules: soul/rules/core/*.md
      - Learned Rules: soul/rules/learned/*.md
      
      你会从每次任务执行中学习，自动生成新规则到 learned/ 目录。

commands:
  soul-check:
    description: 检查 Soul 状态
    script: |
      python -m ai_as_me.cli soul status
  
  evolve:
    description: 手动触发进化反思
    script: |
      python -m ai_as_me.cli evolve --force
  
  stats:
    description: 查看进化统计
    script: |
      python -m ai_as_me.cli evolve stats
```

```markdown
# .opencode/agents/default.md
# AI-as-Me Default Agent

加载完整 Soul 上下文，包括：
- Profile（个人档案）
- Mission（使命目标）
- Core Rules（核心规则）
- Learned Rules（学习规则）

支持自我进化，每次任务执行后自动学习。
```

---

## 总结

| Epic | Stories | 预估总时长 | 优先级 |
|------|---------|-----------|--------|
| Epic 1: 进化引擎 | 5 | 20h | P0 |
| Epic 2: Soul 扩展 | 2 | 4h | P0 |
| Epic 3: Experience | 2 | 2h | P1 |
| Epic 4: Skills | 3 | 6h | P1 |
| Epic 5: 进化日志 | 2 | 4h | P1 |
| Epic 6: OpenCode | 1 | 2h | P1 |

**总计：15 Stories，约 38h（5-6 工作日）**

### 实施顺序

```
Week 1:
├── Epic 1: 进化引擎核心 (P0)
└── Epic 2: Soul 系统扩展 (P0)

Week 2:
├── Epic 3: Experience 目录 (P1)
├── Epic 4: Skills 架构 (P1)
├── Epic 5: 进化日志 (P1)
└── Epic 6: OpenCode 集成 (P1)
```
