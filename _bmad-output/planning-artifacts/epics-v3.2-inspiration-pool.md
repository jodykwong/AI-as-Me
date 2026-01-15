# AI-as-Me v3.2 Epics & Stories - 灵感池机制

**文档版本**: 1.0  
**创建日期**: 2026-01-15

---

## Epic 1: 灵感捕获与存储

### Story 1.1: 灵感数据模型
**描述**: 实现 Inspiration 数据类和存储格式  
**估时**: 2h

**任务**:
- [ ] 创建 `inspiration/__init__.py`
- [ ] 定义 Inspiration dataclass
- [ ] 实现 JSON 序列化/反序列化

**验收标准**:
- Inspiration 对象可正确创建
- 可序列化为 JSON

---

### Story 1.2: 灵感池管理
**描述**: 实现 InspirationPool 类  
**估时**: 3h

**任务**:
- [ ] 创建 `inspiration/pool.py`
- [ ] 实现 add/get/list/update/archive 方法
- [ ] 实现 index.json 维护

**验收标准**:
- CRUD 操作正常
- 索引自动更新

---

### Story 1.3: 灵感捕获器
**描述**: 实现从文本和任务中捕获灵感  
**估时**: 3h

**任务**:
- [ ] 创建 `inspiration/capturer.py`
- [ ] 实现 TRIGGER_PATTERNS 匹配
- [ ] 实现 capture_from_text 和 capture_from_task

**验收标准**:
- 关键词触发正确识别
- 捕获的灵感包含完整上下文

---

## Epic 2: 灵感孵化

### Story 2.1: 成熟度计算
**描述**: 实现灵感成熟度算法  
**估时**: 2h

**任务**:
- [ ] 创建 `inspiration/incubator.py`
- [ ] 实现 calculate_maturity 方法
- [ ] 支持时间/提及/优先级三因素

**验收标准**:
- 成熟度范围 0.0-1.0
- 算法符合设计文档

---

### Story 2.2: 批量孵化
**描述**: 实现定期孵化和成熟灵感筛选  
**估时**: 2h

**任务**:
- [ ] 实现 incubate_all 方法
- [ ] 实现 get_mature 方法
- [ ] 自动更新灵感状态

**验收标准**:
- 可批量更新成熟度
- 正确筛选成熟灵感

---

## Epic 3: 灵感转化

### Story 3.1: 转化为规则
**描述**: 将灵感转化为 Soul 规则  
**估时**: 3h

**任务**:
- [ ] 创建 `inspiration/converter.py`
- [ ] 实现 to_rule 方法
- [ ] 集成 Evolution Engine

**验收标准**:
- 生成的规则符合规范
- 规则写入 soul/rules/learned/

---

### Story 3.2: 转化为任务
**描述**: 将灵感转化为 Kanban 任务  
**估时**: 2h

**任务**:
- [ ] 实现 to_task 方法
- [ ] 集成 Kanban API

**验收标准**:
- 任务创建成功
- 关联原始灵感 ID

---

## Epic 4: CLI 集成

### Story 4.1: inspiration 命令组
**描述**: 实现 CLI 命令  
**估时**: 3h

**任务**:
- [ ] 添加 inspiration 命令组到 cli_main.py
- [ ] 实现 add/list/show/mature/convert/archive/stats 子命令

**验收标准**:
- 所有命令可正常执行
- 输出格式友好

---

### Story 4.2: Agent 集成
**描述**: 在 Agent 中自动捕获灵感  
**估时**: 2h

**任务**:
- [ ] 修改 agent.py 集成 Capturer
- [ ] 对话处理时自动捕获

**验收标准**:
- 对话中的灵感自动记录
- 不影响正常对话流程

---

## Epic 5: 测试与文档

### Story 5.1: 单元测试
**描述**: 编写核心模块测试  
**估时**: 2h

**任务**:
- [ ] 创建 `tests/unit/test_inspiration.py`
- [ ] 测试 Capturer 模式匹配
- [ ] 测试成熟度计算
- [ ] 测试 Pool CRUD

**验收标准**:
- 测试覆盖率 > 80%
- 所有测试通过

---

## 总结

| Epic | Stories | 估时 |
|------|---------|------|
| Epic 1: 捕获与存储 | 3 | 8h |
| Epic 2: 孵化 | 2 | 4h |
| Epic 3: 转化 | 2 | 5h |
| Epic 4: CLI 集成 | 2 | 5h |
| Epic 5: 测试 | 1 | 2h |
| **总计** | **10** | **24h** |

---

**下一步**: 开始实现 Epic 1
