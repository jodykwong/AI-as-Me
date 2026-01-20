"""Agentic RAG 检索模块 - Epic 7"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Any
from functools import lru_cache  # Story 9.2: 缓存支持
import os
import chromadb
from sentence_transformers import SentenceTransformer


# Story 7.2: 任务经验数据模型
@dataclass
class TaskExperience:
    task_id: str
    description: str
    tool_used: str
    result_summary: str
    success: bool
    user_feedback: Optional[str]
    created_at: datetime

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "description": self.description,
            "tool_used": self.tool_used,
            "result_summary": self.result_summary,
            "success": self.success,
            "user_feedback": self.user_feedback,
            "created_at": self.created_at.isoformat(),
        }


# Story 7.1: 向量存储
class VectorStore:
    """ChromaDB 向量存储"""

    # Story 9.3: 类级别的模型缓存
    _model_cache: Optional[SentenceTransformer] = None
    _model_lock: Optional[Any] = None

    def __init__(self, persist_dir: Optional[str] = None) -> None:
        if persist_dir is None:
            persist_dir = str(Path.home() / ".ai-as-me" / "rag")

        Path(persist_dir).mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection("experiences")

        # Story 9.3: 使用预加载的模型
        self.embedder = self._get_or_load_model()

    @classmethod
    def _get_or_load_model(cls):
        """获取或加载嵌入模型（单例模式）"""
        if cls._model_cache is None:
            if cls._model_lock is None:
                import threading

                cls._model_lock = threading.Lock()

            with cls._model_lock:
                if cls._model_cache is None:
                    cls._model_cache = SentenceTransformer("all-MiniLM-L6-v2")

        return cls._model_cache

    @classmethod
    def warmup(cls):
        """预热：预加载模型"""
        cls._get_or_load_model()

    def add(self, experience: TaskExperience) -> None:
        """添加任务经验"""
        embedding = self.embedder.encode(experience.description)

        # H3 修复: 使用 upsert 避免重复 ID 错误
        try:
            self.collection.add(
                ids=[experience.task_id],
                embeddings=[embedding.tolist()],
                metadatas=[
                    {
                        "tool": experience.tool_used,
                        "success": str(experience.success),
                        "created_at": experience.created_at.isoformat(),
                    }
                ],
                documents=[experience.result_summary],
            )
        except Exception:
            # 如果 ID 已存在，更新记录
            self.collection.update(
                ids=[experience.task_id],
                embeddings=[embedding.tolist()],
                metadatas=[
                    {
                        "tool": experience.tool_used,
                        "success": str(experience.success),
                        "created_at": experience.created_at.isoformat(),
                    }
                ],
                documents=[experience.result_summary],
            )

    def query(self, text: str, top_k: int = 5) -> list[dict]:
        """查询相似经验"""
        embedding = self.embedder.encode(text)

        results = self.collection.query(
            query_embeddings=[embedding.tolist()], n_results=top_k
        )

        return self._format_results(results)

    def _format_results(self, results: dict) -> list[dict]:
        """格式化查询结果"""
        formatted = []

        if not results["ids"] or not results["ids"][0]:
            return formatted

        for i in range(len(results["ids"][0])):
            formatted.append(
                {
                    "id": results["ids"][0][i],
                    "document": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": (
                        results["distances"][0][i] if "distances" in results else None
                    ),
                }
            )

        return formatted


# Story 7.3 & 7.4: 经验检索器
class ExperienceRetriever:
    """任务经验检索器"""

    def __init__(self, persist_dir: str = None):
        self.store = VectorStore(persist_dir)
        # Story 9.2: 缓存配置
        self._cache_size = 128

    def store_experience(self, exp: TaskExperience) -> None:
        """存储任务经验"""
        self.store.add(exp)
        # 清除缓存（新数据加入）
        self._retrieve_cached.cache_clear()

    @lru_cache(maxsize=128)  # Story 9.2: LRU 缓存检索结果
    def _retrieve_cached(self, query: str, top_k: int, success_only: bool) -> tuple:
        """缓存的检索方法（返回 tuple 以支持缓存）"""
        results = self.store.query(query, top_k * 2)

        if success_only:
            results = [r for r in results if r["metadata"].get("success") == "True"]

        # 转为 tuple 以支持缓存
        return tuple(tuple(r.items()) for r in results[:top_k])

    def retrieve(
        self, query: str, top_k: int = 5, success_only: bool = True
    ) -> list[dict]:
        """检索相似经验（带缓存）"""
        # 使用缓存方法
        cached_results = self._retrieve_cached(query, top_k, success_only)

        # 转回 dict 格式
        return [dict(r) for r in cached_results]

    def build_context(self, experiences: list[dict], max_tokens: int = 2000) -> str:
        """构建注入上下文"""
        if not experiences:
            return ""

        context_parts = []
        total_len = 0

        for exp in experiences:
            doc = exp.get("document", "")
            tool = exp.get("metadata", {}).get("tool", "unknown")

            part = f"[历史经验 - {tool}]\n{doc[:200]}\n"

            # 粗略估算 token (1 token ≈ 4 chars)
            if total_len + len(part) > max_tokens * 4:
                break

            context_parts.append(part)
            total_len += len(part)

        return "\n".join(context_parts)


# Story 7.5: 反馈学习 (Story 8.2: 持久化版本, M3 修复: 环境变量)
class FeedbackLearner:
    """用户反馈学习器 - 持久化版本"""

    def __init__(self, retriever: ExperienceRetriever, db_path: str = None):
        self.retriever = retriever
        self.db_path = db_path or os.getenv(
            "AI_AS_ME_FEEDBACK_DB", str(Path.home() / ".ai-as-me" / "feedback.db")
        )
        self._ensure_db()
        self.feedback_weights = self._load_weights()

    def _ensure_db(self):
        """确保数据库表存在"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        import sqlite3

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS feedback_weights (
                    task_id TEXT PRIMARY KEY,
                    weight REAL NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

    def _load_weights(self) -> dict:
        """从数据库加载权重"""
        import sqlite3

        weights = {}

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT task_id, weight FROM feedback_weights")
            for row in cursor:
                weights[row[0]] = row[1]

        return weights

    def record_feedback(self, task_id: str, satisfied: bool):
        """记录用户反馈并持久化"""
        import sqlite3

        adjustment = 0.1 if satisfied else -0.1
        new_weight = self.feedback_weights.get(task_id, 0) + adjustment
        self.feedback_weights[task_id] = new_weight

        # 持久化到数据库
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO feedback_weights (task_id, weight, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """,
                (task_id, new_weight),
            )

    def get_weight(self, task_id: str) -> float:
        """获取任务权重"""
        return 1.0 + self.feedback_weights.get(task_id, 0)
