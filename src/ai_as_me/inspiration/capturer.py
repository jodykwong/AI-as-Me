"""Inspiration Capturer - 灵感捕获器."""
import re
from typing import Optional
from .models import Inspiration


class InspirationCapturer:
    """从文本和任务中捕获灵感."""
    
    TRIGGER_PATTERNS = [
        (r"以后(可以|应该|要)(.+)", "future_action"),
        (r"(想法|灵感|idea)[：:]\s*(.+)", "explicit_idea"),
        (r"TODO[：:]\s*(.+)", "todo"),
        (r"或许(可以|应该)(.+)", "suggestion"),
        (r"如果能(.+)就好了", "wish"),
    ]
    
    def capture_from_text(self, text: str, source: str = "conversation", source_id: str = None) -> Optional[Inspiration]:
        """从文本中捕获灵感."""
        for pattern, tag in self.TRIGGER_PATTERNS:
            match = re.search(pattern, text)
            if match:
                # 提取灵感内容
                content = match.group(0)
                
                return Inspiration(
                    content=content,
                    source=source,
                    source_id=source_id,
                    tags=[tag],
                    priority=self._infer_priority(text)
                )
        return None
    
    def capture_from_task(self, task_result: dict) -> Optional[Inspiration]:
        """从任务结果中捕获灵感."""
        if not task_result.get("success", True):
            # 任务失败时记录改进想法
            return Inspiration(
                content=f"任务失败: {task_result.get('error', '未知错误')}，需要改进",
                source="task",
                source_id=task_result.get("task_id"),
                tags=["improvement", "failure"],
                priority="high"
            )
        return None
    
    def _infer_priority(self, text: str) -> str:
        """推断优先级."""
        high_keywords = ["紧急", "重要", "必须", "立刻", "马上"]
        low_keywords = ["以后", "有空", "或许", "可能"]
        
        for kw in high_keywords:
            if kw in text:
                return "high"
        for kw in low_keywords:
            if kw in text:
                return "low"
        return "medium"
