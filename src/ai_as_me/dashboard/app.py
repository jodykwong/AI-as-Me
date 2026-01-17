"""FastAPI 应用主入口."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI(
    title="AI-as-Me Dashboard",
    version="3.4.2",
    description="AI-as-Me 灵感管理与规则配置 Dashboard API",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册 API 路由（顺序很重要！）
from .api import inspirations, rules, stats, logs, kanban, soul, agent_status

app.include_router(agent_status.router, prefix="/api", tags=["agent"])
app.include_router(kanban.router, prefix="/api", tags=["kanban"])
app.include_router(soul.router, prefix="/api", tags=["soul"])
app.include_router(rules.router, prefix="/api", tags=["rules"])
app.include_router(stats.router, prefix="/api", tags=["stats"])
app.include_router(logs.router, prefix="/api", tags=["logs"])
app.include_router(inspirations.router, prefix="/api", tags=["inspirations"])  # 最后注册，避免路径冲突

# 静态文件
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/health")
async def health_check():
    """健康检查."""
    return {"status": "ok", "version": "3.4.0"}


@app.get("/")
async def index():
    """首页."""
    return FileResponse(static_dir / "index.html")


@app.get("/inspirations.html")
async def inspirations_page():
    """灵感池页面."""
    return FileResponse(static_dir / "inspirations.html")


@app.get("/rules.html")
async def rules_page():
    """规则管理页面."""
    return FileResponse(static_dir / "rules.html")


@app.get("/stats.html")
async def stats_page():
    """统计图表页面."""
    return FileResponse(static_dir / "stats.html")


@app.get("/soul.html")
async def soul_page():
    """Soul 状态页面."""
    return FileResponse(static_dir / "soul.html")


@app.get("/kanban.html")
async def kanban_page():
    """Kanban 看板页面."""
    return FileResponse(static_dir / "kanban.html")


@app.get("/logs.html")
async def logs_page():
    """日志查看器页面."""
    return FileResponse(static_dir / "logs.html")
