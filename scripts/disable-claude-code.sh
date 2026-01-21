#!/bin/bash
# Disable Claude Code Integration
# This script removes Claude Code to prevent token consumption

set -e

echo "🚫 Disabling Claude Code Integration"
echo "====================================="
echo ""

# Remove Claude Code agent file
if [ -f "src/ai_as_me/agents/claude_agent.py" ]; then
    rm -f src/ai_as_me/agents/claude_agent.py
    echo "✓ Removed claude_agent.py"
fi

# Remove Claude Code scripts
rm -f scripts/select_claude_model.py scripts/query_claude_models.py
echo "✓ Removed Claude Code scripts"

# Remove Claude Code config
rm -f _bmad/_config/ides/claude-code.yaml
echo "✓ Removed Claude Code config"

# Backup and clear Claude Code cache (optional)
if [ -d ~/.claude ]; then
    echo ""
    read -p "Clear Claude Code cache in ~/.claude? [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        mv ~/.claude ~/.claude.backup.$(date +%Y%m%d_%H%M%S)
        echo "✓ Claude cache backed up and cleared"
    else
        echo "⊘ Skipped cache clearing"
    fi
fi

echo ""
echo "====================================="
echo "✓ Claude Code integration disabled"
echo ""
echo "Only OpenCode agent is now available."
echo "This prevents unauthorized token consumption."
echo ""
