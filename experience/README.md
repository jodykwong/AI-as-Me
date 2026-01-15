# Experience 目录

存储任务执行经验和识别的模式。

## 目录结构

- `successes/` - 成功执行的任务经验
- `failures/` - 失败的任务经验
- `patterns/` - 识别出的可复用模式

## 文件格式

所有文件使用 JSON 格式，文件名为 `{task_id}.json`。

### Experience 格式

```json
{
  "task_id": "task-20260115-001",
  "description": "实现 Experience Collector",
  "tool_used": "claude_code",
  "result": "成功实现，测试通过",
  "success": true,
  "duration": 3600.5,
  "timestamp": "2026-01-15T19:00:00+08:00"
}
```

### Pattern 格式

```json
{
  "pattern_id": "pattern-1",
  "description": "当任务涉及架构设计时，优先使用 BMad Method",
  "frequency": 5,
  "source_tasks": ["task-001", "task-002", "task-003"],
  "confidence": 0.85,
  "category": "工具选择"
}
```

## 使用方式

经验由 `ExperienceCollector` 自动收集，模式由 `PatternRecognizer` 识别。

## 数据保留

- 成功经验：永久保留
- 失败经验：保留用于学习
- 模式：定期更新置信度
