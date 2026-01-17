# Agent 模型配置指南

## 概述

本指南说明如何配置和使用 OpenCode 和 Claude Code 的自动化模型选择功能。

## OpenCode 配置

### 查询可用模型

```bash
python3 scripts/query_opencode_models.py
```

输出示例：
```json
[
  "opencode/big-pickle",
  "opencode/glm-4.7-free",
  "opencode/gpt-5-nano",
  "opencode/grok-code",
  "opencode/minimax-m2.1-free"
]
```

### 配置文件

编辑 `.opencode/config.yaml`:

```yaml
settings:
  model: opencode/big-pickle  # 使用 provider/model 格式
  temperature: 0
  max_iterations: 50
```

## Claude Code 配置

### 查询支持的模型

```bash
python3 scripts/query_claude_models.py
```

输出示例：
```json
["sonnet", "opus"]
```

### 智能模型选择

系统根据任务复杂度自动选择：

| 任务类型 | 条件 | 模型 |
|---------|------|------|
| 简单 | < 50 词或 < 5 行 | haiku |
| 常规 | 50-200 词 | sonnet |
| 复杂 | > 200 词或 > 20 行 | opus |

### 手动选择

```bash
# 简单任务
echo "Fix typo" | python3 scripts/select_claude_model.py
# 输出: haiku

# 复杂任务
echo "Refactor entire auth system with OAuth2, SAML..." | python3 scripts/select_claude_model.py
# 输出: opus
```

## 统一 Agent 管理

### 使用 Agent Manager

```bash
# OpenCode
echo "Create login page" | python3 scripts/agent_manager.py opencode

# Claude Code
echo "Review security" | python3 scripts/agent_manager.py claude
```

## 最佳实践

1. **定期更新模型列表**: 运行查询脚本获取最新模型
2. **根据成本选择**: 优先使用免费模型（OpenCode）
3. **任务分类**: 简单任务用 Haiku，复杂任务用 Sonnet/Opus
4. **配置备份**: 保存工作配置到版本控制

## 故障排除

### OpenCode 无可用模型

```bash
# 检查网络连接
npx opencode-ai models

# 检查配置
cat .opencode/config.yaml
```

### Claude Code 模型不可用

```bash
# 查看帮助
npx @anthropic-ai/claude-code --help

# 测试连接
npx @anthropic-ai/claude-code --model sonnet --print "test"
```

## API Key 配置

### OpenCode Zen（推荐）

1. 访问 https://opencode.ai/auth
2. 获取 API Key
3. 设置环境变量：
   ```bash
   export OPENCODE_API_KEY=your_key
   ```

### Claude Code

1. 访问 https://console.anthropic.com
2. 获取 API Key
3. 设置环境变量：
   ```bash
   export ANTHROPIC_API_KEY=your_key
   ```

## 参考资料

- OpenCode 文档: https://opencode.ai/docs
- Claude 文档: https://docs.anthropic.com
- 项目 SOP: `docs/AGENT_INTEGRATION_SOP.md`
