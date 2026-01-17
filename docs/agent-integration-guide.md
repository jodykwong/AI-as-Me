# AI Coding Agents 集成指南

## 前置要求

1. **Node.js** (>=18)
2. **API密钥**
   - Claude Code: Anthropic API Key
   - OpenCode: 支持多种模型（OpenAI, Anthropic等）

## 安装和认证

### Claude Code

```bash
# 1. 安装（首次运行会自动安装）
npx -y @anthropic-ai/claude-code

# 2. 认证（会提示输入API密钥）
# 按照提示完成认证流程

# 3. 测试
claude --print "Hello, 1+1等于几？"
```

### OpenCode

```bash
# 1. 安装
npx -y opencode-ai

# 2. 认证（会提示配置）
# 按照提示选择模型和输入API密钥

# 3. 测试
opencode "Hello, 2+2等于几？"
```

## 在 AI-as-Me 中使用

### 方式1：通过CLI

```bash
# 执行doing任务
python -m ai_as_me.cli_main execute <task-id> --tool claude-code

# 使用自动切换
python -m ai_as_me.cli_main execute <task-id> --tool claude-code --fallback
```

### 方式2：通过Kanban界面

1. 创建任务
2. 澄清任务时选择工具：`claude-code` 或 `opencode`
3. 移动到doing
4. 系统自动调用对应的agent执行

## 验证集成

```bash
# 运行集成测试
python test_integration_real.py
```

## 架构说明

```
AI-as-Me
├── AgentCLI (orchestrator/agent_cli.py)
│   ├── claude --print --dangerously-skip-permissions "prompt"
│   └── opencode "prompt"
│
├── Soul注入 (可选)
│   └── 自动添加 soul/profile + rules 到提示词
│
└── 任务执行
    ├── 读取 kanban/doing/{task-id}.md
    ├── 调用 agent
    └── 保存结果到 {task-id}-result.md
```

## 与 Vibe Kanban 的区别

| 特性 | Vibe Kanban | AI-as-Me |
|------|-------------|----------|
| 语言 | Rust + TypeScript | Python |
| 任务隔离 | Git Worktree | 文件目录 |
| 实时日志 | WebSocket流 | 文件日志 |
| 并行执行 | ✅ | ❌ (顺序执行) |
| Soul系统 | ❌ | ✅ |
| 自我进化 | ❌ | ✅ |

## 故障排查

### Claude Code 调用失败

```bash
# 检查是否已认证
claude --version

# 重新认证
rm -rf ~/.config/claude-code
npx -y @anthropic-ai/claude-code
```

### OpenCode 调用失败

```bash
# 检查配置
cat ~/.opencode/config.json

# 重新配置
opencode --configure
```

### 超时问题

默认超时5分钟。如需调整：

```python
agent = AgentCLI()
result = agent.call('claude-code', prompt, timeout=600)  # 10分钟
```

## API密钥管理

**不要**将API密钥提交到代码仓库！

使用环境变量：

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-xxx
```

Claude Code 和 OpenCode 会自动读取这些环境变量。
