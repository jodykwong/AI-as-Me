"""Task executor."""
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime


class TaskExecutor:
    """Execute tasks using LLM."""
    
    def __init__(self, llm_client, soul_context: Optional[str] = None, tracker=None):
        """Initialize task executor.
        
        Args:
            llm_client: LLMClient instance
            soul_context: Combined soul files content
            tracker: EventTracker instance
        """
        self.llm_client = llm_client
        self.soul_context = soul_context
        self.tracker = tracker
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with soul context."""
        base_prompt = """You are a personal AI assistant executing tasks on behalf of your user.

Your role is to:
1. Understand the task requirements thoroughly
2. Apply the user's rules and preferences
3. Generate high-quality, actionable outputs
4. Stay aligned with the user's mission and values
"""
        
        if self.soul_context:
            return f"{base_prompt}\n\n## Your Identity and Context\n\n{self.soul_context}"
        
        return base_prompt
    
    def execute(self, task) -> Optional[Dict]:
        """Execute a task.
        
        Args:
            task: Task object
            
        Returns:
            Dict with result content and metadata, or None if failed
        """
        start_time = datetime.now()
        
        # Log task start
        if self.tracker:
            self.tracker.info("executor", "task_start", {
                "task": task.title,
                "file": task.file_path.name
            })
        
        # Build messages
        system_prompt = self._build_system_prompt()
        
        user_message = f"""# Task: {task.title}

## Context
{task.context}
"""
        
        if task.expected_output:
            user_message += f"\n## Expected Output Format\n{task.expected_output}\n"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # Log LLM request
        if self.tracker:
            # Mask API key safely
            api_key = self.llm_client.client.api_key or ""
            masked_key = api_key[:4] + "****" if len(api_key) > 4 else "****"
            self.tracker.info("llm", "api_request", {
                "model": self.llm_client.model,
                "api_key": masked_key,
                "messages_count": len(messages),
                "system_prompt_length": len(system_prompt),
                "user_message_length": len(user_message)
            })
        
        # Execute
        result = self.llm_client.chat(messages)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        if result:
            # Log LLM response
            if self.tracker:
                self.tracker.info("llm", "api_response", {
                    "duration": duration,
                    "response_length": len(result)
                })
            
            # Log task completion
            if self.tracker:
                self.tracker.info("executor", "task_complete", {
                    "task": task.title,
                    "duration": duration
                })
            
            return {
                "content": result,
                "task_title": task.title,
                "started_at": start_time.isoformat(),
                "completed_at": end_time.isoformat(),
                "duration": duration,
                "model": self.llm_client.model,
            }
        else:
            # Log failure
            if self.tracker:
                self.tracker.error("executor", "task_failed", {
                    "task": task.title,
                    "duration": duration
                })
        
        return None
    
    def save_result(self, result: Dict, output_path: Path, task_file: str):
        """Save execution result to file.
        
        Args:
            result: Result dict from execute()
            output_path: Path to save result
            task_file: Original task filename
        """
        content = f"""---
task: {task_file}
title: {result['task_title']}
started_at: {result['started_at']}
completed_at: {result['completed_at']}
duration: {result['duration']:.2f}s
model: {result['model']}
---

# Result

{result['content']}
"""
        output_path.write_text(content)
        
        # Log result saved
        if self.tracker:
            self.tracker.info("executor", "result_saved", {
                "file": output_path.name
            })
