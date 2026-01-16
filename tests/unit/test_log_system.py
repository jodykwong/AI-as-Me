"""Tests for log_system module."""
import json
import logging
import pytest
from pathlib import Path
from ai_as_me.log_system import JSONFormatter, setup_logging, LogQuery, get_logger


@pytest.fixture(autouse=True)
def reset_logging():
    """Reset logging state before each test."""
    import ai_as_me.log_system.config as config_module
    config_module._configured = False
    
    root = logging.getLogger('ai_as_me')
    root.handlers.clear()
    root.setLevel(logging.NOTSET)


@pytest.fixture
def temp_log_dir(tmp_path):
    """临时日志目录."""
    return tmp_path / "logs"


def test_json_formatter():
    """测试 JSON 格式化器."""
    import logging
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Test message",
        args=(),
        exc_info=None
    )
    
    output = formatter.format(record)
    data = json.loads(output)
    
    assert data["level"] == "INFO"
    assert data["message"] == "Test message"
    assert "timestamp" in data


def test_setup_logging(temp_log_dir):
    """测试日志配置."""
    setup_logging(log_dir=temp_log_dir, level="INFO")
    
    root = logging.getLogger('ai_as_me')
    
    # Create log record (pytest intercepts logger.info())
    record = logging.LogRecord(
        name="ai_as_me.test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Test log",
        args=(),
        exc_info=None
    )
    
    # Emit directly to handlers
    for handler in root.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.emit(record)
            handler.flush()
    
    log_file = temp_log_dir / "agent.log"
    assert log_file.exists()
    
    content = log_file.read_text()
    assert "Test log" in content


def test_log_query(temp_log_dir):
    """测试日志查询."""
    # 创建测试日志
    log_file = temp_log_dir / "app.log"
    temp_log_dir.mkdir(parents=True)
    
    logs = [
        {"timestamp": "2026-01-15T20:00:00", "level": "INFO", "message": "Test 1"},
        {"timestamp": "2026-01-15T20:01:00", "level": "ERROR", "message": "Test 2"},
        {"timestamp": "2026-01-15T20:02:00", "level": "INFO", "message": "Test 3"},
    ]
    
    log_file.write_text("\n".join(json.dumps(log) for log in logs))
    
    # 测试查询
    query = LogQuery(log_file)
    
    # 级别筛选
    results = query.query(level="ERROR")
    assert len(results) == 1
    assert results[0]["message"] == "Test 2"
    
    # Tail
    tail_results = query.tail(n=2)
    assert len(tail_results) == 2
    assert tail_results[-1]["message"] == "Test 3"
