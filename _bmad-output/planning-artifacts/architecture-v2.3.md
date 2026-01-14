# Architecture Supplement - AI-as-Me v2.3

**Author:** BMad Master
**Date:** 2026-01-14
**Status:** Draft
**Base Document:** architecture-v2.1.md

---

## 1. 版本概述

v2.3 架构变更聚焦代码组织和可维护性，无重大架构调整。

---

## 2. 项目结构变更

### 2.1 新增目录

```
src/ai_as_me/
├── kanban/
│   ├── api.py              # 精简：仅API逻辑
│   └── templates/          # 新增：HTML模板目录
│       └── dashboard.html  # 提取的仪表板模板
├── config/
│   └── settings.yaml       # 新增：统一配置文件
└── ...

tests/
├── unit/
├── integration/
└── performance/            # 新增：性能测试
    └── test_benchmark.py
```

---

## 3. FR-11: 代码质量标准化

### 3.1 类型注解规范

```python
# 标准格式
def function_name(param1: str, param2: int = 0) -> dict[str, Any]:
    """函数描述"""
    pass

# 复杂类型使用 TypeAlias
TaskScores: TypeAlias = dict[str, float]
```

### 3.2 模板分离架构

```
┌─────────────┐     ┌──────────────────┐
│   api.py    │────▶│ Jinja2Templates  │
│  (逻辑)     │     │   (渲染引擎)     │
└─────────────┘     └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │ templates/       │
                    │ └─dashboard.html │
                    └──────────────────┘
```

### 3.3 日志级别标准

| 级别 | 使用场景 |
|------|----------|
| DEBUG | 详细调试信息、变量值 |
| INFO | 关键业务事件（任务创建、完成） |
| WARNING | 潜在问题、降级操作 |
| ERROR | 错误和异常 |

---

## 4. FR-12: 配置标准化

### 4.1 配置层次

```
环境变量 > config/settings.yaml > 代码默认值
```

### 4.2 配置文件结构

```yaml
# config/settings.yaml
database:
  path: ${AI_AS_ME_DB:data/tasks.db}
  pool_size: 5

rag:
  persist_dir: ${AI_AS_ME_RAG_DIR:~/.ai-as-me/rag}
  model: all-MiniLM-L6-v2

api:
  host: 0.0.0.0
  port: 8000
  cors_origins: ["*"]
```

### 4.3 API文档增强

```python
app = FastAPI(
    title="AI-as-Me Dashboard",
    description="自进化AI数字分身系统API",
    version="2.3.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.post("/api/tasks", response_model=TaskResponse,
          summary="创建任务",
          description="创建新任务并自动选择执行工具")
async def create_task(task: TaskCreate):
    """
    创建新任务
    
    - **description**: 任务描述
    - **tool**: 可选，指定执行工具
    """
    pass
```

---

## 5. FR-13: 测试架构

### 5.1 性能测试框架

```python
# tests/performance/test_benchmark.py
import pytest

@pytest.mark.benchmark(group="api")
def test_task_list_performance(benchmark, client):
    result = benchmark(client.get, "/api/tasks")
    assert result.status_code == 200

@pytest.mark.benchmark(group="rag")
def test_rag_retrieval_performance(benchmark, retriever):
    result = benchmark(retriever.retrieve, "test query")
    assert len(result) >= 0
```

### 5.2 健康检查增强

```python
@app.get("/api/health/detailed")
async def detailed_health():
    return {
        "status": "healthy",
        "components": {
            "database": check_db_connection(),
            "rag": check_rag_service(),
            "tools": check_tool_availability()
        },
        "timestamp": datetime.now().isoformat()
    }
```

---

## 6. FR-14: 数据模型扩展

### 6.1 任务优先级

```sql
ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'P2';
```

```python
class TaskPriority(Enum):
    P1 = "P1"  # 紧急
    P2 = "P2"  # 正常
    P3 = "P3"  # 低优先级
```

### 6.2 执行历史API

```python
@app.get("/api/tasks/{task_id}/history")
async def get_task_history(task_id: str) -> list[ExecutionRecord]:
    """获取任务执行历史"""
    pass
```

---

## 7. 技术决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 模板引擎 | Jinja2 | FastAPI原生支持 |
| 性能测试 | pytest-benchmark | 与现有测试集成 |
| 配置管理 | PyYAML + envvar | 简单灵活 |

---

**Document Status:** Ready for Implementation Readiness Check
