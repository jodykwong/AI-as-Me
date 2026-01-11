"""Agent main loop."""
import time
import signal
import sys
from pathlib import Path
from typing import Optional


class Agent:
    """Main agent loop."""
    
    def __init__(self, kanban_dir: Path, llm_client=None, soul_context: Optional[str] = None, 
                 skip_clarification: bool = True, tracker=None, poll_interval: int = 5):
        self.kanban_dir = kanban_dir
        self.todo_dir = kanban_dir / "todo"
        self.doing_dir = kanban_dir / "doing"
        self.done_dir = kanban_dir / "done"
        self.poll_interval = poll_interval
        self.running = False
        self.skip_clarification = skip_clarification
        self.tracker = tracker
        
        # LLM execution
        self.llm_client = llm_client
        self.soul_context = soul_context
        self.executor = None
        self.clarifier = None
        
        if llm_client:
            from ai_as_me.llm.executor import TaskExecutor
            from ai_as_me.clarify.analyzer import ClarificationAnalyzer
            
            self.executor = TaskExecutor(llm_client, soul_context, tracker)
            self.clarifier = ClarificationAnalyzer(llm_client)
        
        # Setup signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def _move_task(self, task_path: Path, target_dir: Path):
        """Move task to target directory."""
        target_path = target_dir / task_path.name
        task_path.rename(target_path)
        return target_path
    
    def _process_task(self, task_path: Path):
        """Process a single task."""
        from ai_as_me.kanban.manager import Task
        
        print(f"📝 Processing: {task_path.name}")
        
        # Move to doing
        doing_path = self._move_task(task_path, self.doing_dir)
        print(f"  → Moved to doing")
        
        success = False
        
        # Execute task if executor available
        if self.executor:
            try:
                task = Task(doing_path)
                
                # Clarification phase
                if self.clarifier and not self.skip_clarification:
                    if self.clarifier.should_clarify(task):
                        print(f"  🤔 Analyzing task complexity...")
                        complexity = self.clarifier.analyze_complexity(task)
                        print(f"  📊 Complexity: {complexity}")
                        print(f"  ⏭️  Skipping clarification (not implemented)")
                
                # Execute
                print(f"  🤖 Executing with LLM...")
                result = self.executor.execute(task)
                
                if result:
                    # Save result
                    result_file = doing_path.stem + "-result.md"
                    result_path = self.done_dir / result_file
                    self.executor.save_result(result, result_path, doing_path.name)
                    print(f"  ✓ Result saved: {result_file}")
                    success = True
                else:
                    print(f"  ✗ Execution failed")
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
        else:
            # No executor, just simulate
            time.sleep(1)
            success = True
        
        # Move to appropriate directory
        if success:
            done_path = self._move_task(doing_path, self.done_dir)
            print(f"  ✓ Completed, moved to done")
        else:
            # Move back to inbox on failure
            inbox_path = self._move_task(doing_path, self.kanban_dir / "inbox")
            print(f"  ↩️ Failed, moved back to inbox")
    
    def start(self):
        """Start the agent main loop."""
        # Log agent start
        if self.tracker:
            self.tracker.info("agent", "start", {
                "poll_interval": self.poll_interval,
                "skip_clarification": self.skip_clarification
            })
        
        print("🚀 AI-as-Me Agent starting...")
        print(f"📂 Watching: {self.todo_dir}")
        print(f"⏱️  Poll interval: {self.poll_interval}s")
        
        if self.executor:
            print(f"🤖 LLM execution: enabled")
            clarify_status = "disabled (skip)" if self.skip_clarification else "enabled"
            print(f"🤔 Clarification: {clarify_status}")
        else:
            print(f"⚠️  LLM execution: disabled (simulation mode)")
        
        print("Press Ctrl+C to stop\n")
        
        self.running = True
        
        while self.running:
            try:
                # Rotate logs if needed
                if self.tracker:
                    self.tracker.rotate_if_needed()
                
                # Check for tasks in todo directory
                tasks = list(self.todo_dir.glob("*.md")) if self.todo_dir.exists() else []
                
                if tasks:
                    print(f"📋 Found {len(tasks)} task(s) in queue")
                    
                    # Process first task
                    self._process_task(tasks[0])
                else:
                    print("💤 No tasks in queue, waiting...")
                
                # Sleep with interrupt check
                for _ in range(self.poll_interval):
                    if not self.running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                if self.tracker:
                    self.tracker.error("agent", "loop_error", {"error": str(e)})
                time.sleep(self.poll_interval)
        
        # Log agent stop
        if self.tracker:
            self.tracker.info("agent", "stop", {})
        
        print("✓ Agent stopped")
