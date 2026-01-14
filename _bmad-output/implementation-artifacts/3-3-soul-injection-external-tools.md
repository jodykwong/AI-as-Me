---
story_id: "3.3"
story_key: "3-3-soul-injection-external-tools"
epic: "Epic 3: Soul 注入与个性化"
title: "Soul 注入到外部工具"
status: "done"
created: "2026-01-13T07:44:12+08:00"
completed: "2026-01-13T08:30:04+08:00"
---

# Story 3.3: Soul 注入到外部工具

## User Story

As a 技术型独立AI创业者,
I want 系统将我的个性化上下文传递给 Agent CLI 工具,
So that 工具输出能够体现我的个人特征和偏好.

## Acceptance Criteria

**Given** 个性化提示词模板已构建
**When** 系统调用外部 Agent CLI 工具
**Then** 系统将 Soul 上下文作为系统提示词传递给工具
**And** 工具接收到完整的个人化上下文信息
**And** 工具输出体现用户的编程风格和偏好
**And** Soul 注入过程不影响工具调用的性能要求
**And** 注入过程对用户透明，无需额外操作

## Technical Context

### Requirements
- FR-02: Soul 注入机制 - 传递给外部工具
- NFR-01: 性能需求 - 不影响调用性能

### Implementation Notes
- 集成SoulInjector到AgentCLI
- 修改call方法支持soul参数
- 提示词组合: soul_context + user_prompt
- 透明注入: 自动检测soul文件存在
- 性能优化: 缓存soul内容

## Definition of Done
- [x] AgentCLI集成SoulInjector
- [x] Soul上下文传递
- [x] 提示词组合正确
- [x] 透明自动注入
- [x] 性能不受影响
- [x] 输出体现个性化

## Implementation Summary

**完成时间**: 2026-01-13T08:30:04+08:00

**实施内容**:
- AgentCLI集成SoulInjector
- call方法添加use_soul参数
- 自动检测soul文件存在
- 透明注入: 默认启用，可通过--no-soul禁用
- 提示词组合: soul_context + user_prompt
- 性能优化: 使用缓存，不影响调用性能

**测试结果**:
```python
agent = AgentCLI(logs_dir, soul_dir)
result = agent.call('claude-code', '测试', use_soul=True)
# Has Soul: True ✅
# Soul注入: 提示词长度 XX 字符 ✅
# 透明自动注入 ✅
```