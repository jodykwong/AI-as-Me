"""Epic 5 单元测试"""
import pytest
import sqlite3
from pathlib import Path
from ai_as_me.orchestrator.skill_matcher import (
    TaskType, TaskAnalyzer, ToolRegistry, HistoryTracker, SkillMatcher
)


# Story 5.1 测试
class TestTaskAnalyzer:
    @pytest.fixture
    def analyzer(self):
        return TaskAnalyzer()
    
    def test_code_generation(self, analyzer):
        assert analyzer.analyze("写一个 Python 函数计算斐波那契数列") == TaskType.CODE_GENERATION
        assert analyzer.analyze("create a sorting algorithm") == TaskType.CODE_GENERATION
    
    def test_code_review(self, analyzer):
        assert analyzer.analyze("审查这段代码的安全性") == TaskType.CODE_REVIEW
        assert analyzer.analyze("review this PR") == TaskType.CODE_REVIEW
    
    def test_documentation(self, analyzer):
        assert analyzer.analyze("写一份 API 文档") == TaskType.DOCUMENTATION
        assert analyzer.analyze("document this module") == TaskType.DOCUMENTATION
    
    def test_architecture(self, analyzer):
        assert analyzer.analyze("设计微服务架构") == TaskType.ARCHITECTURE
        assert analyzer.analyze("design system architecture") == TaskType.ARCHITECTURE
    
    def test_debug(self, analyzer):
        assert analyzer.analyze("修复这个 bug") == TaskType.DEBUG
        assert analyzer.analyze("fix memory leak") == TaskType.DEBUG


# Story 5.2 测试
class TestToolRegistry:
    @pytest.fixture
    def config_file(self, tmp_path):
        config = tmp_path / "agents.yaml"
        config.write_text("""
agents:
  claude_code:
    capabilities:
      code_generation: 0.9
      code_review: 0.9
  opencode:
    capabilities:
      debug: 0.9
""")
        return config
    
    def test_load_tools(self, config_file):
        registry = ToolRegistry(config_file)
        assert "claude_code" in registry.get_available()
        assert "opencode" in registry.get_available()
        assert len(registry.get_available()) == 2
    
    def test_get_capability(self, config_file):
        registry = ToolRegistry(config_file)
        cap = registry.get_capability("claude_code", TaskType.CODE_GENERATION)
        assert cap == 0.9
        
        cap = registry.get_capability("opencode", TaskType.DEBUG)
        assert cap == 0.9
    
    def test_missing_tool(self, config_file):
        registry = ToolRegistry(config_file)
        cap = registry.get_capability("nonexistent", TaskType.CODE_GENERATION)
        assert cap == 0.0


# Story 5.3 测试
class TestHistoryTracker:
    @pytest.fixture
    def tracker(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        return HistoryTracker(db_path)
    
    def test_record_history(self, tracker):
        tracker.record("task-1", "claude_code", TaskType.CODE_GENERATION, True, 10.5)
        rate = tracker.get_success_rate("claude_code", TaskType.CODE_GENERATION)
        assert rate == 1.0
    
    def test_success_rate_calculation(self, tracker):
        tracker.record("task-1", "claude_code", TaskType.CODE_GENERATION, True)
        tracker.record("task-2", "claude_code", TaskType.CODE_GENERATION, True)
        tracker.record("task-3", "claude_code", TaskType.CODE_GENERATION, False)
        
        rate = tracker.get_success_rate("claude_code", TaskType.CODE_GENERATION)
        assert abs(rate - 2/3) < 0.01
    
    def test_no_history_default(self, tracker):
        rate = tracker.get_success_rate("unknown", TaskType.CODE_GENERATION)
        assert rate == 0.5  # 默认值


# Story 5.4 测试
class TestSkillMatcher:
    @pytest.fixture
    def matcher(self, tmp_path):
        config = tmp_path / "agents.yaml"
        config.write_text("""
agents:
  claude_code:
    capabilities:
      code_generation: 0.9
      debug: 0.7
  opencode:
    capabilities:
      code_generation: 0.7
      debug: 0.9
""")
        db_path = str(tmp_path / "test.db")
        return SkillMatcher(config, db_path)
    
    def test_match_code_generation(self, matcher):
        tool = matcher.match("写一个排序算法")
        assert tool == "claude_code"  # 能力最强
    
    def test_match_debug(self, matcher):
        tool = matcher.match("修复这个内存泄漏 bug")
        assert tool == "opencode"  # debug 能力最强
    
    def test_rank_tools(self, matcher):
        ranking = matcher.rank("实现一个排序算法")  # 更明确的代码生成任务
        assert len(ranking) == 2
        assert ranking[0][0] == "claude_code"  # 最高分
        assert ranking[0][1] >= ranking[1][1]  # 分数递减或相等
