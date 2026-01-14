---
story_id: "1.3"
story_key: "1-3-initialization-config-directory-structure"
epic: "Epic 1: 系统基础设施与安装"
title: "初始化配置和目录结构"
status: "done"
created: "2026-01-13T06:55:10+08:00"
completed: "2026-01-13T07:01:54+08:00"
---

# Story 1.3: 初始化配置和目录结构

## User Story

As a 技术型独立AI创业者,
I want 系统自动创建必需的配置和目录结构,
So that 我可以立即开始使用系统而无需手动创建文件夹.

## Acceptance Criteria

**Given** 环境依赖检查通过
**When** 用户执行 `ai-as-me init`
**Then** 系统创建 `soul/` 目录结构
**And** 系统创建 `kanban/` 目录用于任务管理
**And** 系统创建 `logs/` 目录用于日志记录
**And** 系统生成默认的 `.env` 配置文件模板
**And** 所有目录权限设置为用户可读写 (700)

## Technical Context

### Requirements
- NFR-03: 安全需求 - 文件权限600/700
- NFR-04: 可用性需求 - 5分钟内完成配置
- 架构: 文件系统管理，目录结构规范

### Architecture Considerations
- 目录结构:
  - soul/ - Soul数据存储
  - kanban/ - 任务管理数据
  - logs/ - 日志文件
- 配置文件: .env模板

### Implementation Notes
- 实现 `init` CLI命令
- 使用pathlib创建目录
- 设置目录权限: os.chmod(path, 0o700)
- 生成.env模板包含必要的环境变量说明
- 检查目录是否已存在，避免覆盖

## Definition of Done
- [x] init命令实现完成
- [x] soul/目录创建成功
- [x] kanban/目录创建成功
- [x] logs/目录创建成功
- [x] .env模板生成成功
- [x] 目录权限设置为700
- [x] 已存在目录不被覆盖

## Implementation Summary

**完成时间**: 2026-01-13T07:01:54+08:00

**实施内容**:
- 实现init CLI命令
- 使用pathlib创建目录: soul/, kanban/, logs/
- 设置目录权限: os.chmod(path, 0o700)
- 生成.env模板包含API密钥配置说明
- 检查已存在目录，避免覆盖
- 提供--force选项强制重新初始化

**测试结果**:
```
$ ai-as-me init
✅ 创建 soul/ (权限: 700)
✅ 创建 kanban/ (权限: 700)
✅ 创建 logs/ (权限: 700)
✅ 创建 .env (权限: 600)
✅ 初始化完成！

$ stat -c "%a" soul kanban logs .env
700 700 700 600  ✅ 权限正确
```
