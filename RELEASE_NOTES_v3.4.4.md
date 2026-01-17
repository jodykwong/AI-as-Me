# Release Notes v3.4.4

## 版本信息
- **版本号**: v3.4.4
- **发布日期**: 2026-01-17
- **类型**: Agent 模型自动化配置

## 新增功能

### Agent 模型自动化配置
- **OpenCode 免费模型自动检测**: 实时查询可用的免费模型列表
- **Claude Code 智能模型选择**: 根据任务复杂度自动选择 Haiku/Sonnet/Opus
- **动态模型查询**: 从工具本身获取最新支持的模型，避免硬编码过期

## 核心改进

### 1. OpenCode 配置
- 实现 `query_opencode_models.py`: 通过 `opencode models` 命令实时查询
- 实现 `detect_opencode_models.py`: 自动检测可用的免费模型
- 配置文件更新为正确格式: `opencode/big-pickle`

### 2. Claude Code 配置
- 实现 `query_claude_models.py`: 从 `--help` 提取支持的模型别名
- 实现 `select_claude_model.py`: 根据任务复杂度智能选择模型
  - 简单任务 (< 50 词): haiku
  - 常规任务: sonnet
  - 复杂任务 (> 200 词): opus

### 3. 统一管理
- 实现 `agent_manager.py`: 统一入口管理 OpenCode 和 Claude Code
- 支持动态模型查询，确保始终使用最新可用模型

## 技术细节

### 新增脚本
```
scripts/
├── query_opencode_models.py   # OpenCode 模型查询
├── detect_opencode_models.py  # OpenCode 模型检测
├── query_claude_models.py     # Claude 模型查询
├── select_claude_model.py     # Claude 模型选择
└── agent_manager.py            # 统一 Agent 管理器
```

### 配置更新
- `.opencode/config.yaml`: 模型名称从 `anthropic/claude-sonnet-4-20250514` 更新为 `opencode/big-pickle`

## 使用方法

### 查询可用模型
```bash
# OpenCode 模型
python3 scripts/query_opencode_models.py

# Claude 模型
python3 scripts/query_claude_models.py
```

### 智能选择模型
```bash
# 根据任务选择 Claude 模型
echo "Fix bug in login" | python3 scripts/select_claude_model.py
# 输出: haiku

echo "Refactor authentication system..." | python3 scripts/select_claude_model.py
# 输出: sonnet
```

### 调用 Agent
```bash
# 使用 OpenCode
echo "your task" | python3 scripts/agent_manager.py opencode

# 使用 Claude
echo "your task" | python3 scripts/agent_manager.py claude
```

## 验收清单

- [x] OpenCode 自动检测可用模型
- [x] Claude Code 根据任务复杂度选择模型
- [x] 动态查询确保模型名称正确
- [x] 配置文件更新为正确格式
- [x] 所有脚本可执行且测试通过

## 下一步计划

- 集成到 AI-as-Me CLI
- 添加 fallback 机制
- 实现成本追踪
- 添加配置管理界面

## 贡献者
- BMad Master
