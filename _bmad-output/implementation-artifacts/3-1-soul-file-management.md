---
story_id: "3.1"
story_key: "3-1-soul-file-management"
epic: "Epic 3: Soul 注入与个性化"
title: "Soul 文件管理"
status: "done"
created: "2026-01-13T07:44:12+08:00"
completed: "2026-01-13T07:49:58+08:00"
---

# Story 3.1: Soul 文件管理

## User Story

As a 技术型独立AI创业者,
I want 创建和编辑个人 Soul 档案文件,
So that 我可以定义个人偏好和工作风格让 AI 更好地理解我.

## Acceptance Criteria

**Given** AI-as-Me 系统已初始化
**When** 用户执行 `ai-as-me soul init`
**Then** 系统创建 `soul/profile.md` 个人档案模板
**And** 系统创建 `soul/rules.md` 工作规则模板
**And** 文件权限设置为 600 (仅用户可读写)
**And** 模板包含引导性问题帮助用户填写
**And** 用户可以使用任何文本编辑器修改这些文件

## Technical Context

### Requirements
- FR-02: Soul 注入机制 - profile.md, rules.md
- NFR-03: 安全需求 - 文件权限600

### Implementation Notes
- 实现soul init命令
- 创建profile.md模板: 个人信息、编程风格、偏好
- 创建rules.md模板: 工作规则、约束条件
- 设置文件权限: os.chmod(file, 0o600)
- 模板包含引导性注释

## Definition of Done
- [x] soul init命令实现
- [x] profile.md模板创建
- [x] rules.md模板创建
- [x] 文件权限600
- [x] 引导性模板内容
- [x] 可编辑验证

## Implementation Summary

**完成时间**: 2026-01-13T07:49:58+08:00

**实施内容**:
- 实现soul init命令
- 创建profile.md模板: 基本信息、编程风格、工作偏好
- 创建rules.md模板: 代码规则、项目规则、质量规则
- 设置文件权限: os.chmod(file, 0o600)
- 引导性注释: 帮助用户填写
- --force选项: 覆盖已存在文件

**测试结果**:
```
$ ai-as-me soul init
✅ 创建 soul/profile.md (权限: 600)
✅ 创建 soul/rules.md (权限: 600)
✅ Soul初始化完成！

$ stat -c "%a" soul/*.md
600 600  ✅ 权限正确
```