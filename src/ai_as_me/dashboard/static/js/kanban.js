function kanbanApp() {
    return {
        board: { inbox: [], todo: [], doing: [], done: [] },
        agentStatus: null,
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
            console.log('kanbanApp initialized');
            await this.loadBoard();
            await this.loadAgentStatus();
            // 定期刷新Agent状态
            setInterval(() => this.loadAgentStatus(), 5000);
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
            this.loading = true;
            this.error = '';
            try {
                const res = await fetch('/api/kanban/board');
                if (!res.ok) throw new Error('加载看板失败');
                const data = await res.json();
                // 确保所有状态都存在
                this.board = {
                    inbox: data.inbox || [],
                    todo: data.todo || [],
                    doing: data.doing || [],
                    done: data.done || []
                };
            } catch (e) {
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
        }
    };
}
