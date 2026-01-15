"""Tests for stats module."""
import json
from pathlib import Path
from datetime import datetime, timedelta
import pytest
from ai_as_me.stats import StatsCalculator, StatsVisualizer


@pytest.fixture
def temp_log(tmp_path):
    """创建临时日志文件."""
    log_file = tmp_path / "evolution.jsonl"
    now = datetime.now()
    
    entries = [
        {"timestamp": (now - timedelta(days=1)).isoformat(), "event": "rule_applied", "rule_id": "rule_001"},
        {"timestamp": (now - timedelta(days=2)).isoformat(), "event": "rule_applied", "rule_id": "rule_001"},
        {"timestamp": (now - timedelta(days=3)).isoformat(), "event": "rule_generated", "rule_id": "rule_001", "effectiveness_score": 0.8},
        {"timestamp": (now - timedelta(days=4)).isoformat(), "event": "pattern_recognized"},
    ]
    
    log_file.write_text("\n".join(json.dumps(e) for e in entries))
    return log_file


def test_application_frequency(temp_log):
    """测试规则应用频率计算."""
    calc = StatsCalculator(evolution_log=temp_log)
    freq = calc.calculate_application_frequency(days=7)
    
    assert "rule_001" in freq
    assert freq["rule_001"] > 0


def test_effectiveness_score(temp_log):
    """测试有效性评分."""
    calc = StatsCalculator(evolution_log=temp_log)
    scores = calc.calculate_effectiveness_score()
    
    assert "rule_001" in scores
    assert scores["rule_001"] == 0.8


def test_pattern_accuracy(temp_log):
    """测试模式识别准确率."""
    calc = StatsCalculator(evolution_log=temp_log)
    accuracy = calc.calculate_pattern_accuracy()
    
    assert accuracy == 1.0  # 1 pattern, 1 rule


def test_visualizer_ascii_bar():
    """测试 ASCII 条形图."""
    viz = StatsVisualizer()
    data = {"rule_001": 5.0, "rule_002": 3.0}
    output = viz.render_ascii_bar(data)
    
    assert "rule_001" in output
    assert "█" in output


def test_visualizer_ascii_trend():
    """测试有效性趋势."""
    viz = StatsVisualizer()
    scores = {"rule_001": 0.8, "rule_002": 0.6}
    output = viz.render_ascii_trend(scores)
    
    assert "rule_001" in output
    assert "★" in output
