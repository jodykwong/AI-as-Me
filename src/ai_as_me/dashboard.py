"""Minimal Web Dashboard for AI-as-Me."""

from pathlib import Path
from datetime import datetime

try:
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    import uvicorn

    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False


def create_app(kanban_dir: Path, soul_dir: Path, logs_dir: Path):
    """Create FastAPI app."""
    if not HAS_FASTAPI:
        raise ImportError("FastAPI not installed. Run: pip install fastapi uvicorn")

    app = FastAPI(title="AI-as-Me Dashboard")

    @app.get("/", response_class=HTMLResponse)
    async def dashboard():
        # Count tasks
        inbox = len(list((kanban_dir / "inbox").glob("*.md")))
        todo = len(list((kanban_dir / "todo").glob("*.md")))
        doing = len(list((kanban_dir / "doing").glob("*.md")))
        done = len(list((kanban_dir / "done").glob("*.md")))

        # Load rules count
        rules_file = soul_dir / "rules.md"
        rules_count = 0
        if rules_file.exists():
            rules_count = rules_file.read_text().count("- ")

        # Get latest log
        latest_log = "No logs yet"
        log_files = sorted(logs_dir.glob("*.jsonl")) if logs_dir.exists() else []
        if log_files:
            with open(log_files[-1]) as f:
                lines = f.readlines()[-5:]
                latest_log = "<br>".join(lines)

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>AI-as-Me Dashboard</title>
    <meta http-equiv="refresh" content="30">
    <style>
        body {{ font-family: system-ui; max-width: 800px; margin: 40px auto; padding: 0 20px; background: #1a1a2e; color: #eee; }}
        h1 {{ color: #00d9ff; }}
        .board {{ display: flex; gap: 20px; margin: 20px 0; }}
        .col {{ flex: 1; background: #16213e; padding: 15px; border-radius: 8px; text-align: center; }}
        .col h3 {{ margin: 0 0 10px; color: #aaa; }}
        .col .num {{ font-size: 2em; font-weight: bold; }}
        .inbox .num {{ color: #ffd93d; }}
        .todo .num {{ color: #6bcb77; }}
        .doing .num {{ color: #4d96ff; }}
        .done .num {{ color: #ff6b6b; }}
        .stats {{ background: #16213e; padding: 15px; border-radius: 8px; margin: 20px 0; }}
        .log {{ background: #0f0f23; padding: 15px; border-radius: 8px; font-family: monospace; font-size: 12px; overflow-x: auto; }}
        footer {{ color: #666; margin-top: 40px; text-align: center; }}
    </style>
</head>
<body>
    <h1>🤖 AI-as-Me Dashboard</h1>
    
    <div class="board">
        <div class="col inbox"><h3>📥 Inbox</h3><div class="num">{inbox}</div></div>
        <div class="col todo"><h3>📋 Todo</h3><div class="num">{todo}</div></div>
        <div class="col doing"><h3>⚡ Doing</h3><div class="num">{doing}</div></div>
        <div class="col done"><h3>✅ Done</h3><div class="num">{done}</div></div>
    </div>
    
    <div class="stats">
        <strong>📚 Rules learned:</strong> {rules_count}
    </div>
    
    <h3>📜 Recent Logs</h3>
    <div class="log">{latest_log}</div>
    
    <footer>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</footer>
</body>
</html>
"""
        return html

    @app.get("/api/status")
    async def api_status():
        return {
            "inbox": len(list((kanban_dir / "inbox").glob("*.md"))),
            "todo": len(list((kanban_dir / "todo").glob("*.md"))),
            "doing": len(list((kanban_dir / "doing").glob("*.md"))),
            "done": len(list((kanban_dir / "done").glob("*.md"))),
            "timestamp": datetime.now().isoformat(),
        }

    @app.get("/api/tasks/{task_id}/execution-log")
    async def get_execution_log(
        task_id: str, since_timestamp: str = None, limit: int = 100
    ):
        """获取任务执行日志"""
        from .execution_logger import ExecutionLogger

        logger = ExecutionLogger(task_id)
        logs = logger.get_logs(since_timestamp, limit)
        return {"logs": logs}

    @app.get("/monitor", response_class=HTMLResponse)
    async def execution_monitor():
        """执行监控页面"""
        html = (
            """<!DOCTYPE html>
<html>
<head>
    <title>执行监控 - AI-as-Me</title>
    <style>
        body { font-family: system-ui; margin: 0; padding: 20px; background: #1a1a2e; color: #eee; }
        .monitor-panel { max-width: 1200px; margin: 0 auto; }
        .task-header { background: #16213e; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        .task-title { font-size: 1.5em; margin: 0; color: #00d9ff; }
        .task-meta { color: #aaa; margin-top: 5px; }
        .log-panel { background: #0f0f23; border-radius: 8px; height: 500px; display: flex; flex-direction: column; }
        .log-header { padding: 15px; border-bottom: 1px solid #333; display: flex; justify-content: space-between; align-items: center; }
        .log-controls { display: flex; gap: 10px; }
        .btn { padding: 5px 10px; background: #4d96ff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .btn:hover { background: #3d86ef; }
        .btn.active { background: #00d9ff; }
        .log-content { flex: 1; padding: 15px; overflow-y: auto; font-family: 'Courier New', monospace; font-size: 13px; line-height: 1.4; }
        .log-entry { margin-bottom: 8px; }
        .log-timestamp { color: #666; margin-right: 10px; }
        .log-step { color: #00d9ff; }
        .log-command { color: #ffd93d; }
        .log-output { color: #6bcb77; }
        .log-error { color: #ff6b6b; }
        .search-box { padding: 5px; background: #333; border: 1px solid #555; color: #eee; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="monitor-panel">
        <div class="task-header">
            <h1 class="task-title" id="taskTitle">任务执行监控</h1>
            <div class="task-meta" id="taskMeta">实时监控AI执行过程</div>
        </div>
        
        <div class="log-panel">
            <div class="log-header">
                <h3>实时执行日志</h3>
                <div class="log-controls">
                    <input type="text" class="search-box" placeholder="搜索日志..." id="searchBox">
                    <button class="btn active" id="autoScrollBtn">自动滚动</button>
                    <button class="btn" id="pauseBtn">暂停更新</button>
                    <button class="btn" id="clearBtn">清空</button>
                </div>
            </div>
            <div class="log-content" id="logContent">
                <div class="log-entry">
                    <span class="log-timestamp">["""
            + datetime.now().strftime("%H:%M:%S")
            + """]</span>
                    <span class="log-step">执行监控系统已启动，等待任务执行...</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        class ExecutionMonitor {
            constructor() {
                this.taskId = new URLSearchParams(window.location.search).get('task_id') || 'demo';
                this.autoScroll = true;
                this.paused = false;
                this.lastTimestamp = null;
                this.logs = [];
                
                this.initElements();
                this.bindEvents();
                this.startPolling();
            }
            
            initElements() {
                this.logContent = document.getElementById('logContent');
                this.autoScrollBtn = document.getElementById('autoScrollBtn');
                this.pauseBtn = document.getElementById('pauseBtn');
                this.clearBtn = document.getElementById('clearBtn');
                this.searchBox = document.getElementById('searchBox');
                this.taskTitle = document.getElementById('taskTitle');
                this.taskMeta = document.getElementById('taskMeta');
            }
            
            bindEvents() {
                this.autoScrollBtn.addEventListener('click', () => this.toggleAutoScroll());
                this.pauseBtn.addEventListener('click', () => this.togglePause());
                this.clearBtn.addEventListener('click', () => this.clearLogs());
                this.searchBox.addEventListener('input', () => this.filterLogs());
            }
            
            toggleAutoScroll() {
                this.autoScroll = !this.autoScroll;
                this.autoScrollBtn.textContent = this.autoScroll ? '自动滚动' : '手动滚动';
                this.autoScrollBtn.classList.toggle('active', this.autoScroll);
            }
            
            togglePause() {
                this.paused = !this.paused;
                this.pauseBtn.textContent = this.paused ? '恢复更新' : '暂停更新';
                this.pauseBtn.classList.toggle('active', this.paused);
            }
            
            clearLogs() {
                this.logs = [];
                this.logContent.innerHTML = '<div class="log-entry"><span class="log-timestamp">[' + new Date().toLocaleTimeString() + ']</span><span class="log-step">日志已清空</span></div>';
            }
            
            filterLogs() {
                const query = this.searchBox.value.toLowerCase();
                const entries = this.logContent.querySelectorAll('.log-entry');
                entries.forEach(entry => {
                    const visible = !query || entry.textContent.toLowerCase().includes(query);
                    entry.style.display = visible ? 'block' : 'none';
                });
            }
            
            async fetchLogs() {
                if (this.paused) return;
                
                try {
                    const url = `/api/tasks/${this.taskId}/execution-log` + 
                               (this.lastTimestamp ? `?since_timestamp=${this.lastTimestamp}` : '');
                    const response = await fetch(url);
                    const data = await response.json();
                    
                    if (data.logs && data.logs.length > 0) {
                        data.logs.forEach(log => this.addLogEntry(log));
                        this.lastTimestamp = data.logs[data.logs.length - 1].timestamp;
                    }
                } catch (error) {
                    console.error('获取日志失败:', error);
                }
            }
            
            addLogEntry(log) {
                this.logs.push(log);
                
                const entry = document.createElement('div');
                entry.className = 'log-entry';
                
                const timestamp = new Date(log.timestamp).toLocaleTimeString();
                const typeClass = `log-${log.type}`;
                
                entry.innerHTML = `
                    <span class="log-timestamp">[${timestamp}]</span>
                    <span class="${typeClass}">${this.escapeHtml(log.content)}</span>
                `;
                
                this.logContent.appendChild(entry);
                
                if (this.autoScroll) {
                    this.logContent.scrollTop = this.logContent.scrollHeight;
                }
                
                // 限制日志条数
                if (this.logs.length > 1000) {
                    this.logs.shift();
                    this.logContent.removeChild(this.logContent.firstChild);
                }
            }
            
            escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }
            
            startPolling() {
                this.fetchLogs();
                setInterval(() => this.fetchLogs(), 2000);
            }
        }
        
        new ExecutionMonitor();
    </script>
</body>
</html>"""
        )
        return html

    return app


def run_dashboard(
    kanban_dir: Path,
    soul_dir: Path,
    logs_dir: Path,
    host: str = "0.0.0.0",
    port: int = 8000,
):
    """Run the dashboard server."""
    app = create_app(kanban_dir, soul_dir, logs_dir)
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    # Default paths
    base = Path.home() / "AI-as-Me"
    run_dashboard(base / "kanban", base / "soul", base / "logs")
