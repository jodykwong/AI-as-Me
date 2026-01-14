# Story 5.1: 任务类型识别

**Epic:** Epic 5 - 多工具智能选择
**Status:** ready-for-dev
**Created:** 2026-01-14T08:04:00+08:00

---

## User Story

As a 技术型独立AI创业者,
I want 系统能够自动识别任务类型（代码生成/审查/文档/架构/调试）,
So that 系统可以基于任务类型选择合适的工具。

---

## Acceptance Criteria

- [ ] **AC1:** Given 任务描述 "写一个 Python 函数计算斐波那契数列", When 系统分析, Then 识别为 `code_generation`
- [ ] **AC2:** Given 任务描述 "审查这段代码的安全性", When 系统分析, Then 识别为 `code_review`
- [ ] **AC3:** Given 任务描述 "写一份 API 文档", When 系统分析, Then 识别为 `documentation`
- [ ] **AC4:** Given 任务描述 "设计微服务架构", When 系统分析, Then 识别为 `architecture`
- [ ] **AC5:** Given 任务描述 "修复这个 bug", When 系统分析, Then 识别为 `debug`
- [ ] **AC6:** 识别准确率 >80%

---

## Dev Checklist

### 1. 创建任务类型枚举

**File:** `src/ai_as_me/orchestrator/skill_matcher.py`

```python
from enum import Enum

class TaskType(Enum):
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    DOCUMENTATION = "documentation"
    ARCHITECTURE = "architecture"
    DEBUG = "debug"
    UNKNOWN = "unknown"
```

### 2. 实现 TaskAnalyzer 类

**File:** `src/ai_as_me/orchestrator/skill_matcher.py`

```python
class TaskAnalyzer:
    """基于关键词匹配的任务类型识别器"""
    
    KEYWORDS = {
        TaskType.CODE_GENERATION: [
            "写", "创建", "实现", "生成", "开发", "编写",
            "write", "create", "implement", "generate", "develop"
        ],
        TaskType.CODE_REVIEW: [
            "审查", "检查", "review", "check", "分析代码", "代码质量"
        ],
        TaskType.DOCUMENTATION: [
            "文档", "说明", "readme", "doc", "注释", "document"
        ],
        TaskType.ARCHITECTURE: [
            "架构", "设计", "architecture", "design", "系统设计", "模块"
        ],
        TaskType.DEBUG: [
            "修复", "bug", "fix", "调试", "debug", "错误", "问题"
        ],
    }
    
    def analyze(self, description: str) -> TaskType:
        """分析任务描述，返回任务类型"""
        desc_lower = description.lower()
        scores = {t: 0 for t in TaskType if t != TaskType.UNKNOWN}
        
        for task_type, keywords in self.KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in desc_lower:
                    scores[task_type] += 1
        
        if max(scores.values()) == 0:
            return TaskType.UNKNOWN
        
        return max(scores, key=scores.get)
```

### 3. 添加单元测试

**File:** `tests/unit/test_skill_matcher.py`

```python
import pytest
from ai_as_me.orchestrator.skill_matcher import TaskAnalyzer, TaskType

@pytest.fixture
def analyzer():
    return TaskAnalyzer()

def test_code_generation(analyzer):
    assert analyzer.analyze("写一个 Python 函数计算斐波那契数列") == TaskType.CODE_GENERATION

def test_code_review(analyzer):
    assert analyzer.analyze("审查这段代码的安全性") == TaskType.CODE_REVIEW

def test_documentation(analyzer):
    assert analyzer.analyze("写一份 API 文档") == TaskType.DOCUMENTATION

def test_architecture(analyzer):
    assert analyzer.analyze("设计微服务架构") == TaskType.ARCHITECTURE

def test_debug(analyzer):
    assert analyzer.analyze("修复这个 bug") == TaskType.DEBUG
```

### 4. 验证步骤

```bash
# 运行测试
pytest tests/unit/test_skill_matcher.py -v

# 手动验证
python -c "
from ai_as_me.orchestrator.skill_matcher import TaskAnalyzer, TaskType
a = TaskAnalyzer()
print(a.analyze('写一个排序算法'))  # CODE_GENERATION
print(a.analyze('review this PR'))   # CODE_REVIEW
"
```

---

## Files to Create/Modify

| 文件 | 操作 |
|------|------|
| `src/ai_as_me/orchestrator/skill_matcher.py` | 创建 |
| `tests/unit/test_skill_matcher.py` | 创建 |

---

## Dependencies

- 无外部依赖
- 无前置 Story

---

## Definition of Done

- [ ] TaskType 枚举已创建
- [ ] TaskAnalyzer 类已实现
- [ ] 5 种任务类型均可识别
- [ ] 单元测试通过
- [ ] 代码无 lint 错误
