# AI-as-Me

个人 AI 代理系统，具有灵魂、记忆和**自我进化能力**。

## 特性

### v3.5 执行监控升级 🎯
- 🎯 **分阶段进度可视化**: PREPARING → ANALYZING → EXECUTING → VALIDATING → COMPLETED
- 📊 **实时进度条**: 0-100%执行进度显示，平滑动画效果
- 🎨 **状态颜色编码**: 🟡准备中 🔵执行中 🟢完成 🔴失败
- 🔍 **执行监控面板**: 实时显示doing任务状态和执行时长
- ⚡ **拖拽优化**: 修复卡片消失问题，本地状态更新
- 🛠️ **代码审查工作流**: 完整的代码质量检查和修复流程

### v3.0 核心突破 🧬
- 🧬 **自我进化**: AI 自动从经验中学习，生成新规则到 `soul/rules/learned/`
- 🔄 **进化闭环**: experience → pattern → rule 完整转化流程
- 🎯 **Skills 架构**: 能力不足时自动调用外部方法论（BMad Method）
- 📊 **进化追踪**: 完整的进化日志和统计（`ai-as-me evolve stats`）
- 🔧 **OpenCode 集成**: 完整 MVP 工具栈（OpenCode + Claude Code）
- 🤖 **Agent 集成**: 统一的 AI Agent 执行接口，支持多种 AI 编程助手

### v2.3 功能
- 🎯 **任务优先级**: P1/P2/P3优先级管理
- 📊 **执行历史**: 任务执行记录和统计
- ⚡ **批量操作**: 批量更新和删除任务
- 📚 **API文档**: 完整的OpenAPI文档 (/docs)
- 🔍 **健康检查**: 组件级健康状态监控
- 📱 **响应式设计**: 移动端优化

### 核心功能
- 🧠 **灵魂系统**: 通过 profile/rules/mission 定义 AI 个性
- 🤖 **智能工具选择**: 自动选择最适合的AI工具
- 📋 **Web仪表板**: 实时任务管理和监控
- 🔄 **Agentic RAG**: 从历史经验学习
- 💬 **混合澄清**: 任务执行前的智能确认
- 📊 **执行追踪**: 完整的日志和透明度

## 快速开始

### 一键部署

```bash
bash scripts/setup.sh
```

这将自动：
- 安装 Python 依赖
- 创建运行时目录
- 生成配置文件模板
- （可选）配置 systemd 服务

### 手动安装

```bash
# 安装依赖
pip install -e .

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 启动 Web 仪表板
python -m ai_as_me.cli_main serve
```

## v3.0 新功能使用

### Agent 执行

```bash
# 列出所有可用的 agents
ai-as-me agent list

# 执行任务（自动选择 agent）
ai-as-me agent execute <task_id>

# 指定 agent 执行
ai-as-me agent execute <task_id> --agent opencode

# 不触发进化
ai-as-me agent execute <task_id> --no-evolution
```

### 查看进化统计

```bash
ai-as-me evolve stats --days 7
```

### 查看进化历史

```bash
ai-as-me evolve history --limit 10
```

### 检查 Soul 状态

```bash
ai-as-me soul status
```

### 查看学习的规则

```bash
ls soul/rules/learned/
```

### 访问

- **Web Dashboard**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

详细部署说明见 [docs/deployment.md](docs/deployment.md)

### 配置

创建 `.env` 文件：

```bash
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_API_BASE=https://api.deepseek.com/v1
```

完整环境变量说明见 [docs/environment-variables.md](docs/environment-variables.md)

### 使用

```bash
# 查看帮助
ai-as-me --help

# 查看系统状态
ai-as-me status

# 启动 Agent
ai-as-me run
```

### systemd 服务（可选）

```bash
# 启动服务
systemctl --user start ai-as-me

# 查看状态
systemctl --user status ai-as-me

# 查看日志
journalctl --user -u ai-as-me -f

# 停止服务
systemctl --user stop ai-as-me
```

## 目录结构

```
ai-as-me/
├── src/ai_as_me/    # 源代码
├── soul/            # 灵魂文件 (profile/rules/mission)
├── kanban/          # 任务看板 (inbox/todo/doing/done)
└── logs/            # 执行日志
```

## 开发

本项目使用 BMad Method 进行开发。

## License

MIT
