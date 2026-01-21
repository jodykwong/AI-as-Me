#!/bin/bash
# 彻底清除 Claude Code 集成 - 完整版
# 修复 token 偷跑问题

set -e

echo "🔥 彻底清除 Claude Code 集成"
echo "================================"
echo ""

# 1. 删除活跃脚本（最危险）
echo "1️⃣ 删除活跃脚本..."
rm -f scripts/agent_manager.py
rm -f scripts/query_models.py
rm -f test_integration_real.py
echo "✓ 删除了 agent_manager.py 和相关脚本"

# 2. 清理配置文件
echo ""
echo "2️⃣ 清理配置文件..."
if [ -f "_bmad/_config/manifest.yaml" ]; then
    sed -i '/claude-code/d' _bmad/_config/manifest.yaml
    echo "✓ 从 BMAD manifest 移除 claude-code"
fi

if [ -f "config/agents.yaml" ]; then
    sed -i '/claude/d' config/agents.yaml
    echo "✓ 从 agents.yaml 移除 claude"
fi

# 3. 清理缓存
echo ""
echo "3️⃣ 清理缓存..."
rm -rf .mypy_cache/
rm -rf __pycache__/
find . -name "*.pyc" -delete
find . -name "*claude*.pyc" -delete
echo "✓ 清理了 Python 缓存"

# 4. 备份并清理 Claude 项目配置
echo ""
echo "4️⃣ 处理 Claude 项目配置..."
if [ -d ~/.claude/projects/-home-sunrise-AI-as-Me ]; then
    BACKUP_DIR=~/.claude-backup-$(date +%Y%m%d_%H%M%S)
    mkdir -p "$BACKUP_DIR"
    mv ~/.claude/projects/-home-sunrise-AI-as-Me "$BACKUP_DIR/"
    echo "✓ 备份并移除了 Claude 项目配置到 $BACKUP_DIR"
fi

# 5. 清理 Claude 本地设置
if [ -f .claude/settings.local.json ]; then
    mv .claude/settings.local.json .claude/settings.local.json.bak
    echo "✓ 备份了 .claude/settings.local.json"
fi

# 6. 验证清理结果
echo ""
echo "5️⃣ 验证清理结果..."
echo ""

CLAUDE_REFS=$(grep -r "claude" --include="*.py" --include="*.sh" . 2>/dev/null | grep -v ".git" | grep -v "__pycache__" | grep -v "# " | grep -v "disable-claude" | grep -v "CLAUDE_CODE_REMOVAL" | wc -l)

if [ "$CLAUDE_REFS" -eq 0 ]; then
    echo "✅ 验证通过：没有发现活跃的 Claude 引用"
else
    echo "⚠️  仍有 $CLAUDE_REFS 个 Claude 引用，请手动检查："
    grep -r "claude" --include="*.py" --include="*.sh" . 2>/dev/null | grep -v ".git" | grep -v "__pycache__" | grep -v "# " | grep -v "disable-claude" | grep -v "CLAUDE_CODE_REMOVAL" | head -5
fi

echo ""
echo "================================"
echo "✅ 清理完成！"
echo ""
echo "建议："
echo "1. 重启任何运行中的 AI-as-Me 服务"
echo "2. 检查 Claude API 使用情况"
echo "3. 监控未来 24 小时是否还有 token 消耗"
echo ""
