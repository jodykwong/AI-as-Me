---
story_id: "3.2"
story_key: "3-2-prompt-template-construction"
epic: "Epic 3: Soul 注入与个性化"
title: "提示词模板构建"
status: "done"
created: "2026-01-13T07:44:12+08:00"
completed: "2026-01-13T08:01:18+08:00"
---

# Story 3.2: 提示词模板构建

## User Story

As a 技术型独立AI创业者,
I want 系统基于我的 Soul 数据构建个性化提示词,
So that 外部 AI 工具能够按照我的风格和偏好工作.

## Acceptance Criteria

**Given** Soul 文件已创建并包含用户数据
**When** 系统准备调用外部工具
**Then** 系统读取 `soul/profile.md` 和 `soul/rules.md` 内容
**And** 系统构建包含个人上下文的提示词模板
**And** 模板包含用户的编程风格、偏好和约束
**And** 提示词构建过程在 5 秒内完成
**And** 构建的提示词不超过外部工具的 context window 限制

## Technical Context

### Requirements
- FR-02: Soul 注入机制 - 提示词模板构建
- NFR-01: 性能需求 - 构建时间<5秒

### Implementation Notes
- 创建soul_injector.py模块
- 实现SoulInjector类
- 读取soul/*.md文件
- 构建提示词模板: 系统提示 + 用户任务
- 模板格式: Markdown或纯文本
- 长度控制: 截断或摘要

## Definition of Done
- [x] SoulInjector类实现
- [x] 读取soul文件
- [x] 提示词模板构建
- [x] 构建时间<5秒
- [x] 长度控制机制
- [x] 模板格式正确

## Implementation Summary

**完成时间**: 2026-01-13T08:01:18+08:00

**实施内容**:
- 创建SoulInjector类: orchestrator/soul_injector.py
- 读取soul文件: profile.md, rules.md
- 构建提示词: 个人档案 + 工作规则 + 任务
- 缓存机制: 避免重复读取
- 长度控制: max_length参数，优先保留任务和规则
- 性能优化: 缓存soul内容

**测试结果**:
```python
injector = SoulInjector(soul_dir)
prompt = injector.build_prompt('创建API接口')
# Has Soul: True ✅
# 构建时间: <0.001秒 ✅
# 格式: # 个人档案 + # 工作规则 + # 任务 ✅
```