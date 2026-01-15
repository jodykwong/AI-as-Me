"""Dashboard 性能验证测试."""
import pytest
import time
from fastapi.testclient import TestClient
from concurrent.futures import ThreadPoolExecutor


@pytest.fixture
def client():
    from ai_as_me.dashboard.app import app
    return TestClient(app)


class TestAPIPerformance:
    """API 性能测试."""
    
    def test_health_endpoint_performance(self, client, benchmark):
        """健康检查端点性能."""
        def health_check():
            return client.get("/health")
        
        result = benchmark(health_check)
        assert result.status_code == 200
        # 目标: <10ms
    
    def test_inspirations_list_performance(self, client, benchmark):
        """灵感列表端点性能."""
        def list_inspirations():
            return client.get("/api/inspirations")
        
        result = benchmark(list_inspirations)
        assert result.status_code == 200
        # 目标: <50ms
    
    def test_rules_list_performance(self, client, benchmark):
        """规则列表端点性能."""
        def list_rules():
            return client.get("/api/rules")
        
        result = benchmark(list_rules)
        assert result.status_code == 200
        # 目标: <50ms
    
    def test_stats_query_performance(self, client, benchmark):
        """统计查询端点性能."""
        def get_stats():
            return client.get("/api/stats?days=7")
        
        result = benchmark(get_stats)
        assert result.status_code == 200
        # 目标: <100ms
    
    def test_logs_query_performance(self, client, benchmark):
        """日志查询端点性能."""
        def query_logs():
            return client.get("/api/logs?limit=10")
        
        result = benchmark(query_logs)
        assert result.status_code == 200
        # 目标: <100ms


class TestConcurrency:
    """并发测试."""
    
    def test_concurrent_health_checks(self, client):
        """并发健康检查."""
        def make_request():
            return client.get("/health")
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(50)]
            results = [f.result() for f in futures]
        
        assert all(r.status_code == 200 for r in results)
        assert len(results) == 50
    
    def test_concurrent_api_calls(self, client):
        """并发 API 调用."""
        endpoints = [
            "/api/inspirations",
            "/api/rules",
            "/api/stats?days=7",
            "/api/logs?limit=10"
        ]
        
        def make_request(endpoint):
            return client.get(endpoint)
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for _ in range(5):
                for endpoint in endpoints:
                    futures.append(executor.submit(make_request, endpoint))
            
            results = [f.result() for f in futures]
        
        assert all(r.status_code == 200 for r in results)
        assert len(results) == 20


class TestLoadCapacity:
    """负载容量测试."""
    
    def test_sustained_load(self, client):
        """持续负载测试 (10秒)."""
        start_time = time.time()
        request_count = 0
        errors = 0
        
        while time.time() - start_time < 10:
            try:
                response = client.get("/health")
                if response.status_code == 200:
                    request_count += 1
                else:
                    errors += 1
            except Exception:
                errors += 1
        
        # 目标: >100 req/s, 错误率 <1%
        rps = request_count / 10
        error_rate = errors / (request_count + errors) if request_count + errors > 0 else 0
        
        assert rps > 100, f"RPS too low: {rps:.2f}"
        assert error_rate < 0.01, f"Error rate too high: {error_rate:.2%}"
    
    def test_response_time_consistency(self, client):
        """响应时间一致性测试."""
        response_times = []
        
        for _ in range(100):
            start = time.time()
            response = client.get("/api/inspirations")
            duration = time.time() - start
            
            if response.status_code == 200:
                response_times.append(duration * 1000)  # ms
        
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        
        # 目标: 平均 <50ms, 最大 <200ms
        assert avg_time < 50, f"Average response time too high: {avg_time:.2f}ms"
        assert max_time < 200, f"Max response time too high: {max_time:.2f}ms"


class TestMemoryUsage:
    """内存使用测试."""
    
    def test_no_memory_leak(self, client):
        """检测内存泄漏."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # 执行 1000 次请求
        for _ in range(1000):
            client.get("/api/inspirations")
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # 目标: 内存增长 <50MB
        assert memory_increase < 50, f"Memory leak detected: +{memory_increase:.2f}MB"
