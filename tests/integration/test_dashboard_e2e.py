"""Dashboard 集成测试 - E2E 流程"""
import pytest
from fastapi.testclient import TestClient
import time


@pytest.fixture
def client():
    from ai_as_me.dashboard.app import app
    return TestClient(app)


class TestDashboardE2E:
    """Dashboard 端到端测试"""
    
    def test_complete_workflow(self, client):
        """测试完整工作流：添加灵感 -> 查看统计 -> 查询日志"""
        
        # 1. 添加灵感
        inspiration = {
            "content": "E2E测试灵感",
            "priority": "high",
            "tags": ["e2e", "test"]
        }
        response = client.post("/api/inspirations", json=inspiration)
        assert response.status_code in [200, 201]
        
        # 2. 查看统计
        response = client.get("/api/stats?days=1")
        assert response.status_code == 200
        
        # 3. 查询日志
        response = client.get("/api/logs?limit=5")
        assert response.status_code == 200
    
    def test_page_navigation(self, client):
        """测试页面导航"""
        pages = ["/", "/inspirations.html", "/rules.html", "/stats.html"]
        
        for page in pages:
            response = client.get(page)
            assert response.status_code == 200
            assert "text/html" in response.headers.get("content-type", "")
    
    def test_api_error_handling(self, client):
        """测试 API 错误处理"""
        
        # 无效的规则 ID
        response = client.get("/api/rules/invalid-id-999")
        assert response.status_code in [404, 400]
        
        # 无效的日志查询参数
        response = client.get("/api/logs?limit=-1")
        assert response.status_code in [400, 422]


class TestPerformance:
    """性能测试"""
    
    def test_api_response_time(self, client):
        """测试 API 响应时间"""
        endpoints = [
            "/api/inspirations",
            "/api/rules",
            "/api/stats?days=7",
            "/api/logs?limit=10"
        ]
        
        for endpoint in endpoints:
            start = time.time()
            response = client.get(endpoint)
            duration = time.time() - start
            
            assert response.status_code == 200
            assert duration < 1.0, f"{endpoint} 响应时间过长: {duration:.2f}s"
    
    def test_concurrent_requests(self, client):
        """测试并发请求"""
        import concurrent.futures
        
        def make_request():
            return client.get("/api/stats?days=7")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [f.result() for f in futures]
        
        assert all(r.status_code == 200 for r in results)
