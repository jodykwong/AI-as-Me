# UX Design v3.4.4 - Agent 模型自动化配置

## 1. 设计目标

### 1.1 用户目标
- 快速配置 Agent 模型
- 无需了解模型细节
- 自动化程度高

### 1.2 设计原则
- **自动化优先**: 默认行为无需用户干预
- **透明可控**: 用户可查看和覆盖自动选择
- **简单直观**: 命令行界面清晰易懂

## 2. 用户流程

### 2.1 OpenCode 配置流程

```
用户启动系统
    ↓
系统自动检测可用模型
    ↓
[有可用模型]          [无可用模型]
    ↓                     ↓
自动配置首选模型      提示用户配置 API Key
    ↓                     ↓
显示配置结果          显示配置指南
    ↓
完成
```

#### 交互示例

```bash
$ python3 scripts/detect_opencode_models.py

✓ 检测到 5 个可用模型:
  1. opencode/big-pickle (推荐)
  2. opencode/glm-4.7-free
  3. opencode/grok-code
  4. opencode/minimax-m2.1-free
  5. opencode/gpt-5-nano

✓ 已配置首选模型: opencode/big-pickle
```

### 2.2 Claude 模型选择流程

```
用户提交任务
    ↓
系统分析任务复杂度
    ↓
[简单]    [常规]    [复杂]
  ↓         ↓         ↓
haiku    sonnet     opus
  ↓         ↓         ↓
执行任务
  ↓
显示结果 + 使用的模型
```

#### 交互示例

```bash
$ echo "Fix typo in README" | python3 scripts/select_claude_model.py
haiku

$ echo "Refactor authentication system with OAuth2..." | python3 scripts/select_claude_model.py
sonnet
```

### 2.3 统一 Agent 调用流程

```
用户指定 Agent 和任务
    ↓
Agent Manager 路由
    ↓
[OpenCode]              [Claude]
    ↓                      ↓
检测模型                分析复杂度
    ↓                      ↓
执行任务                执行任务
    ↓                      ↓
返回结果 + 模型信息
```

#### 交互示例

```bash
$ echo "Create login page" | python3 scripts/agent_manager.py opencode

{
  "output": "...",
  "model": "opencode/big-pickle"
}

$ echo "Review security" | python3 scripts/agent_manager.py claude

{
  "output": "...",
  "model": "sonnet"
}
```

## 3. 界面设计

### 3.1 命令行界面

#### 查询模型
```bash
# OpenCode
$ python3 scripts/query_opencode_models.py
[
  "opencode/big-pickle",
  "opencode/glm-4.7-free",
  ...
]

# Claude
$ python3 scripts/query_claude_models.py
["sonnet", "opus"]
```

#### 检测和选择
```bash
# OpenCode 检测
$ python3 scripts/detect_opencode_models.py
{
  "model": "opencode/big-pickle",
  "available": [...]
}

# Claude 选择
$ echo "task description" | python3 scripts/select_claude_model.py
sonnet
```

#### 统一调用
```bash
# 基本用法
$ echo "task" | python3 scripts/agent_manager.py <opencode|claude>

# 带详细输出
$ echo "task" | python3 scripts/agent_manager.py opencode --verbose
```

### 3.2 配置文件界面

#### .opencode/config.yaml
```yaml
version: 1
project:
  name: AI-as-Me
  type: python

settings:
  model: opencode/big-pickle  # 自动配置
  temperature: 0
  max_iterations: 50
```

### 3.3 错误处理界面

#### 无可用模型
```bash
$ python3 scripts/detect_opencode_models.py

✗ 错误: 未检测到可用模型

请配置以下任一 API Key:
  - OPENCODE_API_KEY (推荐)
  - XAI_API_KEY
  - ZHIPU_API_KEY
  - MINIMAX_API_KEY

配置方法:
  export OPENCODE_API_KEY=your_key

获取 API Key:
  https://opencode.ai/auth
```

#### 网络错误
```bash
$ python3 scripts/query_opencode_models.py

✗ 错误: 无法连接到 OpenCode 服务

请检查:
  1. 网络连接
  2. npx 是否已安装
  3. opencode-ai 是否可用

重试: python3 scripts/query_opencode_models.py
```

## 4. 信息架构

### 4.1 脚本组织
```
scripts/
├── query_opencode_models.py    # 查询 OpenCode 模型
├── detect_opencode_models.py   # 检测首选模型
├── query_claude_models.py      # 查询 Claude 别名
├── select_claude_model.py      # 智能选择模型
└── agent_manager.py             # 统一管理器
```

### 4.2 配置层次
```
全局配置 (.opencode/config.yaml)
    ↓
环境变量 (OPENCODE_API_KEY)
    ↓
命令行参数 (--model)
    ↓
运行时检测 (自动)
```

## 5. 交互细节

### 5.1 反馈机制

#### 成功反馈
- ✓ 绿色勾号
- 清晰的成功消息
- 显示配置结果

#### 错误反馈
- ✗ 红色叉号
- 明确的错误原因
- 可操作的解决方案

#### 进度反馈
- 查询中...
- 检测中...
- 执行中...

### 5.2 帮助信息

```bash
$ python3 scripts/agent_manager.py --help

Usage: agent_manager.py <agent> [options]

Arguments:
  agent          Agent type: opencode | claude

Options:
  --verbose      Show detailed output
  --help         Show this help message

Examples:
  echo "task" | python3 scripts/agent_manager.py opencode
  echo "task" | python3 scripts/agent_manager.py claude --verbose
```

## 6. 可访问性

### 6.1 命令行友好
- 支持管道输入
- 支持标准输出
- 支持 JSON 格式

### 6.2 脚本可组合
- 每个脚本单一职责
- 输出格式统一
- 易于集成到其他工具

## 7. 未来改进

### 7.1 Web UI
- 可视化模型选择
- 实时配置预览
- 历史记录查看

### 7.2 交互式配置
- 引导式配置向导
- 自动测试连接
- 推荐最优配置

### 7.3 监控面板
- 模型使用统计
- 成本追踪
- 性能分析
