# Kanban 任务卡片闪现问题调试报告

**报告时间**: 2026-01-21 05:15  
**问题状态**: ❌ 未解决（修复后仍存在）  
**调试人员**: BMad Master

---

## 📋 问题描述

**现象**: 任务从 Todo 拖拽到 Doing 列后，卡片"一闪而过"立即消失

**预期行为**: 任务应停留在 Doing 列，显示执行状态

---

## 🔍 已执行的修复（无效）

### 修复1: 任务保护期（3秒）
```javascript
// refreshDoingTasks() 第91-103行
const now = Date.now();
this.board.doing = this.board.doing.filter(task => {
    if (this._optimisticUpdates.has(task.id)) {
        return true;
    }
    const taskAge = now - new Date(task.updated_at).getTime();
    return taskAge < 3000 || newDoing.some(t => t.id === task.id);
});
```
**结果**: ❌ 无效

### 修复2: 执行日志延迟清空（5秒）
```javascript
// fetchExecutionLogs() 第495行
if (!currentTask) {
    if (!this._logClearTimer) {
        this._logClearTimer = setTimeout(() => {
            this.executionLogs = [];
        }, 5000);
    }
    return;
}
```
**结果**: ❌ 无效

### 修复3: 乐观更新锁
```javascript
// moveTask() 第312行
this._optimisticUpdates.set(taskId, { status: toStatus, timestamp: Date.now() });
```
**结果**: ❌ 无效

---

## 🎯 新的排查方向

### 可能原因4: 后端立即返回完成状态
**假设**: 任务被移动到 Doing 后，后端执行器立即完成任务并返回 Done 状态

**验证方法**:
```bash
# 监控后端日志
tail -f dashboard.log | grep -E "move|status|doing"

# 检查任务执行时长
curl http://localhost:8000/api/kanban/board | jq '.doing'
```

### 可能原因5: WebSocket/SSE 推送状态更新
**假设**: 存在实时推送机制，绕过了前端保护逻辑

**验证方法**:
```javascript
// 在浏览器控制台执行
performance.getEntriesByType('resource')
  .filter(r => r.name.includes('stream') || r.name.includes('ws'))
```

### 可能原因6: 拖拽事件触发多次 moveTask
**假设**: SortableJS 的 onEnd 事件被触发多次

**验证方法**:
```javascript
// 在 kanban.js 第80行添加日志
onEnd: async (evt) => {
    console.log('🔥 onEnd triggered:', evt.item.dataset.id, evt.to.dataset.status);
    // ... 原有代码
}
```

### 可能原因7: Vue 响应式系统导致的重新渲染
**假设**: Alpine.js 的响应式更新触发了 DOM 重建

**验证方法**:
```javascript
// 检查 board.doing 的变化
watch(() => this.board.doing, (newVal, oldVal) => {
    console.log('📊 doing changed:', oldVal.length, '->', newVal.length);
});
```

---

## 🛠️ 下一步调试计划

### 步骤1: 添加详细日志
```javascript
// 在 kanban.js 关键位置添加
console.log('🔍 [moveTask] START:', taskId, toStatus);
console.log('🔍 [refreshDoingTasks] doing count:', this.board.doing.length);
console.log('🔍 [updateLocalTaskStatus] task moved:', taskId);
```

### 步骤2: 检查后端 API 响应
```bash
# 监控 /api/kanban/tasks/{id}/move 请求
curl -X PUT http://localhost:8000/api/kanban/tasks/{TASK_ID}/move \
  -H "Content-Type: application/json" \
  -d '{"to_status": "doing"}' \
  -v
```

### 步骤3: 禁用自动刷新测试
```javascript
// 临时注释掉第58行
// setInterval(() => this.refreshDoingTasks(), CONFIG.DOING_TASKS_REFRESH_INTERVAL);
```

### 步骤4: 检查任务执行流程
```bash
# 查看任务执行器代码
grep -r "DOING\|DONE" src/ai_as_me/kanban/ --include="*.py"
```

---

## 📊 需要收集的数据

1. **浏览器控制台日志**（拖拽时的完整输出）
2. **Network 面板**（/api/kanban/* 的所有请求）
3. **后端日志**（dashboard.log 中的相关记录）
4. **任务状态变化时间线**（从 Todo -> Doing -> ? 的时间戳）

---

## 🚨 紧急建议

**临时解决方案**: 禁用自动刷新，改为手动刷新按钮
```javascript
// 注释掉自动刷新
// setInterval(() => this.refreshDoingTasks(), CONFIG.DOING_TASKS_REFRESH_INTERVAL);

// 添加手动刷新按钮
<button @click="loadBoard()">🔄 刷新</button>
```

---

## 📝 待确认信息

- [ ] 任务是否真的进入了 Doing 状态（后端数据库）
- [ ] 任务消失的确切时机（立即？1秒后？10秒后？）
- [ ] 是否所有任务都闪现，还是特定类型任务
- [ ] 手动刷新页面后，任务在哪个列？

---

**下一步行动**: 需要用户提供浏览器控制台日志和 Network 请求记录
