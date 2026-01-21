# AI-as-Me Project Context

**Version**: 3.5.0  
**Last Updated**: 2026-01-22  
**Purpose**: Critical rules and patterns for AI agents developing AI-as-Me

---

## Project Overview

AI-as-Me is a self-evolving AI digital twin system that learns from user interactions, adapts behavior through rule evolution, and manages tasks via an intelligent Kanban system.

**Core Philosophy**: The system evolves itself by learning patterns from user interactions and generating new behavioral rules automatically.

---

## Critical Rules for AI Agents

### Rule 1: Soul System is Sacred
- **NEVER** modify `soul/` files without explicit user approval
- Soul contains: `profile.md`, `mission.md`, `rules/core/`, `rules/learned/`
- File permissions: `soul/` = 700, `*.md` = 600, `.env` = 600
- All soul modifications must be logged in `logs/soul-evolution.log`

### Rule 2: Evolution System Safety
- Generated rules MUST pass safety validation before activation
- Pattern matching uses regex - validate all patterns before storage
- New rules go to `soul/rules/learned/` with metadata
- Archive ineffective rules to `soul/rules/archived/`

### Rule 3: Kanban Task Integrity
- Tasks stored in `kanban/{inbox,todo,doing,done}/`
- Task IDs: 8-char UUID (e.g., `9bcfeb01`) or filename-based
- Status transitions: inbox → todo → doing → done
- NEVER delete tasks, move to `done/` or `failed/`

### Rule 4: Agent Execution Isolation
- Each agent execution creates isolated environment
- Agent outputs logged to `logs/agent_calls.log`
- Failed executions must be recoverable
- Support both OpenCode and Claude Code agents

### Rule 5: Security First
- Validate ALL external inputs (API, CLI, file uploads)
- No SQL injection: use parameterized queries
- No command injection: validate shell commands
- Sanitize file paths to prevent traversal
- Log security events to `logs/security.log`

---

## Architecture Patterns

### Module Structure
```
src/ai_as_me/
├── soul/          # Soul system (profile, rules, evolution)
├── kanban/        # Task management (Vibe Kanban)
├── agents/        # Agent execution (OpenCode, Claude Code)
├── evolution/     # Pattern learning and rule generation
├── dashboard/     # Web UI (FastAPI + vanilla JS)
└── cli_main.py    # CLI entry point
```

### Data Flow
1. **User Interaction** → Dashboard/CLI
2. **Task Creation** → Kanban system
3. **Agent Execution** → Task processing
4. **Pattern Detection** → Evolution system
5. **Rule Generation** → Soul update (with approval)

### Key Technologies
- **Backend**: Python 3.9+, FastAPI, Pydantic
- **Database**: PostgreSQL (optional), JSON files (default)
- **Frontend**: Vanilla JavaScript, no frameworks
- **Agents**: OpenCode (Node.js), Claude Code (optional)
- **Testing**: pytest, Ralph (TDD workflows)

---

## Code Standards

### Python Style
- **Formatter**: Black (line length 100)
- **Linter**: Ruff
- **Type hints**: Required for all functions
- **Docstrings**: Chinese preferred, English acceptable
- **Naming**: snake_case for functions/variables, PascalCase for classes

### Error Handling
```python
# Always use specific exceptions
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise CustomError("User-friendly message") from e
```

### Logging
```python
# Use structured logging
logger.info("Task created", extra={
    "task_id": task_id,
    "status": "inbox",
    "user": user_id
})
```

---

## Testing Requirements

### Unit Tests
- Location: `tests/`
- Coverage: Minimum 70% for new code
- Run: `pytest tests/`

### Integration Tests
- Test agent execution end-to-end
- Test evolution system with mock patterns
- Test Kanban state transitions

### TDD with Ralph
- Use `ralph run -c ralph-test.yml` for TDD workflows
- Red → Green → Refactor cycle
- Test results in `.agent/test-results.md`

---

## File Conventions

### Configuration
- `.env` - Environment variables (API keys, secrets)
- `config.yaml` - Application configuration
- `_bmad/bmm/config.yaml` - BMAD workflow configuration

### Logs
- `logs/agent_calls.log` - Agent execution logs (1.6MB+)
- `logs/dashboard.log` - Web UI logs
- `logs/service.log` - Service startup/shutdown
- `logs/soul-evolution.log` - Soul modifications

### Data Storage
- `kanban/` - Task markdown files
- `soul/` - Soul system files
- `inspiration_pool/` - Idea storage (1526 items)
- `experience/` - Historical data

---

## Common Pitfalls

### ❌ Don't Do This
```python
# Direct file modification without validation
with open("soul/rules/core/rule.md", "w") as f:
    f.write(user_input)  # DANGEROUS!

# Unvalidated shell command
os.system(f"ai-as-me task {task_id}")  # INJECTION RISK!

# Missing type hints
def process_task(task):  # BAD
    return task.execute()
```

### ✅ Do This Instead
```python
# Validated file modification
from ai_as_me.soul.loader import SoulLoader
loader = SoulLoader(Path("soul"))
loader.update_rule(rule_id, validated_content)

# Safe command execution
import subprocess
result = subprocess.run(
    ["ai-as-me", "task", task_id],
    capture_output=True,
    text=True,
    timeout=30
)

# Proper type hints
def process_task(task: Task) -> TaskResult:
    return task.execute()
```

---

## Development Workflow

### Adding New Features
1. Create task in `kanban/inbox/`
2. Move to `todo/` when prioritized
3. Move to `doing/` when starting work
4. Write tests first (TDD)
5. Implement feature
6. Update documentation
7. Run `ai-as-me soul check` for security
8. Move to `done/` when complete

### Modifying Soul System
1. Get explicit user approval
2. Validate new rule format
3. Test rule in isolation
4. Add to `soul/rules/learned/`
5. Log change in `logs/soul-evolution.log`
6. Monitor effectiveness

### Agent Integration
1. Check agent availability: `ai-as-me agent list`
2. Test agent: `ai-as-me agent execute <task-id>`
3. Monitor logs: `tail -f logs/agent_calls.log`
4. Handle failures gracefully

---

## Performance Guidelines

- Dashboard response time: < 1 second
- Agent execution: Varies by task complexity
- Memory usage: < 500MB for service
- Database queries: Use indexes, avoid N+1

---

## Security Checklist

- [ ] Input validation on all external data
- [ ] Parameterized SQL queries
- [ ] File path sanitization
- [ ] Command injection prevention
- [ ] API authentication (if enabled)
- [ ] Secrets in `.env`, not code
- [ ] Soul file permissions (700/600)
- [ ] Error messages don't leak sensitive data

---

## Quick Reference

### CLI Commands
```bash
ai-as-me --version              # Check version
ai-as-me task list              # List tasks
ai-as-me agent list             # List available agents
ai-as-me soul check             # Security check
ai-as-me soul status            # Soul statistics
```

### Important Paths
- Project root: `/home/sunrise/AI-as-Me`
- Soul: `soul/`
- Kanban: `kanban/`
- Logs: `logs/`
- Config: `.env`, `config.yaml`

### Key Files
- `src/ai_as_me/cli_main.py` - CLI entry point
- `src/ai_as_me/dashboard/app.py` - Web server
- `src/ai_as_me/soul/loader.py` - Soul management
- `src/ai_as_me/kanban/vibe_manager.py` - Task management

---

**Remember**: This system evolves itself. Your changes should enable evolution, not replace it.
