"""Evolution Flow Integration Tests - P0-2"""
import pytest
from pathlib import Path
import json
import shutil
from datetime import datetime


class TestEvolutionFlow:
    """端到端进化流程测试"""
    
    @pytest.fixture
    def test_dirs(self, tmp_path):
        """创建测试目录结构"""
        experience_dir = tmp_path / "experience"
        (experience_dir / "successes").mkdir(parents=True)
        (experience_dir / "failures").mkdir(parents=True)
        (experience_dir / "patterns").mkdir(parents=True)
        
        soul_dir = tmp_path / "soul"
        (soul_dir / "rules" / "core").mkdir(parents=True)
        (soul_dir / "rules" / "learned").mkdir(parents=True)
        
        logs_dir = tmp_path / "logs"
        logs_dir.mkdir(parents=True)
        
        return {
            "experience": experience_dir,
            "soul": soul_dir,
            "logs": logs_dir,
            "root": tmp_path
        }
    
    def test_experience_collector(self, test_dirs):
        """测试经验收集"""
        from src.ai_as_me.evolution.collector import ExperienceCollector
        
        collector = ExperienceCollector(test_dirs["experience"], None)
        
        # 模拟任务
        class MockTask:
            id = "test-001"
            description = "Test task"
            tool = "claude_code"
        
        exp = collector.collect(MockTask(), "Success result", success=True, duration=1.5)
        
        assert exp.task_id == "test-001"
        assert exp.success is True
        assert (test_dirs["experience"] / "successes" / "test-001.json").exists()
    
    def test_experience_collector_failure(self, test_dirs):
        """测试失败经验收集"""
        from src.ai_as_me.evolution.collector import ExperienceCollector
        
        collector = ExperienceCollector(test_dirs["experience"], None)
        
        class MockTask:
            id = "test-002"
            description = "Failed task"
            tool = "opencode"
        
        exp = collector.collect(MockTask(), "Error occurred", success=False)
        
        assert exp.success is False
        assert (test_dirs["experience"] / "failures" / "test-002.json").exists()
    
    def test_get_recent_experiences(self, test_dirs):
        """测试获取最近经验"""
        from src.ai_as_me.evolution.collector import ExperienceCollector
        
        collector = ExperienceCollector(test_dirs["experience"], None)
        
        # 创建多个经验
        for i in range(5):
            class MockTask:
                id = f"test-{i:03d}"
                description = f"Task {i}"
                tool = "claude_code"
            collector.collect(MockTask(), f"Result {i}", success=True)
        
        recent = collector.get_recent(limit=3)
        assert len(recent) == 3
    
    def test_soul_writer(self, test_dirs):
        """测试规则写入"""
        from src.ai_as_me.evolution.writer import SoulWriter
        from src.ai_as_me.evolution.generator import GeneratedRule
        from datetime import datetime
        
        writer = SoulWriter(test_dirs["soul"])
        
        rule = GeneratedRule(
            rule_id="rule-001",
            category="Technical",
            content="当遇到架构问题时，优先使用 BMad Method",
            source_pattern="pattern-001",
            confidence=0.85,
            created_at=datetime.now(),
            metadata={}
        )
        
        path = writer.write_rule(rule)
        
        assert path.exists()
        assert "Technical" in path.name
        assert writer.count_rules() == 1
    
    def test_evolution_logger(self, test_dirs):
        """测试进化日志"""
        from src.ai_as_me.evolution.logger import EvolutionLogger
        
        logger = EvolutionLogger(test_dirs["logs"] / "evolution.jsonl")
        
        class MockExp:
            task_id = "test-log-001"
        
        logger.log(MockExp(), [], [])
        
        assert (test_dirs["logs"] / "evolution.jsonl").exists()
        
        stats = logger.get_stats(days=7)
        assert stats["total_experiences"] == 1
    
    def test_skill_loader(self):
        """测试 Skills 加载"""
        from src.ai_as_me.skills.loader import SkillLoader
        
        loader = SkillLoader(Path("skills"))
        skills = loader.list_skills()
        
        assert "bmad" in skills
        
        bmad = loader.load_skill("bmad")
        assert bmad is not None
        assert bmad.name == "bmad"
        assert len(bmad.triggers) > 0
    
    def test_soul_loader_rules(self):
        """测试 Soul 规则加载"""
        from src.ai_as_me.soul.loader import SoulLoader
        
        loader = SoulLoader(Path("soul"))
        rules = loader.load_all_rules()
        
        assert len(rules) > 0
        assert "Core Rule" in rules


class TestEvolutionEngine:
    """进化引擎集成测试"""
    
    @pytest.fixture
    def mock_llm(self):
        """模拟 LLM 客户端"""
        class MockLLM:
            def chat(self, messages, **kwargs):
                return "[Technical] 当遇到复杂任务时，分解为小步骤 | 置信度: 0.8"
        return MockLLM()
    
    def test_evolution_engine_init(self, tmp_path, mock_llm):
        """测试进化引擎初始化"""
        from src.ai_as_me.evolution.engine import EvolutionEngine
        
        # 创建目录
        (tmp_path / "experience" / "successes").mkdir(parents=True)
        (tmp_path / "experience" / "failures").mkdir(parents=True)
        (tmp_path / "experience" / "patterns").mkdir(parents=True)
        (tmp_path / "soul" / "rules" / "learned").mkdir(parents=True)
        
        engine = EvolutionEngine({
            'experience_dir': str(tmp_path / "experience"),
            'soul_dir': str(tmp_path / "soul"),
            'llm_client': mock_llm,
            'log_path': str(tmp_path / "logs" / "evolution.jsonl")
        })
        
        assert engine.collector is not None
        assert engine.recognizer is not None
        assert engine.generator is not None
        assert engine.writer is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
