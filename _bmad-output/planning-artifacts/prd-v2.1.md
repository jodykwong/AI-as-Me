# Product Requirements Document - AI-as-Me v2.1

**Author:** BMad Master
**Date:** 2026-01-14
**Status:** Draft
**Base Document:** prd-v2.0.md

---

## 1. 版本概述

### 1.1 版本目标
v2.1 在 MVP 基础上增强三个核心 P1 功能，提升系统智能化和可视化能力。

### 1.2 前置条件
- v2.0 MVP 功能稳定运行
- FR-01 ~ FR-04 已完成验证

---

## 2. P1 功能需求详细定义

### FR-05: 多工具智能选择

#### 2.1.1 功能描述
系统根据任务特征自动选择最适合的 Agent CLI 工具执行。

#### 2.1.2 用户故事
```
作为 Jody，
我希望系统能自动选择最合适的工具，
以便我不需要每次手动指定工具。
```

#### 2.1.3 功能规格

| 子功能 | 描述 | 优先级 |
|--------|------|--------|
| 任务类型识别 | 分析任务描述，识别类型（代码/文档/分析） | 必须 |
| 工具能力映射 | 维护工具-能力矩阵 | 必须 |
| 历史成功率 | 基于历史执行结果计算工具成功率 | 应该 |
| 手动覆盖 | `--tool` 参数允许用户指定工具 | 必须 |

#### 2.1.4 工具能力矩阵

| 工具 | 代码生成 | 代码审查 | 文档编写 | 架构设计 | 调试修复 |
|------|----------|----------|----------|----------|----------|
| Claude Code | ★★★ | ★★★ | ★★☆ | ★★★ | ★★☆ |
| OpenCode | ★★☆ | ★★☆ | ★☆☆ | ★☆☆ | ★★★ |
| Gemini CLI | ★★☆ | ★★☆ | ★★★ | ★★☆ | ★☆☆ |
| Qwen Code | ★★☆ | ★☆☆ | ★★☆ | ★☆☆ | ★★☆ |

#### 2.1.5 选择算法
```
score = task_type_match * 0.5 + history_success_rate * 0.3 + availability * 0.2
```

#### 2.1.6 接口设计
```python
# skill_matcher.py
class SkillMatcher:
    def match(self, task: Task) -> Tool:
        """返回最匹配的工具"""
    
    def rank(self, task: Task) -> list[tuple[Tool, float]]:
        """返回工具排名和分数"""
```

#### 2.1.7 验收标准
- [ ] 工具选择准确率 >80%
- [ ] 支持 4 种 Agent CLI 工具
- [ ] 手动覆盖功能正常
- [ ] 选择决策可解释（日志记录原因）

---

### FR-06: Web 仪表板

#### 2.2.1 功能描述
提供可视化的任务管理和系统监控 Web 界面。

#### 2.2.2 用户故事
```
作为 Jody，
我希望通过 Web 界面查看任务状态和系统运行情况，
以便更直观地管理工作流程。
```

#### 2.2.3 功能规格

| 子功能 | 描述 | 优先级 |
|--------|------|--------|
| 任务看板 | Kanban 视图 (inbox/todo/doing/done) | 必须 |
| 任务创建 | Web 表单创建新任务 | 必须 |
| 实时状态 | SSE 推送任务执行状态 | 应该 |
| 系统监控 | 工具健康状态、资源使用 | 应该 |
| Soul 可视化 | 显示当前 Soul 配置和学习进度 | 可选 |

#### 2.2.4 技术栈
- **后端**: FastAPI + SSE
- **前端**: HTMX + Alpine.js (轻量级)
- **样式**: Tailwind CSS

#### 2.2.5 页面结构
```
/                    # 仪表板首页（任务看板）
/tasks               # 任务列表
/tasks/new           # 创建任务
/tasks/{id}          # 任务详情
/system              # 系统状态
/soul                # Soul 配置查看
```

