"""CLI entry point for AI-as-Me."""
import click
from pathlib import Path
import sys
from functools import wraps


def handle_errors(f):
    """Decorator to handle common CLI errors."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            click.echo(f"✗ Error: {e}", err=True)
            sys.exit(1)
        except KeyboardInterrupt:
            click.echo("\n✓ Interrupted by user")
            sys.exit(0)
    return wrapper


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """AI-as-Me - Personal AI Agent with Soul
    
    A self-evolving AI agent that learns from your tasks and decisions.
    """
    pass


@cli.command()
@handle_errors
def status():
    """Show system status and task queue information."""
    from ai_as_me.core.config import load_config
    from ai_as_me.kanban.manager import KanbanManager
    from ai_as_me.soul.loader import SoulLoader
    
    # Load config
    config = load_config()
    click.echo("✓ Configuration loaded")
    
    # Check API connection (basic check)
    click.echo(f"✓ API endpoint: {config.api_base}")
    click.echo(f"✓ Model: {config.model}")
    
    # Check soul files
    soul_loader = SoulLoader(config.soul_dir)
    soul_status = soul_loader.check_status()
    click.echo("\n📖 Soul Files:")
    for name, exists in soul_status.items():
        status_icon = "✓" if exists else "✗"
        click.echo(f"  {status_icon} {name}.md")
    
    # Check task queue
    kanban = KanbanManager(config.kanban_dir)
    counts = kanban.get_task_counts()
    click.echo("\n📋 Task Queue:")
    click.echo(f"  Inbox: {counts['inbox']}")
    click.echo(f"  Todo:  {counts['todo']}")
    click.echo(f"  Doing: {counts['doing']}")
    click.echo(f"  Done:  {counts['done']}")


@cli.command()
@handle_errors
def run():
    """Start the agent main loop."""
    from ai_as_me.core.config import load_config
    from ai_as_me.core.agent import Agent
    from ai_as_me.soul.loader import SoulLoader
    from ai_as_me.llm.client import LLMClient
    from ai_as_me.logger.tracker import EventTracker
    
    config = load_config()
    
    # Initialize event tracker
    tracker = EventTracker(config.logs_dir)
    
    # Load soul context
    soul_loader = SoulLoader(config.soul_dir)
    soul_context = soul_loader.load_all()
    
    # Initialize LLM client
    llm_client = LLMClient(
        api_key=config.api_key,
        base_url=config.api_base,
        model=config.model
    )
    
    # Start agent with LLM
    agent = Agent(
        config.kanban_dir,
        llm_client=llm_client,
        soul_context=soul_context,
        skip_clarification=config.skip_clarification,
        tracker=tracker,
        poll_interval=5
    )
    agent.start()


@cli.command()
@click.option('--last', default=5, help='Analyze last N tasks')
@click.option('--auto-approve', is_flag=True, help='Automatically approve all rules')
@handle_errors
def reflect(last, auto_approve):
    """Trigger reflection and rule extraction."""
    from ai_as_me.core.config import load_config
    from ai_as_me.llm.client import LLMClient
    from ai_as_me.reflect.extractor import ReflectionEngine
    
    config = load_config()
    
    # Initialize LLM client
    llm_client = LLMClient(
        api_key=config.api_key,
        base_url=config.api_base,
        model=config.model
    )
    
    # Initialize reflection engine
    done_dir = config.kanban_dir / "done"
    rules_file = config.soul_dir / "rules.md"
    
    engine = ReflectionEngine(llm_client, done_dir, rules_file)
    
    click.echo(f"🤔 Analyzing last {last} completed tasks...")
    
    # Analyze tasks
    analyses = engine.analyze_tasks(last_n=last)
    
    if not analyses:
        click.echo("No completed tasks found")
        return
    
    click.echo(f"✓ Analyzed {len(analyses)} tasks")
    
    # Extract rules
    click.echo("\n🔍 Extracting potential rules...")
    rules = engine.extract_rules(analyses)
    
    if not rules:
        click.echo("No new rules extracted")
        return
    
    click.echo(f"✓ Extracted {len(rules)} potential rules\n")
    
    # Show and confirm rules
    approved_rules = []
    
    for i, rule in enumerate(rules, 1):
        click.echo(f"📋 Rule {i}/{len(rules)}")
        click.echo(f"   Category: {rule['category']}")
        click.echo(f"   Content: {rule['content']}")
        click.echo(f"   Source: {rule['source']}")
        click.echo(f"   Confidence: {rule['confidence']}")
        
        if auto_approve:
            click.echo("   ✓ Auto-approved\n")
            approved_rules.append(rule)
        else:
            if click.confirm("   Approve this rule?", default=True):
                approved_rules.append(rule)
                click.echo("   ✓ Approved\n")
            else:
                click.echo("   ✗ Rejected\n")
    
    # Add approved rules
    if approved_rules:
        click.echo(f"💾 Adding {len(approved_rules)} rules to rules.md...")
        
        for rule in approved_rules:
            engine.add_rule(rule)
        
        click.echo(f"✓ Rules added successfully!")
        click.echo(f"\nRun 'ai-as-me rules' to view all rules")
    else:
        click.echo("No rules were approved")


@cli.command()
@handle_errors
def init():
    """Initialize soul files with templates."""
    from ai_as_me.core.config import load_config
    from ai_as_me.soul.loader import SoulLoader
    
    config = load_config()
    soul_loader = SoulLoader(config.soul_dir)
    soul_loader.initialize()
    
    click.echo("✓ Soul directory initialized")
    click.echo(f"📂 Location: {config.soul_dir}")
    click.echo("\nCreated files:")
    click.echo("  - profile.md (personal background and style)")
    click.echo("  - rules.md (decision rules and preferences)")
    click.echo("  - mission.md (goals and values)")
    click.echo("\nEdit these files to define your AI's personality!")


@cli.command()
@handle_errors
def rules():
    """View current rules from rules.md."""
    from ai_as_me.core.config import load_config
    from ai_as_me.soul.loader import SoulLoader
    import re
    
    config = load_config()
    soul_loader = SoulLoader(config.soul_dir)
    
    if not soul_loader.rules_file.exists():
        click.echo("⚠️  No rules.md file found")
        click.echo("Run 'ai-as-me init' to create soul files")
        sys.exit(1)
    
    content = soul_loader.rules_file.read_text()
    
    # Extract rules (lines starting with -)
    rule_lines = [line.strip() for line in content.split('\n') 
                 if line.strip().startswith('-')]
    
    # Extract categories (## headers)
    categories = re.findall(r'^## (.+)$', content, re.MULTILINE)
    
    click.echo("📋 Current Rules\n")
    
    if not rule_lines:
        click.echo("No rules defined yet. Edit soul/rules.md to add rules.")
    else:
        click.echo(content)
        click.echo(f"\n📊 Statistics:")
        click.echo(f"  Categories: {len(categories)}")
        click.echo(f"  Total Rules: {len(rule_lines)}")


@cli.command()
@handle_errors
def tasks():
    """List all tasks by status."""
    from ai_as_me.core.config import load_config
    from ai_as_me.kanban.manager import KanbanManager
    
    config = load_config()
    kanban = KanbanManager(config.kanban_dir)
    
    counts = kanban.get_task_counts()
    total = sum(counts.values())
    
    click.echo(f"📋 Tasks ({total} total)\n")
    
    for status in ["inbox", "todo", "doing", "done"]:
        task_list = kanban.get_tasks(status)
        icon = {"inbox": "📥", "todo": "📝", "doing": "⚙️", "done": "✅"}[status]
        
        click.echo(f"{icon} {status.upper()} ({len(task_list)})")
        
        if task_list:
            for task in task_list:
                created = f" ({task.created_at})" if task.created_at else ""
                priority_icon = "🔴" if task.priority == "high" else "🟡" if task.priority == "medium" else ""
                click.echo(f"  {priority_icon} {task.title}{created}")
        
        click.echo()


@cli.command()
@click.argument('task_file')
@click.argument('target_status', type=click.Choice(['inbox', 'todo', 'doing', 'done']))
@handle_errors
def move(task_file, target_status):
    """Move a task to a different status.
    
    Example: ai-as-me move my-task.md todo
    """
    from ai_as_me.core.config import load_config
    from ai_as_me.kanban.manager import KanbanManager
    
    config = load_config()
    kanban = KanbanManager(config.kanban_dir)
    
    if kanban.move_task(task_file, target_status):
        click.echo(f"✓ Moved {task_file} to {target_status}")
    else:
        click.echo(f"✗ Task {task_file} not found or target exists", err=True)
        sys.exit(1)


@cli.command()
@click.option('--task', help='Filter by task name')
@click.option('--level', type=click.Choice(['info', 'warning', 'error']), help='Filter by log level')
@click.option('-n', '--lines', default=20, help='Number of lines to show')
@handle_errors
def logs(task, level, lines):
    """View execution logs."""
    from ai_as_me.core.config import load_config
    import json
    
    config = load_config()
    logs_dir = config.logs_dir
    
    if not logs_dir.exists():
        click.echo("No logs found")
        return
    
    # Collect all log entries
    entries = []
    for log_file in sorted(logs_dir.glob("*.jsonl")):
        with open(log_file) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    
                    # Apply filters
                    if level and entry.get('level') != level:
                        continue
                    
                    if task and 'data' in entry and entry['data'].get('task') != task:
                        continue
                    
                    entries.append(entry)
                except json.JSONDecodeError:
                    continue
    
    # Show last N entries
    entries = entries[-lines:]
    
    if not entries:
        click.echo("No matching log entries")
        return
    
    click.echo(f"📋 Showing {len(entries)} log entries\n")
    
    for entry in entries:
        ts = entry.get('ts', '')[:19]  # Trim microseconds
        level_icon = {"info": "ℹ️", "warning": "⚠️", "error": "❌"}.get(entry.get('level'), "•")
        module = entry.get('module', '')
        event = entry.get('event', '')
        
        click.echo(f"{level_icon} {ts} [{module}] {event}")
        
        if 'data' in entry:
            for key, value in entry['data'].items():
                click.echo(f"    {key}: {value}")
        click.echo()


if __name__ == "__main__":
    cli()
