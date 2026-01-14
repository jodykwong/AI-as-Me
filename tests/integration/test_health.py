"""Story 13.3: 健康检查增强测试"""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from ai_as_me.kanban.api import app
    return TestClient(app)


def test_basic_health_check(client):
    """基础健康检查"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data


def test_detailed_health_check(client):
    """详细健康检查"""
    response = client.get("/api/system/health")
    assert response.status_code == 200
    data = response.json()
    
    # 验证整体状态
    assert "status" in data
    assert data["status"] in ["healthy", "degraded"]
    
    # 验证组件状态
    assert "components" in data
    components = data["components"]
    
    # 数据库组件
    assert "database" in components
    assert "status" in components["database"]
    
    # RAG组件
    assert "rag" in components
    assert "status" in components["rag"]
    
    # 工具组件
    assert "tools" in components
    assert "status" in components["tools"]
    if components["tools"]["status"] == "healthy":
        assert "available" in components["tools"]
        assert "count" in components["tools"]


def test_health_check_timestamp(client):
    """验证时间戳格式"""
    response = client.get("/api/system/health")
    data = response.json()
    
    assert "timestamp" in data
    # 验证ISO格式
    from datetime import datetime
    datetime.fromisoformat(data["timestamp"])