#### 2.2.6 API 端点
```
GET  /api/tasks              # 获取任务列表
POST /api/tasks              # 创建任务
GET  /api/tasks/{id}         # 获取任务详情
PUT  /api/tasks/{id}/status  # 更新任务状态
GET  /api/system/health      # 系统健康检查
GET  /api/events             # SSE 事件流
```

#### 2.2.7 验收标准
- [ ] 任务看板正常显示四列
- [ ] 可通过 Web 创建和管理任务
- [ ] 任务状态实时更新（<2秒延迟）
- [ ] 移动端响应式布局
- [ ] `ai-as-me serve` 启动 Web 服务

---

### FR-07: Agentic RAG 检索

#### 2.3.1 功能描述
检索和利用历史任务经验，增强任务执行上下文。

#### 2.3.2 用户故事
```
作为 Jody，
我希望系统能记住并利用之前的成功经验，
以便相似任务能更快更好地完成。
```

#### 2.3.3 功能规格

| 子功能 | 描述 | 优先级 |
|--------|------|--------|
| 任务向量化 | 将任务描述和结果转为向量 | 必须 |
| 相似检索 | 检索相似历史任务 | 必须 |
| 上下文注入 | 将相关经验注入提示词 | 必须 |
| 反馈学习 | 根据用户反馈调整检索权重 | 应该 |

#### 2.3.4 技术方案
- **向量存储**: ChromaDB (本地轻量)
- **嵌入模型**: sentence-transformers/all-MiniLM-L6-v2
- **检索策略**: Top-K 相似度 + 时间衰减

#### 2.3.5 数据模型
```python
@dataclass
class TaskExperience:
    task_id: str
    description: str           # 任务描述
    tool_used: str             # 使用的工具
    result_summary: str        # 结果摘要
    success: bool              # 是否成功
    user_feedback: str | None  # 用户反馈
    created_at: datetime
    embedding: list[float]     # 向量表示
```

#### 2.3.6 检索流程
```
1. 新任务 → 向量化
2. 检索 Top-5 相似任务
3. 过滤成功案例
4. 构建上下文片段
5. 注入 Soul 提示词
```

#### 2.3.7 接口设计
```python
# rag/retriever.py
class ExperienceRetriever:
    def store(self, experience: TaskExperience) -> None:
        """存储任务经验"""
    
    def retrieve(self, query: str, top_k: int = 5) -> list[TaskExperience]:
        """检索相似经验"""
    
    def build_context(self, experiences: list[TaskExperience]) -> str:
        """构建上下文字符串"""
```

#### 2.3.8 验收标准
- [ ] 检索准确率 >85%（相关性评估）
- [ ] 检索响应时间 <500ms
- [ ] 支持至少 1000 条历史记录
- [ ] 上下文注入不超过 2000 tokens

---

## 3. 非功能需求补充

### 3.1 性能
- Web 仪表板页面加载 <3秒
- RAG 检索响应 <500ms
- 工具选择决策 <1秒

### 3.2 存储
- ChromaDB 数据目录: `~/.ai-as-me/rag/`
- 向量维度: 384 (MiniLM)
- 预估存储: ~1MB/1000条记录

---

## 4. 实施计划

| 功能 | 预估工时 | 依赖 |
|------|----------|------|
| FR-05 多工具选择 | 2天 | FR-01 |
| FR-06 Web 仪表板 | 3天 | FR-03 |
| FR-07 Agentic RAG | 2天 | FR-04 |

**总计**: 7天

---

## 5. 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 工具选择不准确 | 用户体验差 | 保留手动覆盖，收集反馈迭代 |
| RAG 检索慢 | 响应延迟 | 限制向量库大小，定期清理 |
| Web 安全漏洞 | 数据泄露 | 仅本地访问，无认证需求 |

---

## 6. 待确认事项

1. [ ] Web 仪表板是否需要用户认证？（建议：MVP 阶段仅本地访问，无需认证）
2. [ ] RAG 向量库是否需要云端备份？（建议：本地存储，用户自行备份）
3. [ ] 工具能力矩阵如何更新？（建议：配置文件 + 用户反馈自动调整）
