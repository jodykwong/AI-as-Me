# Story 5.4: 智能工具选择算法

**Epic:** Epic 5 - 多工具智能选择
**Status:** ready-for-dev
**Created:** 2026-01-14T08:06:00+08:00

---

## User Story

As a 技术型独立AI创业者,
I want 系统综合任务类型、工具能力和历史成功率选择最优工具,
So that 我不需要每次手动指定工具。

---

## Acceptance Criteria

- [ ] **AC1:** 用户创建任务未指定工具时，系统自动选择
- [ ] **AC2:** 评分公式: `score = capability * 0.5 + history * 0.3 + availability * 0.2`
- [ ] **AC3:** 返回最高分工具
- [ ] **AC4:** 选择决策记录到日志
- [ ] **AC5:** 工具选择准确率 >80%

---

## Dev Checklist

### 1. 实现 SkillMatcher 主类

**File:** `src/ai_as_me/orchestrator/skill_matcher.py`

```python
import logging

logger = logging.getLogger(__name__)

class SkillMatcher:
    def __init__(self, config_path: Path, db_path: str):
        self.analyzer = TaskAnalyzer()
        self.registry = ToolRegistry(config_path)
        self.history = HistoryTracker(db_path)
    
    def match(self, task_description: str) -> str:
        """返回最匹配的工具名称"""
        # 1. 分析任务类型
        task_type = self.analyzer.analyze(task_description)
        
        # 2. 计算所有工具的评分
        scores = self._calculate_scores(task_type)
        
        # 3. 选择最高分工具
        best_tool = max(scores, key=scores.get)
        
        # 4. 记录决策
        logger.info(
            f"Tool selection: task_type={task_type.value}, "
            f"selected={best_tool}, scores={scores}"
        )
        
        return best_tool
    
    def _calculate_scores(self, task_type: TaskType) -> dict[str, float]:
        """计算所有工具的评分"""
        scores = {}
        
        for tool in self.registry.get_available():
            # 能力评分 (50%)
            cap_score = self.registry.get_capability(tool, task_type)
            
            # 历史成功率 (30%)
            hist_score = self.history.get_success_rate(tool, task_type)
            
            # 可用性 (20%) - 简化为 1.0
            avail_score = 1.0
            
            # 综合评分
            scores[tool] = (
                cap_score * 0.5 + 
                hist_score * 0.3 + 
                avail_score * 0.2
            )
        
        return scores
    
    def rank(self, task_description: str) -> list[tuple[str, float]]:
        """返回工具排名和分数"""
        task_type = self.analyzer.analyze(task_description)
        scores = self._calculate_scores(task_type)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

### 2. 集成到任务创建流程

**File:** `src/ai_as_me/orchestrator/scheduler.py` (修改)

```python
class TaskScheduler:
    def __init__(self, db_path: str, config_path: Path):
        # ... 现有初始化 ...
        self.skill_matcher = SkillMatcher(config_path, db_path)
    
    def create_task(self, description: str, tool: str = None) -> str:
        """创建任务，自动选择工具"""
        # 如果未指定工具，自动选择
        if tool is None:
            tool = self.skill_matcher.match(description)
        
        # ... 创建任务逻辑 ...
        task_id = self._save_task(description, tool)
        return task_id
```

### 3. 添加单元测试

**File:** `tests/unit/test_skill_matcher.py`

```python
def test_skill_matcher():
    matcher = SkillMatcher(
        config_path=Path("config/agents.yaml"),
        db_path=":memory:"
    )
    
    # 测试代码生成任务
    tool = matcher.match("写一个 Python 排序算法")
    assert tool == "claude_code"  # 能力最强
    
    # 测试调试任务
    tool = matcher.match("修复这个内存泄漏 bug")
    assert tool == "opencode"  # debug 能力最强
    
    # 测试排名
    ranking = matcher.rank("写 API 文档")
    assert len(ranking) == 4
    assert ranking[0][0] == "gemini_cli"  # documentation 最强
```

### 4. 添加日志配置

**File:** `src/ai_as_me/utils/logging.py` (确保存在)

```python
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
```

---

## Files to Create/Modify

| 文件 | 操作 |
|------|------|
| `src/ai_as_me/orchestrator/skill_matcher.py` | 修改 (添加主类) |
| `src/ai_as_me/orchestrator/scheduler.py` | 修改 (集成) |
| `tests/unit/test_skill_matcher.py` | 修改 (添加测试) |

---

## Dependencies

- Story 5.1 (TaskAnalyzer)
- Story 5.2 (ToolRegistry)
- Story 5.3 (HistoryTracker)

---

## Definition of Done

- [ ] SkillMatcher 类已实现
- [ ] 评分算法正确实现
- [ ] 集成到任务创建流程
- [ ] 选择决策记录到日志
- [ ] 单元测试通过
- [ ] 准确率验证 >80%
