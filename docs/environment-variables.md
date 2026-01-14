# Environment Variables Documentation

## Story 12.3: 环境变量说明

### Database

| Variable | Default | Description |
|----------|---------|-------------|
| `AI_AS_ME_DB` | `data/tasks.db` | 主数据库路径 |
| `AI_AS_ME_FEEDBACK_DB` | `~/.ai-as-me/feedback.db` | 反馈权重数据库路径 |

### RAG

| Variable | Default | Description |
|----------|---------|-------------|
| `AI_AS_ME_RAG_DIR` | `~/.ai-as-me/rag` | RAG向量存储目录 |

### Tools

| Variable | Default | Description |
|----------|---------|-------------|
| `AI_AS_ME_TOOLS_CONFIG` | `config/agents.yaml` | 工具配置文件路径 |

### API

| Variable | Default | Description |
|----------|---------|-------------|
| `AI_AS_ME_CONFIG` | `config/settings.yaml` | 主配置文件路径 |

### Logging

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | 日志级别 (DEBUG/INFO/WARNING/ERROR) |

## Usage

```bash
# 复制示例文件
cp .env.example .env

# 编辑配置
vim .env

# 运行应用
python -m ai_as_me.cli_main serve
```
