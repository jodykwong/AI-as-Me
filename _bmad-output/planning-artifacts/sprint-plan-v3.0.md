---
version: v3.0
date: 2026-01-15
status: planned
sprints: 2
---

# Sprint Plan - AI-as-Me v3.0

## Sprint 1: 进化核心 (P0)

**目标：** 实现完整进化闭环
**时间：** 3 工作日
**开始：** 2026-01-16

### Day 1: Soul 基础 + Experience 收集

| # | Story | 任务 | 预估 | 状态 |
|---|-------|------|------|------|
| 1 | 2.1 | 创建 `soul/rules/core/` 和 `learned/` 目录 | 0.5h | ⬜ |
| 2 | 2.1 | 迁移 `rules.md` → `rules/core/base.md` | 0.5h | ⬜ |
| 3 | 2.2 | 扩展 `SoulLoader.load_all_rules()` | 1h | ⬜ |
| 4 | 1.1 | 定义 `Experience` 数据类 | 0.5h | ⬜ |
| 5 | 1.1 | 实现 `ExperienceCollector.collect()` | 2h | ⬜ |
| 6 | 1.1 | 实现 `ExperienceCollector.get_recent()` | 1h | ⬜ |

**Day 1 产出：**
- `soul/rules/` 目录结构
- `src/ai_as_me/evolution/collector.py`

---

### Day 2: 模式识别 + 规则生成

| # | Story | 任务 | 预估 | 状态 |
|---|-------|------|------|------|
| 7 | 1.2 | 定义 `Pattern` 数据类 | 0.5h | ⬜ |
| 8 | 1.2 | 实现 `PatternRecognizer.recognize()` | 4h | ⬜ |
| 9 | 1.3 | 定义 `GeneratedRule` 数据类 | 0.5h | ⬜ |
| 10 | 1.3 | 实现 `RuleGenerator.generate()` | 3h | ⬜ |

**Day 2 产出：**
- `src/ai_as_me/evolution/recognizer.py`
- `src/ai_as_me/evolution/generator.py`

---

### Day 3: 写入 + 集成

| # | Story | 任务 | 预估 | 状态 |
|---|-------|------|------|------|
| 11 | 1.4 | 实现 `SoulWriter.write_rule()` | 2h | ⬜ |
| 12 | 1.5 | 实现 `EvolutionEngine.evolve()` | 2h | ⬜ |
| 13 | 1.5 | 集成到 `Agent._process_task()` | 1h | ⬜ |
| 14 | - | Sprint 1 测试验证 | 2h | ⬜ |

**Day 3 产出：**
- `src/ai_as_me/evolution/writer.py`
- `src/ai_as_me/evolution/engine.py`
- 进化闭环可运行

---

### Sprint 1 验收标准

- [ ] 任务完成后自动触发进化
- [ ] 经验记录到 `experience/`
- [ ] 模式识别并生成规则
- [ ] 规则写入 `soul/rules/learned/`
- [ ] 进化闭环完整率 100%

---

## Sprint 2: 完善功能 (P1)

**目标：** 完成 P1 功能
**时间：** 1.5 工作日
**开始：** Sprint 1 完成后

### Day 4: Experience + Skills

| # | Story | 任务 | 预估 | 状态 |
|---|-------|------|------|------|
| 15 | 3.1 | 创建 `experience/` 目录结构 | 0.5h | ⬜ |
| 16 | 3.2 | 定义 Experience JSON 格式 | 0.5h | ⬜ |
| 17 | 4.1 | 定义 SKILL.md 格式 | 0.5h | ⬜ |
| 18 | 4.2 | 创建 `skills/bmad/SKILL.md` | 1h | ⬜ |
| 19 | 4.3 | 实现 `SkillLoader` | 2h | ⬜ |
| 20 | 5.1 | 实现 `EvolutionLogger` | 1.5h | ⬜ |

---

### Day 5: OpenCode + 收尾

| # | Story | 任务 | 预估 | 状态 |
|---|-------|------|------|------|
| 21 | 6.1 | 创建 `.opencode/config.yaml` | 1h | ⬜ |
| 22 | 6.1 | 定义自定义命令 | 0.5h | ⬜ |
| 23 | - | 集成测试 | 1.5h | ⬜ |
| 24 | - | 文档更新 | 1h | ⬜ |

---

### Sprint 2 验收标准

- [ ] `experience/` 目录结构完整
- [ ] `skills/bmad/SKILL.md` 可用
- [ ] 进化日志记录正常
- [ ] `.opencode/` 配置完整
- [ ] README 更新

---

## 文件创建清单

### 新建文件

```
src/ai_as_me/evolution/
├── __init__.py
├── collector.py      # Story 1.1
├── recognizer.py     # Story 1.2
├── generator.py      # Story 1.3
├── writer.py         # Story 1.4
├── engine.py         # Story 1.5
└── logger.py         # Story 5.1

src/ai_as_me/skills/
├── __init__.py
└── loader.py         # Story 4.3

soul/rules/
├── core/
│   └── base.md       # 迁移自 rules.md
└── learned/
    └── .gitkeep

experience/
├── successes/
├── failures/
├── patterns/
└── .gitkeep

skills/bmad/
└── SKILL.md          # Story 4.2

logs/
└── evolution.jsonl   # Story 5.1

.opencode/
├── config.yaml       # Story 6.1
└── agents/
    └── default.md
```

### 修改文件

```
src/ai_as_me/soul/loader.py    # Story 2.2
src/ai_as_me/core/agent.py     # Story 1.5
config/settings.yaml           # 添加 evolution 配置
```

---

## 进度追踪

| Sprint | Stories | 完成 | 进度 |
|--------|---------|------|------|
| Sprint 1 | 7 | 0 | 0% |
| Sprint 2 | 6 | 0 | 0% |
| **总计** | **13** | **0** | **0%** |

---

## 启动命令

```bash
# 1. 创建分支
git checkout -b feature/v3.0-evolution

# 2. 备份 Soul
cp soul/rules.md soul/rules.md.backup

# 3. 开始 Story 2.1
mkdir -p soul/rules/core soul/rules/learned
mv soul/rules.md soul/rules/core/base.md
touch soul/rules/learned/.gitkeep
```
