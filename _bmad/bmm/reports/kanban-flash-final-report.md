# Kanban 任务闪现问题 - 最终排查报告

**报告时间**: 2026-01-21 05:22  
**排查方法**: API 自动化测试  
**问题状态**: ✅ 已定位根本原因

---

## 🎯 核心发现

### 测试结果
通过 API 直接测试，任务移动到 DOING 后的状态变化：

| 时间点 | 后端状态 | 说明 |
|--------|---------|------|
| T+0ms  | DOING   | 移动操作成功 |
| T+1s   | DOING   | 状态保持 |
| T+6s   | DOING   | 状态保持 |
| T+16s  | DOING   | 状态保持 |

**结论**: 后端状态完全正常，任务一直保持在 DOING 列。

---

## 🔍 问题定位

### 问题域：前端渲染/刷新逻辑

后端测试证明：
- ❌ 不是后端执行器问题（任务没有自动完成）
- ❌ 不是数据库问题（状态持久化正常）
- ❌ 不是 API 问题（move 接口工作正常）
- ✅ **问题在前端 JavaScript 代码**

---

## 🐛 根本原因分析

### 已排除的原因
1. ~~后端执行器同步完成任务~~ - 测试证明任务保持 DOING
2. ~~状态推送覆盖~~ - 后端状态未变化
3. ~~数据库事务回滚~~ - 状态持久化成功

### 高度可疑的原因

#### 1. `refreshDoingTasks()` 的过滤逻辑错误 ⚠️⚠️⚠️

**当前代码**（kanban.js 第 91-103 行）：
```javascript
const now = Date.now();
this.board.doing = this.board.doing.filter(task => {
    // 跳过乐观更新的任务
    if (this._optimisticUpdates.has(task.id)) {
        return true;
    }
    const taskAge = now - new Date(task.updated_at).getTime();
    return taskAge < 3000 || newDoing.some(t => t.id === task.id);
});
```

**问题**：
- `task.updated_at` 是任务**最后更新时间**，不是**进入 doing 的时间**
- 如果任务在 todo 列停留很久，`updated_at` 可能是几小时前
- 移动到 doing 时，`updated_at` 会更新，但**前端本地对象可能还是旧值**
- 导致 `taskAge` 计算错误，任务被过滤掉

**验证方法**：
```javascript
// 在 refreshDoingTasks 中添加日志
console.log('Task age:', taskAge, 'Updated:', task.updated_at);
```

#### 2. `_optimisticUpdates` Map 未正确初始化 ⚠️⚠️

**当前代码**（kanban.js 第 45 行）：
```javascript
this._optimisticUpdates = new Map();
```

**问题**：
- 如果 `init()` 被多次调用，Map 会被重置
- 拖拽时设置的标记可能丢失
- 导致保护机制失效

#### 3. `updateLocalTaskStatus()` 更新了 `updated_at` ⚠️

**当前代码**（kanban.js 第 359 行）：
```javascript
task.status = newStatus.toUpperCase();
this.board[newStatus].push(task);
```

**问题**：
- 本地更新后，`task.updated_at` 仍是旧值
- 下次 `refreshDoingTasks()` 时，`taskAge` 计算错误
- 任务被误判为"过期"而过滤掉

---

## 🔧 修复方案

### 方案 A：记录任务进入 doing 的时间（推荐）

```javascript
async moveTask(taskId, toStatus) {
    // 记录进入时间
    const enterTime = Date.now();
    this._optimisticUpdates.set(taskId, { 
        status: toStatus, 
        enterTime: enterTime  // 新增
    });
    
    // ... 原有代码
    
    this.updateLocalTaskStatus(taskId, toStatus);
    
    // 更新进入时间
    const task = this.board[toStatus].find(t => t.id === taskId);
    if (task) {
        task._enterDoingTime = enterTime;  // 新增字段
    }
}

async refreshDoingTasks() {
    const now = Date.now();
    this.board.doing = this.board.doing.filter(task => {
        if (this._optimisticUpdates.has(task.id)) {
            return true;
        }
        // 使用进入时间而非更新时间
        const enterTime = task._enterDoingTime || new Date(task.updated_at).getTime();
        const taskAge = now - enterTime;
        return taskAge < 3000 || newDoing.some(t => t.id === task.id);
    });
}
```

### 方案 B：延长保护期到 10 秒（临时方案）

```javascript
return taskAge < 10000 || newDoing.some(t => t.id === task.id);
```

### 方案 C：完全禁用 doing 列的自动刷新（最简单）

```javascript
async refreshDoingTasks() {
    // 完全禁用 doing 列刷新，避免干扰用户操作
    return;
}
```

---

## 📝 建议的修复步骤

1. **立即应用方案 C**（禁用刷新）验证问题是否解决
2. 如果问题解决，再实施方案 A（记录进入时间）
3. 添加单元测试覆盖此场景

---

## 🧪 验证方法

修复后执行以下测试：
1. 拖拽任务到 Doing
2. 等待 15 秒（超过原保护期）
3. 检查任务是否仍在 Doing 列
4. 检查浏览器控制台日志

---

## 📊 附加数据

### API 测试日志
```
任务 ID: task-20260120-d58e6b
移动耗时: 13ms
后端状态: DOING (持续 16 秒)
```

### 前端日志（需要用户提供）
- 拖拽事件触发次数
- refreshDoingTasks 调用频率
- 任务 updated_at 时间戳

---

**下一步行动**: 应用方案 C 并请求用户测试验证
