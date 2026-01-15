# v3.0 后续工作建议

**基于：** Code Review v3.0 + BMad Method 工作流  
**日期：** 2026-01-15

---

## 📋 工作清单

### Phase 1: 完成 P0 阻塞项（4-6h）

#### 1. Agent 集成（2h）

**任务：** 将 EvolutionEngine 集成到 Agent 主循环

```python
# src/ai_as_me/core/agent.py

class Agent:
    def __init__(self, ...):
        # 添加 EvolutionEngine
        if llm_client:
            from ai_as_me.evolution.engine import EvolutionEngine
            self.evolution_engine = EvolutionEngine({
                'experience_dir': 'experience',
                'soul_dir': 'soul',
                'llm_client': llm_client,
                'vector_store': vector_store,
                'log_path': 'logs/evolution.jsonl'
            })
    
    def _process_task(self, task_path: Path):
        # ... 现有执行逻辑 ...
        
        if success and self.evolution_engine:
            # 触发进化
            evolution_result = self.evolution_engine.evolve(
                task, result, success=True, duration=duration
            )
            if evolution_result["rules"]:
                print(f"  🧬 进化: 生成 {len(evolution_result['rules'])} 条新规则")
```

**验收：**
- [ ] Agent 启动时初始化 EvolutionEngine
- [ ] 任务完成后自动触发进化
- [ ] 进化结果输出到日志

---

#### 2. 端到端测试（2h）

**任务：** 创建集成测试验证完整流程

```python
# tests/integration/test_evolution_flow.py

def test_complete_evolution_flow():
    """测试完整进化闭环"""
    # 1. 创建测试任务
    task = create_test_task()
    
    # 2. 执行任务
    result = execute_task(task)
    
    # 3. 验证经验记录
    assert experience_exists(task.id)
    
    # 4. 验证模式识别
    patterns = get_patterns()
    assert len(patterns) > 0
    
    # 5. 验证规则生成
    rules = get_learned_rules()
    assert len(rules) > 0
    
    # 6. 验证进化日志
    log = get_evolution_log()
    assert log[-1]['task_id'] == task.id
```

**验收：**
- [ ] 测试通过
- [ ] 覆盖完整进化流程
- [ ] 验证所有组件协作

---

#### 3. 基础单元测试（2h）

**任务：** 为核心模块添加单元测试

```python
# tests/unit/test_evolution_collector.py
def test_collect_success()
def test_collect_failure()
def test_get_recent()

# tests/unit/test_soul_writer.py
def test_write_rule()
def test_list_rules()
```

**验收：**
- [ ] ExperienceCollector 测试通过
- [ ] SoulWriter 测试通过
- [ ] 覆盖率 >60%

---

### Phase 2: 完成 P1 质量项（6-8h）

#### 4. 完善单元测试（3h）

- PatternRecognizer 测试
- RuleGenerator 测试
- EvolutionEngine 测试
- SkillLoader 测试

**目标：** 覆盖率 >80%

---

#### 5. 类型注解完善（1h）

```python
# 修复所有类型注解
from typing import Optional, List, Dict, Any

def collect(self, task: Task, result: str, ...) -> Experience:
    ...
```

---

#### 6. 错误处理优化（2h）

```python
# 定义自定义异常
class EvolutionError(Exception): pass
class PatternRecognitionError(EvolutionError): pass
class RuleGenerationError(EvolutionError): pass

# 细化异常处理
try:
    patterns = self.recognizer.recognize(recent)
except PatternRecognitionError as e:
    logger.error(f"Pattern recognition failed: {e}")
    # 降级处理
```

---

#### 7. README 更新（2h）

添加 v3.0 使用说明：
- 进化引擎介绍
- Skills 使用方法
- OpenCode 集成说明
- 故障排查指南

---

### Phase 3: 优化和增强（可选）

#### 8. 性能优化

- 规则加载缓存
- 异步向量存储
- LLM 调用超时控制

#### 9. 规则管理

- 规则冲突检测
- 规则优先级机制
- 规则版本控制

#### 10. 监控和可观测性

- Prometheus metrics
- 进化成功率监控
- 规则应用统计

---

## 🎯 推荐执行顺序

### 立即执行（今天）

1. **Agent 集成** - 2h
2. **端到端测试** - 2h

**目标：** 验证核心功能可运行

---

### 明天执行

3. **基础单元测试** - 2h
4. **README 更新** - 2h

**目标：** 达到可发布状态

---

### 本周内完成

5. **完善单元测试** - 3h
6. **类型注解** - 1h
7. **错误处理** - 2h

**目标：** 达到生产质量

---

## 📊 里程碑

| 里程碑 | 完成标准 | 预估时间 |
|--------|----------|----------|
| **M1: 可运行** | P0 完成 | 4-6h |
| **M2: 可发布** | P0 + 基础测试 + README | 8-10h |
| **M3: 生产就绪** | P0 + P1 全部完成 | 14-18h |

---

## ✅ 验收标准

### M1 验收（可运行）

- [ ] Agent 集成完成
- [ ] 端到端测试通过
- [ ] 手动测试验证进化闭环

### M2 验收（可发布）

- [ ] M1 完成
- [ ] 基础单元测试通过
- [ ] README 更新完成
- [ ] 代码 review 通过

### M3 验收（生产就绪）

- [ ] M2 完成
- [ ] 测试覆盖率 >80%
- [ ] 类型注解完整
- [ ] 错误处理完善
- [ ] 性能测试通过

---

## 🚀 发布计划

### v3.0-alpha（M1 完成后）

- 内部测试版本
- 验证核心功能

### v3.0-beta（M2 完成后）

- 公开测试版本
- 收集用户反馈

### v3.0-stable（M3 完成后）

- 正式发布版本
- 合并到 main 分支

---

## 📝 下一步行动

**立即开始：**

```bash
# 1. 创建 P0 分支
git checkout -b feature/v3.0-p0-integration

# 2. 开始 Agent 集成
# 编辑 src/ai_as_me/core/agent.py

# 3. 创建测试
# 创建 tests/integration/test_evolution_flow.py
```

**BMad Master 建议：立即开始 Phase 1，预计 4-6 小时完成 M1。**
