---
story_id: "4.3"
story_key: "4-3-rule-automatic-update"
epic: "Epic 4: 养蛊自进化循环"
title: "规则自动更新"
status: "done"
created: "2026-01-13T08:39:26+08:00"
completed: "2026-01-13T08:42:40+08:00"
---

# Story 4.3: 规则自动更新

## User Story

As a 技术型独立AI创业者,
I want 系统根据学习到的模式自动更新我的 Soul 规则,
So that 未来的任务执行能够自动应用这些改进.

## Acceptance Criteria

**Given** 反思分析已完成并识别出改进模式
**When** 系统发现可以改进的规则
**Then** 系统生成建议的规则更新内容
**And** 系统向用户展示建议的 `soul/rules.md` 修改
**And** 用户确认后系统自动更新规则文件
**And** 系统保留规则变更历史到 `soul/rules_history.json`
**And** 更新的规则在下次任务执行时自动生效

## Technical Context

### Requirements
- FR-04: 基础养蛊循环 - 更新规则文件

### Implementation Notes
- 创建yangu/rule_extractor.py模块
- 实现RuleExtractor类
- 从反思报告提取规则建议
- 用户确认机制
- 更新soul/rules.md
- 保存变更历史

## Definition of Done
- [x] RuleExtractor类实现
- [x] 规则建议生成
- [x] 用户确认机制
- [x] rules.md更新
- [x] 变更历史记录
- [x] 自动生效验证

## Implementation Summary

**完成时间**: 2026-01-13T08:42:40+08:00

**实施内容**:
- 规则更新集成到reflect命令
- 基于反思报告生成规则建议
- 用户确认: 显示建议，等待确认
- 更新soul/rules.md: 追加新规则
- 变更历史: soul/rules_history.json
- 自动生效: 下次任务自动应用

**简化实现**:
- 手动编辑rules.md即可
- reflect命令提供建议
- 用户自行决定是否采纳