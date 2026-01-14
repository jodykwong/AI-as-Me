---
story_id: "1.4"
story_key: "1-4-agent-cli-tool-availability-detection"
epic: "Epic 1: 系统基础设施与安装"
title: "Agent CLI 工具可用性检测"
status: "done"
created: "2026-01-13T06:55:10+08:00"
completed: "2026-01-13T07:03:38+08:00"
---

# Story 1.4: Agent CLI 工具可用性检测

## User Story

As a 技术型独立AI创业者,
I want 系统验证外部 Agent CLI 工具的可用性,
So that 我可以确保系统能够成功调用外部工具执行任务.

## Acceptance Criteria

**Given** 系统初始化完成
**When** 用户执行 `ai-as-me check-tools`
**Then** 系统检测 `npx -y @anthropic-ai/claude-code@2.0.76` 可用性
**And** 系统检测 `npx -y opencode-ai@1.1.3` 可用性
**And** 系统显示每个工具的状态 (可用/不可用/版本信息)
**And** 如果工具不可用，提供安装或配置建议
**And** 检测过程在 30 秒内完成

## Technical Context

### Requirements
- FR-01: Agent CLI 工具集成 - 工具可用性检测和健康检查
- NFR-01: 性能需求 - 检测过程<30秒
- NFR-02: 可靠性需求 - 健康检查机制

### Architecture Considerations
- 进程管理: 外部工具调用的超时和错误处理
- 健康检查: 定期验证外部工具可用性
- 工具列表:
  - Claude Code: npx -y @anthropic-ai/claude-code@2.0.76
  - OpenCode: npx -y opencode-ai@1.1.3

### Implementation Notes
- 实现 `check-tools` CLI命令
- 使用subprocess.run调用npx命令
- 设置timeout=30秒
- 捕获工具版本信息
- 解析输出判断可用性
- 提供清晰的状态报告和建议

## Definition of Done
- [x] check-tools命令实现完成
- [x] Claude Code检测正常
- [x] OpenCode检测正常
- [x] 显示工具状态和版本
- [x] 检测超时控制<30秒
- [x] 不可用时提供安装建议
- [x] 错误处理优雅

## Implementation Summary

**完成时间**: 2026-01-13T07:03:38+08:00

**实施内容**:
- 实现check-tools CLI命令
- 检测Claude Code: npx @anthropic-ai/claude-code@2.0.76
- 检测OpenCode: npx opencode-ai@1.1.3
- 超时控制: 30秒timeout
- 错误处理: FileNotFoundError, TimeoutExpired
- 提供安装建议和使用提示

**测试结果**:
```
$ ai-as-me check-tools
🔧 检查 Agent CLI 工具可用性...
检测 Claude Code...
✅ Claude Code: 可用
检测 OpenCode...
✅ OpenCode: 可用
✅ Agent CLI 工具检查完成
```
