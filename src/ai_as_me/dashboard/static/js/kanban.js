function kanbanApp() {
    console.log('kanbanApp called');
    
    // 配置常量
    const CONFIG = {
        AGENT_STATUS_REFRESH_INTERVAL: 5000,  // 5秒
        DOING_TASKS_REFRESH_INTERVAL: 10000,  // 10秒
        EXECUTION_PANEL_WIDTH: '396px',
        DRAG_ANIMATION_DURATION: 150
    };
    
    const app = {
        board: { inbox: [], todo: [], doing: [], done: [] },
        agentStatus: null,
        newTask: '',
        newPriority: 'P2',
        showClarifyModal: false,
        showCelebration: false,
        showExecutionModal: false,
        showExecutionStatus: false,
        showTaskModal: false,
        editMode: false,
        editTask: { description: '', priority: 'P2' },
        executionLog: null,
        currentTask: null,
        currentTaskDetail: null,
        loading: false,
        error: '',
        clarifyForm: {
            goal: '',
            acceptance_criteria: [''],
            tool: '',
            time_estimate: ''
        },
        
        // 执行监控相关
        selectedTaskId: '',
        executionLogs: [],
        autoScroll: true,
        lastLogTimestamp: null,

        async init() {
            console.log('kanbanApp initialized');
            // 先设置默认值，避免渲染错误
            this.board = { inbox: [], todo: [], doing: [], done: [] };
            this._optimisticUpdates = new Map(); // 🔧 FIX: 跟踪乐观更新
            await this.loadBoard();
            await this.loadAgentStatus();
            // 定期刷新Agent状态（不刷新看板，避免干扰用户操作）
            setInterval(() => this.loadAgentStatus(), CONFIG.AGENT_STATUS_REFRESH_INTERVAL);
            // 仅刷新doing任务状态（轻量级）
            setInterval(() => this.refreshDoingTasks(), CONFIG.DOING_TASKS_REFRESH_INTERVAL);
            // 执行日志监控
            setInterval(() => this.fetchExecutionLogs(), 2000);
            // 初始化拖拽功能
            this.$nextTick(() => this.initDragDrop());
        },
        
        /**
         * 初始化拖拽功能
         * 使用SortableJS为每个看板列启用拖拽
         * 拖拽完成后自动调用API更新任务状态
         */
        initDragDrop() {
            const statuses = ['inbox', 'todo', 'doing', 'done'];
            statuses.forEach(status => {
                const el = document.getElementById(`${status}-list`);
                if (el) {
                    new Sortable(el, {
                        group: 'kanban',  // 允许跨列拖拽
                        animation: CONFIG.DRAG_ANIMATION_DURATION,
                        ghostClass: 'sortable-ghost',  // 拖拽时的半透明样式
                        dragClass: 'sortable-drag',
                        onEnd: async (evt) => {
                            const taskId = evt.item.dataset.id;
                            const newStatus = evt.to.dataset.status;
                            const oldStatus = evt.from.dataset.status;
                            
                            console.log('🔥 [onEnd] Drag completed:', {
                                taskId,
                                from: oldStatus,
                                to: newStatus,
                                timestamp: new Date().toISOString()
                            });
                            
                            if (taskId && newStatus) {
                                try {
                                    await this.moveTask(taskId, newStatus);
                                } catch (error) {
                                    console.error('🔥 [onEnd] Move failed:', error);
                                    // 回滚: 移回原位置
                                    this.error = `移动失败: ${error.message}`;
                                    // 重新加载看板恢复状态
                                    await this.loadBoard();
                                }
                            }
                        }
                    });
                }
            });
        },
        
        /**
         * 删除任务
         * 显示确认对话框后调用API删除
         * @param {string} taskId - 任务ID
         */
        async deleteTask(taskId) {
            if (!confirm('确定要删除这个任务吗？')) return;
            
            try {
                const res = await fetch(`/api/kanban/tasks/${taskId}`, {
                    method: 'DELETE'
                });
                if (res.ok) {
                    await this.loadBoard();
                } else {
                    this.error = '删除失败';
                }
            } catch (e) {
                this.error = e.message;
            }
        },
        
        /**
         * 刷新doing任务状态
         * 仅在有doing任务时执行，避免不必要的API调用
         * 只更新doing列表，不影响其他列的用户操作
         */
        async refreshDoingTasks() {
            // 仅在有doing任务时刷新
            if ((this.board.doing || []).length > 0) {
                console.log('🔍 [refreshDoingTasks] START, current doing:', this.board.doing.length);
                try {
                    const res = await fetch('/api/kanban/board');
                    if (res.ok) {
                        const data = await res.json();
                        const newDoing = data.doing || [];
                        console.log('🔍 [refreshDoingTasks] API returned doing:', newDoing.length);
                        
                        // 🔧 FIX: 使用进入时间而非更新时间（方案A）
                        const now = Date.now();
                        const beforeFilter = this.board.doing.length;
                        this.board.doing = this.board.doing.filter(task => {
                            // 跳过乐观更新的任务
                            if (this._optimisticUpdates.has(task.id)) {
                                console.log('🔍 [refreshDoingTasks] Skipping optimistic:', task.id);
                                return true;
                            }
                            
                            // 使用进入时间而非更新时间
                            const enterTime = task._enterTime || new Date(task.updated_at).getTime();
                            const taskAge = now - enterTime;
                            const keep = taskAge < 3000 || newDoing.some(t => t.id === task.id);
                            
                            console.log('🔍 [refreshDoingTasks] Task', task.id, 
                                'enterTime:', new Date(enterTime).toISOString(),
                                'age:', taskAge, 'ms, keep:', keep);
                            return keep;
                        });
                        console.log('🔍 [refreshDoingTasks] After filter:', beforeFilter, '->', this.board.doing.length);
                        
                        // 合并新任务
                        newDoing.forEach(newTask => {
                            if (!this.board.doing.some(t => t.id === newTask.id)) {
                                console.log('🔍 [refreshDoingTasks] Adding new task:', newTask.id);
                                // 新任务也标记进入时间
                                newTask._enterTime = now;
                                this.board.doing.push(newTask);
                            }
                        });
                        console.log('🔍 [refreshDoingTasks] Final doing count:', this.board.doing.length);
                    }
                } catch (e) {
                    console.error('🔍 [refreshDoingTasks] ERROR:', e);
                }
            }
        },
        
        getPhaseInfo(task) {
            const phases = {
                'PREPARING': { label: '准备中', color: 'yellow', icon: '🟡', bgClass: 'bg-yellow-50 border-yellow-200', textClass: 'text-yellow-700', progress: 10 },
                'ANALYZING': { label: '分析中', color: 'blue', icon: '🔵', bgClass: 'bg-blue-50 border-blue-200', textClass: 'text-blue-700', progress: 30 },
                'EXECUTING': { label: '执行中', color: 'purple', icon: '🟣', bgClass: 'bg-purple-50 border-purple-200', textClass: 'text-purple-700', progress: 70 },
                'VALIDATING': { label: '验证中', color: 'indigo', icon: '🔷', bgClass: 'bg-indigo-50 border-indigo-200', textClass: 'text-indigo-700', progress: 90 },
                'COMPLETED': { label: '已完成', color: 'green', icon: '🟢', bgClass: 'bg-green-50 border-green-200', textClass: 'text-green-700', progress: 100 },
                'FAILED': { label: '失败', color: 'red', icon: '🔴', bgClass: 'bg-red-50 border-red-200', textClass: 'text-red-700', progress: 0 }
            };
            
            const phase = task.current_phase || (task.has_result ? 'COMPLETED' : 'EXECUTING');
            return phases[phase] || phases['EXECUTING'];
        },
        
        getExecutionDuration(task) {
            if (!task.updated_at) return '未知';
            const start = new Date(task.updated_at);
            const now = new Date();
            const diff = Math.floor((now - start) / 1000);
            // 处理负数情况（时间异常）
            if (diff < 0) return '刚刚';
            if (diff < 60) return `${diff}秒`;
            if (diff < 3600) return `${Math.floor(diff / 60)}分钟`;
            return `${Math.floor(diff / 3600)}小时`;
        },
        
        async refreshTaskStatus(taskId) {
            await this.loadBoard();
        },

        async loadAgentStatus() {
            try {
                const res = await fetch('/api/agent/status');
                if (res.ok) {
                    this.agentStatus = await res.json();
                }
            } catch (e) {
                console.error('Failed to load agent status:', e);
            }
        },

        async loadBoard() {
            console.log('loadBoard called');
            this.loading = true;
            this.error = '';
            try {
                console.log('Fetching board data...');
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 5000);
                
                const res = await fetch('/api/kanban/board', { signal: controller.signal });
                clearTimeout(timeoutId);
                
                console.log('Board response:', res.status);
                if (!res.ok) throw new Error('加载看板失败');
                const data = await res.json();
                console.log('Board data received:', Object.keys(data).map(k => `${k}:${data[k].length}`));
                // 确保所有状态都存在
                this.board = {
                    inbox: data.inbox || [],
                    todo: data.todo || [],
                    doing: data.doing || [],
                    done: data.done || []
                };
                console.log('Board updated');
            } catch (e) {
                console.error('loadBoard error:', e);
                this.error = e.message;
                // 出错时也保持board结构完整
                this.board = { inbox: [], todo: [], doing: [], done: [] };
            } finally {
                this.loading = false;
            }
        },

        async createTask() {
            console.log('createTask called', this.newTask, this.newPriority);
            if (!this.newTask.trim()) {
                console.log('Empty task, returning');
                return;
            }
            
            this.loading = true;
            this.error = '';
            try {
                console.log('Sending POST request...');
                const res = await fetch('/api/kanban/tasks', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        description: this.newTask,
                        priority: this.newPriority
                    })
                });
                
                console.log('Response status:', res.status);
                if (!res.ok) {
                    const data = await res.json();
                    throw new Error(data.detail || '创建任务失败');
                }
                
                this.newTask = '';
                await this.loadBoard();
                console.log('Task created successfully');
            } catch (e) {
                console.error('Create task error:', e);
                this.error = e.message;
            } finally {
                this.loading = false;
            }
        },

        clarifyTask(task) {
            this.currentTask = task;
            this.clarifyForm = {
                goal: task.clarification?.goal || '',
                acceptance_criteria: task.clarification?.acceptance_criteria?.length > 0 
                    ? [...task.clarification.acceptance_criteria] 
                    : [''],
                tool: task.clarification?.tool || '',
                time_estimate: task.clarification?.time_estimate || ''
            };
            this.showClarifyModal = true;
        },

        async submitClarify() {
            if (!this.clarifyForm.goal.trim()) {
                this.error = '请填写目标';
                return;
            }

            const criteria = this.clarifyForm.acceptance_criteria.filter(c => c.trim());
            if (criteria.length === 0) {
                this.error = '请至少添加一条验收标准';
                return;
            }

            this.loading = true;
            this.error = '';
            try {
                const res = await fetch(`/api/kanban/tasks/${this.currentTask.id}/clarify`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        goal: this.clarifyForm.goal,
                        acceptance_criteria: criteria,
                        tool: this.clarifyForm.tool || null,
                        time_estimate: this.clarifyForm.time_estimate || null
                    })
                });

                if (!res.ok) throw new Error('澄清失败');
                
                this.showClarifyModal = false;
                await this.loadBoard();
            } catch (e) {
                this.error = e.message;
            } finally {
                this.loading = false;
            }
        },

        async moveTask(taskId, toStatus) {
            console.log('🔍 [moveTask] START:', taskId, toStatus, new Date().toISOString());
            this.loading = true;
            this.error = '';
            
            // 🔧 FIX: 记录进入时间（方案A）
            const enterTime = Date.now();
            this._optimisticUpdates.set(taskId, { 
                status: toStatus, 
                enterTime: enterTime
            });
            console.log('🔍 [moveTask] Optimistic update set:', this._optimisticUpdates.size, 'enterTime:', enterTime);
            
            try {
                const res = await fetch(`/api/kanban/tasks/${taskId}/move`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ to_status: toStatus })
                });
                
                console.log('🔍 [moveTask] API response:', res.status);
                
                if (!res.ok) {
                    const data = await res.json();
                    throw new Error(data.detail || '移动任务失败');
                }
                
                const responseData = await res.json();
                console.log('🔍 [moveTask] Response data:', responseData);
                
                // 如果移动到done，显示庆祝动画
                if (toStatus === 'done') {
                    this.celebrate();
                }
                
                // 立即更新本地状态，避免重新加载整个看板
                this.updateLocalTaskStatus(taskId, toStatus);
                
                // 🔧 FIX: 标记任务进入时间
                const task = this.board[toStatus]?.find(t => t.id === taskId);
                if (task) {
                    task._enterTime = enterTime;
                    console.log('🔍 [moveTask] Task enter time marked:', taskId, enterTime);
                }
                
                console.log('🔍 [moveTask] Local status updated, doing count:', this.board.doing.length);
                
                // 🔧 FIX: 3秒后移除乐观更新标记
                setTimeout(() => {
                    console.log('🔍 [moveTask] Removing optimistic update for:', taskId);
                    this._optimisticUpdates.delete(taskId);
                }, 3000);
            } catch (e) {
                console.error('🔍 [moveTask] ERROR:', e);
                this.error = e.message;
                // 失败时立即移除标记并重新加载
                this._optimisticUpdates.delete(taskId);
                await this.loadBoard();
            } finally {
                this.loading = false;
                console.log('🔍 [moveTask] END');
            }
        },

        updateLocalTaskStatus(taskId, newStatus) {
            // 从所有列表中找到并移动任务
            let task = null;
            const statuses = ['inbox', 'todo', 'doing', 'done'];
            
            // 找到任务并从原列表移除
            for (const status of statuses) {
                const index = this.board[status].findIndex(t => t.id === taskId);
                if (index !== -1) {
                    task = this.board[status].splice(index, 1)[0];
                    break;
                }
            }
            
            // 添加到新列表
            if (task) {
                task.status = newStatus.toUpperCase();
                this.board[newStatus].push(task);
            }
        },

        celebrate() {
            this.showCelebration = true;
            setTimeout(() => {
                this.showCelebration = false;
            }, 2000);
        },

        showTask(task) {
            // 显示任务详情
            this.currentTaskDetail = task;
            this.editMode = false;
            this.editTask = null;
            this.showTaskModal = true;
        },

        editTaskMode(task) {
            this.editMode = true;
            this.editTask = {
                id: task.id,
                description: task.description,
                priority: task.priority
            };
        },

        async saveTask() {
            if (!this.editTask.description.trim()) {
                this.error = '任务描述不能为空';
                return;
            }

            this.loading = true;
            this.error = '';
            try {
                const res = await fetch(`/api/kanban/tasks/${this.editTask.id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        description: this.editTask.description,
                        priority: this.editTask.priority
                    })
                });

                if (!res.ok) throw new Error('更新任务失败');
                
                this.editMode = false;
                this.editTask = null;
                await this.loadBoard();
            } catch (e) {
                this.error = e.message;
            } finally {
                this.loading = false;
            }
        },

        cancelEdit() {
            this.editMode = false;
            this.editTask = null;
        },

        getPriorityClass(priority) {
            const classes = {
                'P1': 'text-red-600 font-bold',
                'P2': 'text-orange-600',
                'P3': 'text-gray-600'
            };
            return classes[priority] || '';
        },

        getPriorityBadge(priority) {
            const badges = {
                'P1': 'bg-red-100 text-red-800 border border-red-300',
                'P2': 'bg-orange-100 text-orange-800 border border-orange-300',
                'P3': 'bg-gray-100 text-gray-800 border border-gray-300'
            };
            return badges[priority] || '';
        },

        formatTime(isoString) {
            if (!isoString) return '';
            const date = new Date(isoString);
            return date.toLocaleString('zh-CN');
        },

        formatMarkdown(text) {
            if (!text) return '';
            
            // 简单的Markdown渲染
            let html = text;
            
            // 代码块
            html = html.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, lang, code) => {
                return `<div class="my-3 bg-gray-900 text-gray-100 p-3 rounded"><pre class="text-xs overflow-x-auto"><code>${this.escapeHtml(code.trim())}</code></pre></div>`;
            });
            
            // 行内代码
            html = html.replace(/`([^`]+)`/g, '<code class="bg-gray-100 px-1 py-0.5 rounded text-sm">$1</code>');
            
            // 标题
            html = html.replace(/^### (.+)$/gm, '<h3 class="text-lg font-bold mt-4 mb-2">$1</h3>');
            html = html.replace(/^## (.+)$/gm, '<h2 class="text-xl font-bold mt-4 mb-2">$1</h2>');
            html = html.replace(/^# (.+)$/gm, '<h1 class="text-2xl font-bold mt-4 mb-2">$1</h1>');
            
            // 列表
            html = html.replace(/^- (.+)$/gm, '<li class="ml-4">• $1</li>');
            html = html.replace(/^\d+\. (.+)$/gm, '<li class="ml-4 list-decimal">$1</li>');
            
            // 粗体
            html = html.replace(/\*\*(.+?)\*\*/g, '<strong class="font-bold">$1</strong>');
            
            // 段落
            html = html.split('\n\n').map(p => {
                if (p.trim() && !p.startsWith('<')) {
                    return `<p class="mb-2">${p}</p>`;
                }
                return p;
            }).join('\n');
            
            return html;
        },

        escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        },
        
        // 执行监控相关函数
        getCurrentTask() {
            return (this.board.doing || [])[0] || null;
        },
        
        async fetchExecutionLogs() {
            const currentTask = this.getCurrentTask();
            if (!currentTask) {
                // 🔧 FIX: 延迟5秒清空日志，避免任务完成时日志闪现消失
                if (!this._logClearTimer) {
                    this._logClearTimer = setTimeout(() => {
                        this.executionLogs = [];
                        this.selectedTaskId = '';
                        this._logClearTimer = null;
                    }, 5000);
                }
                return;
            }
            
            // 有任务时取消清空定时器
            if (this._logClearTimer) {
                clearTimeout(this._logClearTimer);
                this._logClearTimer = null;
            }
            
            // 如果切换了任务，清空日志
            if (this.selectedTaskId !== currentTask.id) {
                this.selectedTaskId = currentTask.id;
                this.executionLogs = [];
                this.lastLogTimestamp = null;
            }
            
            try {
                const url = `/api/tasks/${currentTask.id}/execution-log` + 
                           (this.lastLogTimestamp ? `?since_timestamp=${this.lastLogTimestamp}` : '');
                const res = await fetch(url);
                const data = await res.json();
                
                if (data.logs && data.logs.length > 0) {
                    this.executionLogs.push(...data.logs);
                    this.lastLogTimestamp = data.logs[data.logs.length - 1].timestamp;
                    
                    // 限制日志条数
                    if (this.executionLogs.length > 100) {
                        this.executionLogs = this.executionLogs.slice(-100);
                    }
                    
                    // 自动滚动
                    if (this.autoScroll) {
                        this.$nextTick(() => {
                            const container = document.getElementById('logContainer');
                            if (container) {
                                container.scrollTop = container.scrollHeight;
                            }
                        });
                    }
                }
            } catch (error) {
                console.error('获取执行日志失败:', error);
            }
        },
        
        toggleAutoScroll() {
            this.autoScroll = !this.autoScroll;
        },
        
        clearLogs() {
            this.executionLogs = [];
            this.lastLogTimestamp = null;
        },
        
        formatLogTime(timestamp) {
            return new Date(timestamp).toLocaleTimeString();
        },
        
        getLogTypeClass(type) {
            const classes = {
                'step': 'text-cyan-400',
                'command': 'text-yellow-400', 
                'output': 'text-green-400',
                'error': 'text-red-400'
            };
            return classes[type] || 'text-gray-400';
        }
    };
    console.log('kanbanApp returning object');
    return app;
}
