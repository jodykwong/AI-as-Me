---
story_id: "2.4"
story_key: "2-4-error-handling-recovery-mechanism"
epic: "Epic 2: Agent CLI 编排核心"
title: "错误处理和恢复机制"
status: "done"
created: "2026-01-13T07:07:05+08:00"
completed: "2026-01-13T07:41:04+08:00"
---

# Story 2.4: 错误处理和恢复机制

## User Story

As a 技术型独立AI创业者,
I want 系统能够处理工具调用失败的情况,
So that 我的工作流程不会因为单个工具问题而中断.

## Acceptance Criteria

**Given** 主要 Agent CLI 工具不可用或调用失败
**When** 系统尝试执行任务
**Then** 系统在 10 秒内检测到失败
**And** 系统自动尝试备用工具 (Claude Code ↔ OpenCode)
**And** 如果所有工具都失败，任务状态设置为 "failed"
**And** 错误信息记录到日志文件
**And** 用户收到明确的错误提示和建议解决方案

## Technical Context

### Requirements
- NFR-02: 可靠性需求 - 故障恢复<10秒
- 架构: 降级机制 - 备用工具切换

### Implementation Notes
- 实现工具失败检测
- 备用工具列表: [Claude Code, OpenCode]
- 重试逻辑: 切换到下一个工具
- 失败状态: failed
- 错误日志: 详细错误信息和堆栈
- 用户提示: 清晰的错误消息

## Definition of Done
- [x] 失败检测机制
- [x] 备用工具切换
- [x] 10秒内检测失败
- [x] failed状态设置
- [x] 错误日志记录
- [x] 用户错误提示

## Implementation Summary

**完成时间**: 2026-01-13T07:41:04+08:00

**实施内容**:
- 实现call_with_fallback方法
- 备用工具列表: [claude-code, opencode]
- 自动切换逻辑: 失败时尝试下一个工具
- 失败检测: timeout=10秒
- 状态设置: failed
- 详细日志: 记录每次尝试
- 用户提示: 建议和解决方案

**测试结果**:
```python
result = agent.call_with_fallback('test', timeout=5)
# Attempts: 2 ✅
# Attempt 1: claude-code - Failed
# Attempt 2: opencode - Failed
# 所有工具调用失败 ✅
```