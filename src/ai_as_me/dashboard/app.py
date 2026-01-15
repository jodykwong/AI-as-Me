"""FastAPI 应用主入口."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI(title="AI-as-Me Dashboard", version="3.4.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册 API 路由（顺序很重要！）
from .api import inspirations, rules, stats, logs

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
