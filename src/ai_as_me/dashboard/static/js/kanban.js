function kanbanApp() {
    return {
        board: { inbox: [], todo: [], doing: [], done: [] },
        newTask: '',
        newPriority: 'P2',
        showClarifyModal: false,
        showCelebration: false,
        showExecutionModal: false,
        showTaskModal: false,
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

        async init() {
            await this.loadBoard();
            // 定期刷新执行状态
            setInterval(() => this.refreshExecutionStatus(), 3000);
        },

        async loadBoard() {
            this.loading = true;
            this.error = '';
            try {
                const res = await fetch('/api/kanban/board');
                if (!res.ok) throw new Error('加载看板失败');
                this.board = await res.json();
            } catch (e) {
                this.error = e.message;
            } finally {
                this.loading = false;
            }
        },

        async createTask() {
            if (!this.newTask.trim()) return;
            
            this.loading = true;
            this.error = '';
            try {
                const res = await fetch('/api/kanban/tasks', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        description: this.newTask,
                        priority: this.newPriority
                    })
                });
                
                if (!res.ok) {
                    const data = await res.json();
                    throw new Error(data.detail || '创建任务失败');
                }
                
                this.newTask = '';
                await this.loadBoard();
            } catch (e) {
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
            this.loading = true;
            this.error = '';
            try {
                const res = await fetch(`/api/kanban/tasks/${taskId}/move`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ to_status: toStatus })
                });
                
                if (!res.ok) {
                    const data = await res.json();
                    throw new Error(data.detail || '移动任务失败');
                }
                
                // 如果移动到done，显示庆祝动画
                if (toStatus === 'done') {
                    this.celebrate();
                }
                
                await this.loadBoard();
            } catch (e) {
                this.error = e.message;
            } finally {
                this.loading = false;
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
            this.showTaskModal = true;
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

        async executeTask(taskId) {
            this.loading = true;
            this.error = '';
            try {
                const res = await fetch(`/api/kanban/tasks/${taskId}/execute`, {
                    method: 'POST'
                });
                
                if (!res.ok) {
                    const data = await res.json();
                    throw new Error(data.detail || '执行失败');
                }
                
                const data = await res.json();
                this.error = '';
                // 显示成功提示
                alert('✅ 任务已开始执行');
            } catch (e) {
                this.error = e.message;
            } finally {
                this.loading = false;
            }
        },

        async checkExecution(taskId) {
            try {
                const res = await fetch(`/api/kanban/tasks/${taskId}/execution`);
                if (res.ok) {
                    return await res.json();
                }
            } catch (e) {
                console.error('Check execution failed:', e);
            }
            return null;
        },

        async showExecutionLog(taskId) {
            try {
                const res = await fetch(`/api/kanban/tasks/${taskId}/execution`);
                if (res.ok) {
                    this.executionLog = await res.json();
                    this.showExecutionModal = true;
                } else {
                    this.error = '获取执行日志失败';
                }
            } catch (e) {
                this.error = e.message;
            }
        },

        async refreshExecutionStatus() {
            // 刷新doing任务的执行状态
            for (const task of this.board.doing) {
                await this.checkExecution(task.id);
            }
        },

        getStatusText(status) {
            const texts = {
                'not_started': '⚪ 未开始',
                'running': '🔵 执行中...',
                'completed': '✅ 执行完成',
                'failed': '❌ 执行失败'
            };
            return texts[status] || status;
        },

        formatTime(isoString) {
            if (!isoString) return '';
            const date = new Date(isoString);
            return date.toLocaleString('zh-CN');
        }
    };
}
