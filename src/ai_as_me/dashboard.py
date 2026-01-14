"""Minimal Web Dashboard for AI-as-Me."""
from pathlib import Path
import json
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
            "timestamp": datetime.now().isoformat()
        }
    
    return app


def run_dashboard(kanban_dir: Path, soul_dir: Path, logs_dir: Path, host: str = "0.0.0.0", port: int = 8000):
    """Run the dashboard server."""
    app = create_app(kanban_dir, soul_dir, logs_dir)
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    # Default paths
    base = Path.home() / "AI-as-Me"
    run_dashboard(base / "kanban", base / "soul", base / "logs")
