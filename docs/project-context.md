# AI-as-Me Project Context

**Version**: 3.5.0  
**Last Updated**: 2026-01-22

## Critical Rules for AI Agents

### Rule 1: Soul System is Sacred
- NEVER modify `soul/` files without explicit user approval
- File permissions: `soul/` = 700, `*.md` = 600

### Rule 2: Kanban Task Integrity
- Tasks stored in `kanban/{inbox,todo,doing,done}/`
- Task IDs: 8-char UUID or filename-based
- NEVER delete tasks

### Rule 3: Security First
- Validate ALL external inputs
- No SQL/command injection
- Sanitize file paths

## Code Standards

- **Formatter**: Black (line length 100)
- **Type hints**: Required
- **Docstrings**: Chinese preferred
- **Naming**: snake_case for functions, PascalCase for classes

## Quick Reference

```bash
ai-as-me task list              # List tasks
ai-as-me agent list             # List agents
ai-as-me soul check             # Security check
```

**Key Files**:
- `src/ai_as_me/cli_main.py` - CLI entry
- `src/ai_as_me/soul/loader.py` - Soul management
- `src/ai_as_me/kanban/vibe_manager.py` - Task management
