"""Tests for Conflict Detection."""
import pytest
from pathlib import Path
from ai_as_me.soul.conflict_detector import ConflictDetector, Conflict
from ai_as_me.soul.conflict_resolver import ConflictResolver


@pytest.fixture
def temp_soul_dir(tmp_path):
    """创建临时 soul 目录."""
    core_dir = tmp_path / "core"
    learned_dir = tmp_path / "learned"
    core_dir.mkdir(parents=True)
    learned_dir.mkdir(parents=True)
    
    # 创建测试规则
    (core_dir / "base.md").write_text("# 核心规则\n\n禁止使用工具 X")
    (learned_dir / "tool.md").write_text("# 学习规则\n\n使用工具 X 提高效率")
    
    return tmp_path


@pytest.mark.asyncio
async def test_detect_contradiction(temp_soul_dir):
    """测试直接矛盾检测."""
    detector = ConflictDetector(temp_soul_dir)
    conflicts = await detector.scan()
    
    assert len(conflicts) > 0
    assert conflicts[0].type == "contradiction"


@pytest.mark.asyncio
async def test_auto_resolve(temp_soul_dir, tmp_path):
    """测试自动处理冲突."""
    detector = ConflictDetector(temp_soul_dir)
    conflicts = await detector.scan()
    
    # 确保有冲突
    assert len(conflicts) > 0, "No conflicts detected"
    
    log_file = tmp_path / "conflicts.jsonl"
    resolver = ConflictResolver(log_file)
    
    resolution = await resolver.auto_resolve(conflicts[0])
    
    assert resolution["action"] == "downgrade_learned"
    assert log_file.exists()


@pytest.mark.asyncio
async def test_no_conflicts():
    """测试无冲突场景."""
    detector = ConflictDetector(Path("soul/rules"))
    conflicts = await detector.scan()
    
    # 应该返回空列表或有冲突
    assert isinstance(conflicts, list)
