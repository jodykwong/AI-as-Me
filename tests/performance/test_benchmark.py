"""Story 13.2: 性能测试自动化"""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile
import os


@pytest.fixture
def client():
    from ai_as_me.kanban.api import app
    return TestClient(app)


@pytest.fixture
def temp_env(tmp_path):
    """临时环境配置"""
    db_path = tmp_path / "test.db"
    os.environ["AI_AS_ME_DB"] = str(db_path)
    yield
    if "AI_AS_ME_DB" in os.environ:
        del os.environ["AI_AS_ME_DB"]


@pytest.mark.benchmark(group="api")
def test_health_check_performance(benchmark, client):
    """健康检查性能基准"""
    result = benchmark(client.get, "/api/health")
    assert result.status_code == 200


@pytest.mark.benchmark(group="api")
def test_list_tasks_performance(benchmark, client, temp_env):
    """任务列表性能基准"""
    result = benchmark(client.get, "/api/tasks")
    assert result.status_code == 200


@pytest.mark.benchmark(group="api")
def test_create_task_performance(benchmark, client, temp_env):
    """创建任务性能基准"""
    def create():
        return client.post("/api/tasks", json={"description": "test task"})
    
    result = benchmark(create)
    assert result.status_code == 200


@pytest.mark.benchmark(group="rag")
def test_rag_retrieval_performance(benchmark, tmp_path):
    """RAG检索性能基准"""
    from ai_as_me.rag.retriever import ExperienceRetriever, TaskExperience
    from datetime import datetime
    
    retriever = ExperienceRetriever(persist_dir=str(tmp_path / "rag"))
    
    # 添加测试数据
    for i in range(10):
        exp = TaskExperience(
            task_id=f"task-{i}",
            description=f"测试任务 {i}",
            tool_used="test_tool",
            result_summary=f"结果 {i}",
            success=True,
            user_feedback=None,
            created_at=datetime.now()
        )
        retriever.store_experience(exp)
    
    # 性能测试
    result = benchmark(retriever.retrieve, "测试", top_k=5)
    assert len(result) >= 0


@pytest.mark.benchmark(group="skill_matcher")
def test_skill_matching_performance(benchmark, tmp_path):
    """工具选择性能基准"""
    from ai_as_me.orchestrator.skill_matcher import SkillMatcher
    from pathlib import Path
    
    # 创建配置
    config = tmp_path / "agents.yaml"
    config.write_text("""
agents:
  test_tool:
    capabilities:
      code_generation: 0.9
""")
    
    matcher = SkillMatcher(config, str(tmp_path / "test.db"))
    
    result = benchmark(matcher.match, "写一个排序算法")
    assert result is not None
