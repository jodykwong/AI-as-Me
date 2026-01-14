"""Epic 6 集成测试"""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile
import os


@pytest.fixture
def test_env(tmp_path):
    """设置测试环境"""
    # 创建临时数据库
    db_path = tmp_path / "test.db"
    config_path = tmp_path / "agents.yaml"
    
    # 创建配置文件
    config_path.write_text("""
agents:
  claude_code:
    capabilities:
      code_generation: 0.9
""")
    
    # 设置环境变量
    os.environ["DB_PATH"] = str(db_path)
    os.environ["CONFIG_PATH"] = str(config_path)
    
    yield {"db_path": db_path, "config_path": config_path}


@pytest.fixture
def client():
    """创建测试客户端"""
    from ai_as_me.kanban.api import app
    return TestClient(app)


# Story 6.1 测试
def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# Story 6.2 测试
def test_list_tasks(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Story 6.3 测试
def test_create_task(client):
    response = client.post("/api/tasks", json={
        "description": "测试任务",
        "tool": "claude_code"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "测试任务"
    assert data["tool"] == "claude_code"
    assert data["status"] == "inbox"


# Story 6.4 测试
def test_update_task_status(client):
    # 先创建任务
    create_response = client.post("/api/tasks", json={
        "description": "测试任务"
    })
    task_id = create_response.json()["id"]
    
    # 更新状态
    response = client.put(f"/api/tasks/{task_id}/status?status=doing")
    assert response.status_code == 200
    assert response.json()["status"] == "doing"


# Story 6.5 测试 (Story 13.3: 更新为新格式)
def test_system_health(client):
    response = client.get("/api/system/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "components" in data
    assert "tools" in data["components"]


# Story 6.2 测试
def test_dashboard_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "AI-as-Me Dashboard" in response.text
