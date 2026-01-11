# Story 1.1: 项目初始化与目录结构

**Story Key:** 1-1-project-init-directory-structure  
**Epic:** Epic 1 - 系统基础与 CLI  
**Status:** ready-for-dev  
**Created:** 2026-01-11  
**Sprint:** Sprint 1

## User Story

As a **开发者**,  
I want **初始化 AI-as-Me 项目结构**,  
So that **所有模块有统一的代码组织和依赖管理**.

## Acceptance Criteria

**Given** 空的项目目录  
**When** 执行初始化脚本  
**Then** 创建完整的 src layout 结构  
**And** pyproject.toml 包含所有依赖声明  
**And** 运行时目录 (soul/, kanban/, logs/) 被创建

## Technical Details

### 目录结构

```
ai-as-me/
├── src/
│   └── ai_as_me/
│       ├── __init__.py
│       ├── cli/              # CLI 命令模块
│       │   ├── __init__.py
│       │   └── main.py
│       ├── core/             # 核心功能
│       │   ├── __init__.py
│       │   ├── config.py     # 配置管理
│       │   └── agent.py      # Agent 主循环
│       ├── soul/             # 灵魂文件管理
│       │   ├── __init__.py
│       │   └── loader.py
│       ├── kanban/           # 任务管理
│       │   ├── __init__.py
│       │   └── manager.py
│       ├── llm/              # LLM 客户端
│       │   ├── __init__.py
│       │   └── client.py
│       ├── clarify/          # 澄清模块
│       │   ├── __init__.py
│       │   └── analyzer.py
│       ├── logger/           # 日志模块
│       │   ├── __init__.py
│       │   └── tracker.py
│       └── reflect/          # 反思模块
│           ├── __init__.py
│           └── extractor.py
├── soul/                     # 运行时灵魂文件
│   ├── profile.md
│   ├── rules.md
│   └── mission.md
├── kanban/                   # 运行时任务看板
│   ├── inbox/
│   ├── todo/
│   ├── doing/
│   └── done/
├── logs/                     # 运行时日志
├── pyproject.toml
├── .env.example
├── .gitignore
└── README.md
```

### pyproject.toml 依赖

```toml
[project]
name = "ai-as-me"
version = "0.1.0"
description = "Personal AI Agent with Soul"
requires-python = ">=3.10"
dependencies = [
    "openai>=1.0.0",
    "python-dotenv>=1.0.0",
    "click>=8.0.0",
    "pydantic>=2.0.0",
    "pyyaml>=6.0.0",
]

[project.scripts]
ai-as-me = "ai_as_me.cli.main:cli"

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"
```

## Implementation Tasks

1. 创建目录结构
2. 创建 pyproject.toml
3. 创建 .gitignore (排除 .env, logs/, __pycache__)
4. 创建运行时目录 (soul/, kanban/, logs/)
5. 创建基础 __init__.py 文件
6. 创建 README.md 说明文档

## Definition of Done

- [ ] 所有目录和文件已创建
- [ ] pyproject.toml 配置正确
- [ ] 可以执行 `pip install -e .` 安装项目
- [ ] .gitignore 正确排除敏感文件
- [ ] README.md 包含基本使用说明

## Notes

- 使用 src layout 以避免导入问题
- 运行时目录在项目根目录，便于用户访问
- 遵循 Python 包管理最佳实践
