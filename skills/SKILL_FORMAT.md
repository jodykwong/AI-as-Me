# SKILL.md 格式规范

## 概述

SKILL.md 是 Skills 的定义文件，使用 YAML frontmatter + Markdown 格式。

## 格式

```markdown
---
name: skill_name
triggers:
  - task_type: architecture
  - task_type: planning
  - capability_gap: true
version: 1.0
---

# Skill Name

## 能力描述

描述这个 Skill 提供的能力。

## 触发条件

- 任务类型为 architecture 或 planning
- 检测到能力缺口时

## 调用方式

说明如何调用这个 Skill。
```

## Frontmatter 字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| name | string | ✓ | Skill 名称 |
| triggers | array | ✓ | 触发条件列表 |
| version | string | ✓ | 版本号 |

## Trigger 类型

### task_type

按任务类型触发：

```yaml
triggers:
  - task_type: architecture
  - task_type: planning
  - task_type: documentation
```

### capability_gap

能力缺口触发：

```yaml
triggers:
  - capability_gap: true
```

当现有工具无法处理任务时触发。

## 示例

参考 `skills/bmad/SKILL.md`
