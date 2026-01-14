# AI-as-Me

个人 AI 代理系统，具有灵魂、记忆和自我进化能力。

## 特性

- 🧠 **灵魂系统**: 通过 profile/rules/mission 定义 AI 个性
- 📋 **任务看板**: 文件级看板管理任务流程
- 🤖 **LLM 驱动**: 智能任务执行和结果生成
- 💬 **混合澄清**: 任务执行前的智能确认
- 📊 **执行追踪**: 完整的日志和透明度
- 🔄 **自我进化**: 从经验中学习，积累规则

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
