"""Agent main loop."""

import time
import signal
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional
from datetime import datetime

# 延迟初始化的 logger
logger = logging.getLogger(__name__)
_logging_configured = False


def setup_logging(log_dir: Path = None):
    """配置日志系统（应在应用启动时调用）."""
    global _logging_configured
    if _logging_configured:
        return

    log_dir = log_dir or Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - [%(task_id)s] %(message)s",
        defaults={"task_id": "N/A"},
    )

    # 文件 handler（带轮转）
    file_handler = RotatingFileHandler(
        log_dir / "agent.log", maxBytes=10 * 1024 * 1024, backupCount=7  # 10MB
    )
    file_handler.setFormatter(formatter)

    # 控制台 handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger("ai_as_me")
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    _logging_configured = True


class Agent:
    """Main agent loop."""

    def __init__(
        self,
        kanban_dir: Path,
        llm_client=None,
        soul_context: Optional[str] = None,
        skip_clarification: bool = True,
        tracker=None,
        poll_interval: int = 5,
        reflection_hour: int = 3,
    ):
        self.kanban_dir = kanban_dir
        self.inbox_dir = kanban_dir / "inbox"
        self.todo_dir = kanban_dir / "todo"
        self.doing_dir = kanban_dir / "doing"
        self.done_dir = kanban_dir / "done"
        self.poll_interval = poll_interval
        self.running = False
        self.skip_clarification = skip_clarification
        self.tracker = tracker
        self.reflection_hour = reflection_hour
        self._last_reflection_date = None

        # LLM execution
        self.llm_client = llm_client
        self.soul_context = soul_context
        self.executor = None
        self.clarifier = None

        # v3.0: Evolution Engine
        self.evolution_engine = None

        # v3.1: Conflict Detector
        self.conflict_detector = None

        # v3.2: Inspiration Capturer
        self.inspiration_capturer = None
        self.inspiration_pool = None

        if llm_client:
            from ai_as_me.agents.executor import AgentExecutor
            from ai_as_me.agents.registry import AgentRegistry
            from ai_as_me.clarify.analyzer import ClarificationAnalyzer

            # 使用新的AgentExecutor支持opencode (claude-code temporarily disabled)
            registry = AgentRegistry()
            self.executor = AgentExecutor(registry)
            self.clarifier = ClarificationAnalyzer(llm_client)

            # v3.0: 初始化进化引擎
            try:
                from ai_as_me.evolution.engine import EvolutionEngine

                self.evolution_engine = EvolutionEngine(
                    {
                        "experience_dir": str(kanban_dir.parent / "experience"),
                        "soul_dir": str(kanban_dir.parent / "soul"),
                        "llm_client": llm_client,
                        "log_path": str(kanban_dir.parent / "logs" / "evolution.jsonl"),
                    }
                )
                print("🧬 Evolution Engine initialized")
            except Exception as e:
                print(f"⚠️ Evolution Engine init failed: {e}")

            # v3.1: 初始化冲突检测器（启动时自动扫描）
            try:
                from ai_as_me.soul.conflict_detector import ConflictDetector
                from ai_as_me.soul.conflict_resolver import ConflictResolver
                import asyncio

                self.conflict_detector = ConflictDetector(
                    kanban_dir.parent / "soul" / "rules"
                )
                conflicts = asyncio.run(self.conflict_detector.scan())

                if conflicts:
                    print(f"⚠️  发现 {len(conflicts)} 个规则冲突")
                    resolver = ConflictResolver(
                        kanban_dir.parent / "logs" / "rule-conflicts.jsonl"
                    )
                    for conflict in conflicts:
                        asyncio.run(resolver.auto_resolve(conflict))
                    print("✓ 冲突已自动处理（Core rules 优先）")
            except Exception as e:
                print(f"⚠️ Conflict Detector init failed: {e}")

            # v3.2: 初始化灵感捕获器
            try:
                from ai_as_me.inspiration import InspirationCapturer, InspirationPool

                self.inspiration_capturer = InspirationCapturer()
                # 使用项目根目录下的 soul/inspiration
                project_root = kanban_dir.parent
                self.inspiration_pool = InspirationPool(
                    project_root / "soul" / "inspiration"
                )
                logger.info("Inspiration Capturer initialized")
            except Exception as e:
                logger.error(f"Inspiration Capturer init failed: {e}")

        # Setup signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
        self.running = False

    def _format_result_metadata(self, result) -> str:
        """格式化执行结果的元数据部分."""
        from ai_as_me.utils.result_formatter import format_result_metadata

        return format_result_metadata(result)

    def _capture_inspiration(self, task_id: str, success: bool, detail: str):
        """统一的灵感捕获方法."""
        if not (self.inspiration_capturer and self.inspiration_pool):
            return

        try:
            task_result = {
                "task_id": task_id,
                "success": success,
                "error" if not success else "result": detail,
            }
            inspiration = self.inspiration_capturer.capture_from_task(task_result)
            if inspiration:
                insp_id = self.inspiration_pool.add(inspiration)
                status = "success" if success else "failure"
                logger.info(
                    f"Inspiration captured: task={task_id}, status={status}, id={insp_id}"
                )
        except Exception as e:
            logger.error(f"Inspiration capture failed: task={task_id}, error={e}")

    def _process_inbox(self):
        """Process tasks in inbox: analyze and move to todo."""
        inbox_tasks = (
            list(self.inbox_dir.glob("*.md")) if self.inbox_dir.exists() else []
        )

        for task_path in inbox_tasks:
            print(f"📥 New task in inbox: {task_path.name}")

            # Check for approval requirement
            content = task_path.read_text()
            if "[需要审批]" in content or "[NEEDS_APPROVAL]" in content:
                approval_file = self.todo_dir / f"{task_path.stem}.approved"
                if not approval_file.exists():
                    print("  ⏸️  Requires approval, moving to todo (waiting)")
                    self._move_task(task_path, self.todo_dir)
                    continue

            # Move to todo for execution
            self._move_task(task_path, self.todo_dir)
            print("  → Moved to todo")

    def _should_reflect(self) -> bool:
        """Check if it's time for scheduled reflection."""
        now = datetime.now()
        today = now.date()

        # Only reflect once per day at the specified hour
        if self._last_reflection_date == today:
            return False

        return now.hour == self.reflection_hour

    def _run_reflection(self, rules_file: Path):
        """Run scheduled reflection on completed tasks."""
        from ai_as_me.reflect.extractor import ReflectionEngine

        print("🌙 Running scheduled reflection...")

        try:
            engine = ReflectionEngine(self.llm_client, self.done_dir, rules_file)
            analyses = engine.analyze_tasks(last_n=10)

            if not analyses:
                print("  No completed tasks to analyze")
                return

            rules = engine.extract_rules(analyses)

            for rule in rules:
                engine.add_rule(rule)
                print(f"  📝 New rule: [{rule['category']}] {rule['content']}")

            self._last_reflection_date = datetime.now().date()
            print(f"  ✓ Reflection complete, {len(rules)} rules extracted")

        except Exception as e:
            print(f"  ❌ Reflection error: {e}")

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
        print("  → Moved to doing")

        success = False

        # Execute task if executor available
        if self.executor:
            try:
                task = Task(doing_path)

                # Clarification phase
                if self.clarifier and not self.skip_clarification:
                    if self.clarifier.should_clarify(task):
                        print("  🤔 Analyzing task complexity...")
                        complexity = self.clarifier.analyze_complexity(task)
                        print(f"  📊 Complexity: {complexity}")
                        print("  ⏭️  Skipping clarification (not implemented)")

                # Execute
                print("  🤖 Executing with agent...")
                result = self.executor.execute_task(task)

                if result and result.success:
                    # Save result with execution metadata
                    result_file = doing_path.stem + "-result.md"
                    result_path = self.done_dir / result_file

                    # Build result content with metadata
                    metadata_section = self._format_result_metadata(result)
                    result_content = f"# {task.title}\n\n{metadata_section}\n\n## 执行结果\n\n{result.output}"
                    result_path.write_text(result_content)
                    print(f"  ✓ Result saved: {result_file}")
                    success = True
                else:
                    error_msg = result.error if result else "Unknown error"
                    print(f"  ✗ Execution failed: {error_msg}")

            except Exception as e:
                print(f"  ❌ Error: {e}")
        else:
            # No executor, just simulate
            time.sleep(1)
            success = True

        # Move to appropriate directory
        if success:
            self._move_task(doing_path, self.done_dir)
            print("  ✓ Completed, moved to done")

            # v3.0: 触发进化
            if self.evolution_engine:
                try:
                    evolution_result = self.evolution_engine.evolve(
                        task, result or "No result", success=True
                    )
                    if evolution_result.get("rules"):
                        logger.info(
                            f"Evolution: {len(evolution_result['rules'])} new rules generated"
                        )
                except Exception as e:
                    logger.error(f"Evolution failed: {e}")

            # v3.2: 自动捕获灵感
            self._capture_inspiration(task_path.stem, True, result or "Task completed")
        else:
            # Move back to inbox on failure
            self._move_task(doing_path, self.kanban_dir / "inbox")
            print("  ↩️ Failed, moved back to inbox")

            # v3.0: 记录失败经验
            if self.evolution_engine:
                try:
                    self.evolution_engine.evolve(
                        task, "Execution failed", success=False
                    )
                except Exception as e:
                    logger.error(f"Evolution (failure) failed: {e}")

            # v3.2: 自动捕获灵感
            self._capture_inspiration(task_path.stem, False, "Execution failed")

    def start(self):
        """Start the agent main loop."""
        # Log agent start
        if self.tracker:
            self.tracker.info(
                "agent",
                "start",
                {
                    "poll_interval": self.poll_interval,
                    "skip_clarification": self.skip_clarification,
                },
            )

        print("🚀 AI-as-Me Agent starting...")
        print(f"📂 Watching: {self.inbox_dir} → {self.todo_dir}")
        print(f"⏱️  Poll interval: {self.poll_interval}s")

        if self.executor:
            print("🤖 LLM execution: enabled")
            clarify_status = "disabled (skip)" if self.skip_clarification else "enabled"
            print(f"🤔 Clarification: {clarify_status}")
        else:
            print("⚠️  LLM execution: disabled (simulation mode)")

        print("Press Ctrl+C to stop\n")

        self.running = True

        while self.running:
            try:
                # Rotate logs if needed
                if self.tracker:
                    self.tracker.rotate_if_needed()

                # Step 1: Process inbox → todo
                self._process_inbox()

                # Step 2: Check for tasks in todo directory
                tasks = (
                    list(self.todo_dir.glob("*.md")) if self.todo_dir.exists() else []
                )

                # Filter out tasks waiting for approval
                executable_tasks = []
                for t in tasks:
                    content = t.read_text()
                    if "[需要审批]" in content or "[NEEDS_APPROVAL]" in content:
                        approval_file = self.todo_dir / f"{t.stem}.approved"
                        if not approval_file.exists():
                            continue
                    executable_tasks.append(t)

                if executable_tasks:
                    print(f"📋 Found {len(executable_tasks)} task(s) ready to execute")

                    # Process first task
                    self._process_task(executable_tasks[0])
                elif self._should_reflect() and self.llm_client:
                    # Idle time reflection
                    rules_file = self.kanban_dir.parent / "soul" / "rules.md"
                    if rules_file.exists():
                        self._run_reflection(rules_file)
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
