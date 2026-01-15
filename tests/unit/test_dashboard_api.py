"""Dashboard API 单元测试"""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import json


@pytest.fixture
def client():
    """创建测试客户端"""
    from ai_as_me.dashboard.app import app
    return TestClient(app)


class TestInspirationAPI:
    """灵感池 API 测试"""
    
    def test_list_inspirations(self, client):
        response = client.get("/api/inspirations")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)  # 直接返回列表
    
    def test_add_inspiration(self, client):
        payload = {
            "content": "测试灵感",
            "priority": "medium",
            "tags": ["test"]
        }
        response = client.post("/api/inspirations", json=payload)
        assert response.status_code in [200, 201]
        data = response.json()
        assert "id" in data
        assert data["status"] == "created"


class TestRulesAPI:
    """规则管理 API 测试"""
    
    def test_list_rules(self, client):
        response = client.get("/api/rules")
        assert response.status_code == 200
        data = response.json()
        assert "core" in data or "learned" in data
    
    def test_get_rule_detail(self, client):
        response = client.get("/api/rules")
        if response.status_code == 200:
            data = response.json()
            if data.get("learned"):
                rule_id = data["learned"][0]["id"]
                detail_response = client.get(f"/api/rules/{rule_id}/history")
                assert detail_response.status_code in [200, 404]


class TestStatsAPI:
    """统计 API 测试"""
    
    def test_get_stats(self, client):
        response = client.get("/api/stats?days=7")
        assert response.status_code == 200
        data = response.json()
        assert "application_frequency" in data or "effectiveness_scores" in data


class TestLogsAPI:
    """日志 API 测试"""
    
    def test_query_logs(self, client):
        response = client.get("/api/logs?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "logs" in data
        assert isinstance(data["logs"], list)
    
    def test_export_logs(self, client):
        response = client.get("/api/logs/export?format=json")
        assert response.status_code == 200
