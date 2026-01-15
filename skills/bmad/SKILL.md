---
name: bmad
triggers:
  - task_type: architecture
  - task_type: planning
  - capability_gap: true
version: 1.0
---

# BMad Method Skill

## 能力描述

BMad Method 提供完整的软件开发方法论支持，包括：

- **产品分析**（Product Brief）- 从想法到产品定义
- **需求规划**（PRD）- 详细需求文档
- **架构设计**（Architecture）- 技术架构决策
- **任务分解**（Epics & Stories）- 可执行的开发任务

## 触发条件

1. **任务类型匹配**
   - 任务类型为 `architecture`（架构设计）
   - 任务类型为 `planning`（规划类任务）

2. **能力缺口检测**
   - 当现有工具（Claude Code, OpenCode 等）无法处理任务时
   - 任务复杂度超出常规工具能力范围

## 调用方式

### 自动调用

当满足触发条件时，系统自动加载 BMad Method 工作流：

```
_bmad/bmm/workflows/
├── 1-analysis/          # 产品分析
├── 2-plan-workflows/    # 需求规划
├── 3-solutioning/       # 架构设计
└── 4-implementation/    # 实施规划
```

### 手动调用

通过 CLI 命令手动触发：

```bash
# 产品分析
ai-as-me bmad analyze

# 需求规划
ai-as-me bmad plan

# 架构设计
ai-as-me bmad architect
```

## 工作流程

```
用户任务
    │
    ▼
能力判断 ──No──▶ 常规工具处理
    │
   Yes
    ▼
加载 BMad Skill
    │
    ▼
选择工作流
    │
    ├─▶ 1-analysis (产品分析)
    ├─▶ 2-plan (需求规划)
    ├─▶ 3-solutioning (架构设计)
    └─▶ 4-implementation (实施规划)
    │
    ▼
生成产物
```

## 产物输出

所有产物输出到 `_bmad-output/` 目录：

- `planning-artifacts/` - 规划文档
- `implementation-artifacts/` - 实施文档

## 集成说明

BMad Skill 与 AI-as-Me 核心系统集成：

1. **Soul 系统** - 遵循 Soul 定义的规则和偏好
2. **Experience 系统** - 执行结果记录到 experience/
3. **Evolution 系统** - 从 BMad 执行中学习和进化

## 版本历史

- v1.0 (2026-01-15) - 初始版本
