# Architecture v3.4.4 - Agent 模型自动化配置

## 系统架构

```
┌─────────────────────────────────────────────────┐
│           AI-as-Me CLI / Orchestrator           │
└────────────────┬────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────┐
│          Agent Manager (agent_manager.py)       │
│  - 统一入口                                      │
│  - 路由选择                                      │
└────────┬───────────────────────┬─────────────────┘
         │                       │
         v                       v
┌────────────────────┐  ┌────────────────────────┐
│  OpenCode Agent    │  │  Claude Code Agent     │
└────────┬───────────┘  └────────┬───────────────┘
         │                       │
         v                       v
┌────────────────────┐  ┌────────────────────────┐
│ Model Detector     │  │  Model Selector        │
│ (detect_*.py)      │  │  (select_*.py)         │
└────────┬───────────┘  └────────┬───────────────┘
         │                       │
         v                       v
┌────────────────────┐  ┌────────────────────────┐
│ Model Query        │  │  Model Query           │
│ (query_*.py)       │  │  (query_*.py)          │
└────────┬───────────┘  └────────┬───────────────┘
         │                       │
         v                       v
┌────────────────────┐  ┌────────────────────────┐
│  npx opencode-ai   │  │ npx claude-code        │
│  models            │  │ --help                 │
└────────────────────┘  └────────────────────────┘
```

## 核心组件

### 1. Agent Manager
- **职责**: 统一管理 OpenCode 和 Claude Code
- **输入**: 任务描述 + Agent 类型
- **输出**: 执行结果 + 使用的模型

### 2. Model Detector (OpenCode)
- **职责**: 检测可用的免费模型
- **方法**: 调用 `query_opencode_models.py`
- **输出**: 首选模型名称

### 3. Model Selector (Claude)
- **职责**: 根据任务复杂度选择模型
- **方法**: 分析 prompt → 分类任务 → 选择模型
- **输出**: haiku / sonnet / opus

### 4. Model Query
- **OpenCode**: `npx opencode-ai models`
- **Claude**: 解析 `--help` 输出

## 数据流

```
用户任务
  ↓
Agent Manager
  ↓
[OpenCode 路径]              [Claude 路径]
  ↓                           ↓
Detect Models               Classify Task
  ↓                           ↓
Query OpenCode              Query Claude Models
  ↓                           ↓
Select First Free           Select by Complexity
  ↓                           ↓
Execute with Model          Execute with Model
  ↓                           ↓
Return Result               Return Result
```

## 配置管理

### OpenCode
- **配置文件**: `.opencode/config.yaml`
- **格式**: `provider/model`
- **示例**: `opencode/big-pickle`

### Claude Code
- **配置方式**: 命令行参数 `--model`
- **格式**: 别名 (haiku/sonnet/opus)
- **动态选择**: 运行时决定

## 扩展性

### 新增 Provider
1. 创建 `query_<provider>_models.py`
2. 更新 `detect_<provider>_models.py`
3. 在 `agent_manager.py` 添加路由

### 新增选择策略
1. 修改 `select_claude_model.py` 的 `classify_task()`
2. 添加新的复杂度判断规则

## 技术栈

- **语言**: Python 3.10+
- **依赖**: subprocess, json, requests
- **外部工具**: npx, opencode-ai, claude-code
