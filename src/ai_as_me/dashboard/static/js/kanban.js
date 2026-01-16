function kanbanApp() {
    return {
        board: { inbox: [], todo: [], doing: [], done: [] },
        newTask: '',
        newPriority: 'P2',
        showClarifyModal: false,
        currentTask: null,
        clarifyForm: {
            goal: '',
            acceptance_criteria: [''],
            tool: '',
            time_estimate: ''
        },

        async init() {
            await this.loadBoard();
        },

        async loadBoard() {
            try {
                const res = await fetch('/api/kanban/board');
                this.board = await res.json();
            } catch (e) {
                console.error('Failed to load board:', e);
            }
        },

        async createTask() {
            if (!this.newTask.trim()) return;
            
            try {
                await fetch('/api/kanban/tasks', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        description: this.newTask,
                        priority: this.newPriority
                    })
                });
                
                this.newTask = '';
                await this.loadBoard();
            } catch (e) {
                alert('创建任务失败: ' + e.message);
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
                alert('请填写目标');
                return;
            }

            const criteria = this.clarifyForm.acceptance_criteria.filter(c => c.trim());
            if (criteria.length === 0) {
                alert('请至少添加一条验收标准');
                return;
            }

            try {
                await fetch(`/api/kanban/tasks/${this.currentTask.id}/clarify`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        goal: this.clarifyForm.goal,
                        acceptance_criteria: criteria,
                        tool: this.clarifyForm.tool || null,
                        time_estimate: this.clarifyForm.time_estimate || null
                    })
                });

                // 自动移动到 todo
                await this.moveTask(this.currentTask.id, 'todo');
                
                this.showClarifyModal = false;
                await this.loadBoard();
            } catch (e) {
                alert('澄清失败: ' + e.message);
            }
        },

        async moveTask(taskId, toStatus) {
            try {
                await fetch(`/api/kanban/tasks/${taskId}/move`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ to_status: toStatus })
                });
                
                await this.loadBoard();
            } catch (e) {
                alert('移动任务失败: ' + e.message);
            }
        },

        showTask(task) {
            // 显示任务详情（简化版）
            console.log('Task:', task);
        },

        getPriorityClass(priority) {
            const classes = {
                'P1': 'text-red-600 font-bold',
                'P2': 'text-orange-600',
                'P3': 'text-gray-600'
            };
            return classes[priority] || '';
        }
    };
}
