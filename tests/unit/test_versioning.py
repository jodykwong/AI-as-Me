"""Tests for rule versioning."""
import pytest
from pathlib import Path
from ai_as_me.soul.versioning import RuleVersionManager


@pytest.fixture
def temp_vm(tmp_path):
    """创建临时版本管理器."""
    rules_dir = tmp_path / "rules"
    rules_dir.mkdir()
    return RuleVersionManager(rules_dir)


@pytest.fixture
def sample_rule(tmp_path):
    """创建示例规则."""
    rules_dir = tmp_path / "rules" / "learned"
    rules_dir.mkdir(parents=True)
    rule_file = rules_dir / "test_rule.md"
    rule_file.write_text("# Test Rule\nVersion 1 content")
    return rule_file


def test_save_version(temp_vm, sample_rule):
    """测试保存版本."""
    version = temp_vm.save_version(sample_rule, "initial")
    assert version == 1
    
    # 修改并保存
    sample_rule.write_text("# Test Rule\nVersion 2 content")
    version2 = temp_vm.save_version(sample_rule, "update")
    assert version2 == 2


def test_get_history(temp_vm, sample_rule):
    """测试获取历史."""
    temp_vm.save_version(sample_rule, "v1")
    temp_vm.save_version(sample_rule, "v2")
    
    history = temp_vm.get_history("test_rule")
    assert len(history) == 2
    assert history[0].reason == "v1"


def test_get_version(temp_vm, sample_rule):
    """测试获取特定版本."""
    temp_vm.save_version(sample_rule, "initial")
    sample_rule.write_text("Updated content")
    temp_vm.save_version(sample_rule, "update")
    
    v1_content = temp_vm.get_version("test_rule", 1)
    assert "Version 1" in v1_content


def test_diff(temp_vm, sample_rule):
    """测试版本对比."""
    temp_vm.save_version(sample_rule, "v1")
    sample_rule.write_text("New line added")
    temp_vm.save_version(sample_rule, "v2")
    
    diff = temp_vm.diff("test_rule", 1, 2)
    assert len(diff['added']) > 0


def test_rollback(temp_vm, sample_rule):
    """测试回滚."""
    temp_vm.save_version(sample_rule, "v1")
    original = sample_rule.read_text()
    
    sample_rule.write_text("Changed content")
    temp_vm.save_version(sample_rule, "v2")
    
    temp_vm.rollback(sample_rule, 1)
    assert sample_rule.read_text() == original
