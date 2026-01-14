"""Epic 7 单元测试"""
import pytest
from datetime import datetime
from pathlib import Path
from ai_as_me.rag.retriever import (
    TaskExperience, VectorStore, ExperienceRetriever, FeedbackLearner
)


# Story 7.1 & 7.2 测试
class TestVectorStore:
    @pytest.fixture
    def store(self, tmp_path):
        return VectorStore(persist_dir=str(tmp_path / "rag"))
    
    def test_add_experience(self, store):
        exp = TaskExperience(
            task_id="task-1",
            description="写一个排序算法",
            tool_used="claude_code",
            result_summary="成功实现了快速排序",
            success=True,
            user_feedback=None,
            created_at=datetime.now()
        )
        
        store.add(exp)
        # 验证添加成功（通过查询）
        results = store.query("排序算法", top_k=1)
        assert len(results) > 0
    
    def test_query_similar(self, store):
        # 添加多个经验
        for i in range(3):
            exp = TaskExperience(
                task_id=f"task-{i}",
                description=f"写代码任务 {i}",
                tool_used="claude_code",
                result_summary=f"结果 {i}",
                success=True,
                user_feedback=None,
                created_at=datetime.now()
            )
            store.add(exp)
        
        # 查询相似经验
        results = store.query("写代码", top_k=2)
        assert len(results) <= 2


# Story 7.3 测试
class TestExperienceRetriever:
    @pytest.fixture
    def retriever(self, tmp_path):
        return ExperienceRetriever(persist_dir=str(tmp_path / "rag"))
    
    def test_store_and_retrieve(self, retriever):
        # 存储经验
        exp = TaskExperience(
            task_id="task-1",
            description="实现二分查找算法",
            tool_used="claude_code",
            result_summary="成功实现",
            success=True,
            user_feedback=None,
            created_at=datetime.now()
        )
        retriever.store_experience(exp)
        
        # 检索
        results = retriever.retrieve("二分查找", top_k=1)
        assert len(results) > 0
    
    def test_success_filter(self, retriever):
        # 添加成功和失败的经验
        for i, success in enumerate([True, False, True]):
            exp = TaskExperience(
                task_id=f"task-{i}",
                description="测试任务",
                tool_used="claude_code",
                result_summary=f"结果 {i}",
                success=success,
                user_feedback=None,
                created_at=datetime.now()
            )
            retriever.store_experience(exp)
        
        # 只检索成功案例
        results = retriever.retrieve("测试", top_k=5, success_only=True)
        for r in results:
            assert r['metadata']['success'] == 'True'


# Story 7.4 测试
class TestContextBuilding:
    @pytest.fixture
    def retriever(self, tmp_path):
        return ExperienceRetriever(persist_dir=str(tmp_path / "rag"))
    
    def test_build_context(self, retriever):
        # 添加经验
        exp = TaskExperience(
            task_id="task-1",
            description="写代码",
            tool_used="claude_code",
            result_summary="这是一个很长的结果摘要" * 10,
            success=True,
            user_feedback=None,
            created_at=datetime.now()
        )
        retriever.store_experience(exp)
        
        # 检索并构建上下文
        results = retriever.retrieve("写代码", top_k=1)
        context = retriever.build_context(results, max_tokens=100)
        
        assert len(context) > 0
        assert "claude_code" in context
    
    def test_empty_context(self, retriever):
        context = retriever.build_context([], max_tokens=100)
        assert context == ""


# Story 7.5 测试
class TestFeedbackLearner:
    @pytest.fixture
    def learner(self, tmp_path):
        retriever = ExperienceRetriever(persist_dir=str(tmp_path / "rag"))
        return FeedbackLearner(retriever)
    
    def test_record_feedback(self, learner):
        learner.record_feedback("task-1", satisfied=True)
        weight = learner.get_weight("task-1")
        assert weight > 1.0
        
        learner.record_feedback("task-2", satisfied=False)
        weight = learner.get_weight("task-2")
        assert weight < 1.0
    
    def test_default_weight(self, learner):
        weight = learner.get_weight("unknown-task")
        assert weight == 1.0
