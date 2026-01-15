"""Experience Collector - Story 1.1"""
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json


@dataclass
class Experience:
    task_id: str
    description: str
    tool_used: str
    result: str
    success: bool
    duration: float
    timestamp: datetime
    
    def to_dict(self):
        d = asdict(self)
        d['timestamp'] = self.timestamp.isoformat()
        return d


class ExperienceCollector:
    def __init__(self, experience_dir: Path, vector_store=None):
        self.experience_dir = experience_dir
        self.vector_store = vector_store
        self.successes_dir = experience_dir / "successes"
        self.failures_dir = experience_dir / "failures"
        self.successes_dir.mkdir(parents=True, exist_ok=True)
        self.failures_dir.mkdir(parents=True, exist_ok=True)
    
    def collect(self, task, result: str, success: bool, duration: float = 0) -> Experience:
        """收集任务执行经验"""
        exp = Experience(
            task_id=getattr(task, 'id', str(task)),
            description=getattr(task, 'description', str(task))[:200],
            tool_used=getattr(task, 'tool', 'unknown'),
            result=result[:500],
            success=success,
            duration=duration,
            timestamp=datetime.now()
        )
        
        # 保存到文件
        target_dir = self.successes_dir if success else self.failures_dir
        file_path = target_dir / f"{exp.task_id}.json"
        file_path.write_text(json.dumps(exp.to_dict(), indent=2))
        
        # 索引到向量存储
        if self.vector_store:
            try:
                from ai_as_me.rag.retriever import TaskExperience
                rag_exp = TaskExperience(
                    task_id=exp.task_id,
                    description=exp.description,
                    tool_used=exp.tool_used,
                    result_summary=exp.result,
                    success=exp.success,
                    user_feedback=None,
                    created_at=exp.timestamp
                )
                self.vector_store.add(rag_exp)
            except Exception as e:
                print(f"Warning: Failed to index to vector store: {e}")
        
        return exp
    
    def get_recent(self, limit: int = 10) -> list[Experience]:
        """获取最近的经验"""
        all_files = sorted(
            list(self.successes_dir.glob("*.json")) + 
            list(self.failures_dir.glob("*.json")),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        experiences = []
        for f in all_files[:limit]:
            try:
                data = json.loads(f.read_text())
                data['timestamp'] = datetime.fromisoformat(data['timestamp'])
                experiences.append(Experience(**data))
            except Exception:
                continue
        
        return experiences
