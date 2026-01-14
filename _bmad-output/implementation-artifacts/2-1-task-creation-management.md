---
story_id: "2.1"
story_key: "2-1-task-creation-management"
epic: "Epic 2: Agent CLI 编排核心"
title: "任务创建和管理"
status: "done"
created: "2026-01-13T07:07:05+08:00"
completed: "2026-01-13T07:08:36+08:00"
---

# Story 2.1: 任务创建和管理

## User Story

As a 技术型独立AI创业者,
I want 通过命令行创建和管理任务,
So that 我可以组织和跟踪需要 AI 协助完成的工作.

## Acceptance Criteria

**Given** AI-as-Me 系统已初始化
**When** 用户执行 `ai-as-me task add "创建新的 API 接口"`
**Then** 系统创建新任务并分配唯一 ID
**And** 任务状态设置为 "todo"
**And** 任务信息保存到 `kanban/tasks.json` 文件
**And** 命令响应时间 < 2 秒
**And** 用户执行 `ai-as-me task list` 可以看到所有任务

## Technical Context

### Requirements
- FR-03: 任务生命周期管理 - task add/list命令
- NFR-01: 性能需求 - 命令响应<2秒

### Implementation Notes
- 实现task命令组: add, list
- 使用JSON存储任务: kanban/tasks.json
- 任务ID生成: UUID或时间戳
- 任务状态: todo, doing, done
- 数据结构: {id, description, status, created_at}

## Definition of Done
- [x] task add命令实现
- [x] task list命令实现
- [x] JSON文件存储
- [x] 唯一ID生成
- [x] 响应时间<2秒
- [x] 任务状态管理

## Implementation Summary

**完成时间**: 2026-01-13T07:08:36+08:00

**实施内容**:
- 创建TaskManager类: kanban/task_manager.py
- 实现task add命令: 添加任务
- 实现task list命令: 列出任务，支持--status过滤
- JSON存储: kanban/tasks.json
- UUID生成: 8位短ID
- 任务数据结构: {id, description, status, created_at}

**测试结果**:
```
$ ai-as-me task add "实现API接口"
✅ 任务已创建
   ID: a5a6b03d
   状态: todo

$ ai-as-me task list
📋 任务列表 (2 个任务)
⏳ [a5a6b03d] 实现API接口
   状态: todo | 创建: 2026-01-13T07:09:45
```