# OpenCode 集成说明

## 概述

AI-as-Me 已完整集成 OpenCode，作为 MVP 工具栈的一部分（OpenCode + Claude Code）。

## 配置文件

- `.opencode/config.yaml` - 全局配置
- `.opencode/agents/default.md` - 默认 agent 定义

## 使用方式

### 启动 OpenCode

```bash
npx opencode-ai@1.1.3
```

### 自定义命令

在 OpenCode 中可以使用以下命令：

- `/soul-check` - 检查 Soul 状态
- `/evolve-stats` - 查看进化统计
- `/evolve-history` - 查看进化历史
- `/serve` - 启动 Web Dashboard

### Agent 配置

默认 agent 会自动加载：
- Soul 文件（profile, mission, rules）
- 进化能力（自动学习）
- Skills 机制（能力扩展）

## 与 Claude Code 的互补

| 工具 | 定位 | 优势 |
|------|------|------|
| **OpenCode** | 开源 AI 编程代理 | 多模型支持、终端优先 |
| **Claude Code** | Anthropic 官方工具 | L4 级 Agent、原生 Skills |

两者互补使用，覆盖不同场景。

## 验证

检查 OpenCode 是否可用：

```bash
ai-as-me check-tools
```

## 文档

- OpenCode 官方文档: https://github.com/opencode-ai/opencode
- AI-as-Me 文档: README.md
