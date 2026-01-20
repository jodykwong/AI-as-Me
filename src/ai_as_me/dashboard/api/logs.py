"""日志流 API (SSE)."""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse, Response
from pathlib import Path
from typing import Optional, List, Dict
from pydantic import BaseModel
from ai_as_me.log_system.query import LogQuery
import asyncio
import json

router = APIRouter()


class LogEntry(BaseModel):
    """日志条目模型."""

    timestamp: str
    level: str
    logger: str
    message: str


class LogQueryResponse(BaseModel):
    """日志查询响应."""

    logs: List[Dict]
    total: int


@router.get("/logs", response_model=LogQueryResponse)
async def query_logs(
    limit: int = Query(100, ge=1, le=1000),
    level: Optional[str] = None,
    logger: Optional[str] = None,
):
    """查询日志."""
    try:
        query = LogQuery()
        logs = query.query(level=level, logger=logger, limit=limit)

        return LogQueryResponse(logs=logs, total=len(logs))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Log file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Log query failed: {str(e)}")


@router.get("/logs/export")
async def export_logs(
    format: str = Query("json", pattern="^(json|csv)$"), level: Optional[str] = None
):
    """导出日志."""
    try:
        query = LogQuery()
        data = query.export(format=format, level=level)

        media_type = "application/json" if format == "json" else "text/csv"
        filename = f"logs.{format}"

        return Response(
            content=data,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Log file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Log export failed: {str(e)}")


async def log_stream_generator(log_file: Path, level: Optional[str] = None):
    """生成日志流."""
    # 读取现有日志
    if log_file.exists():
        with open(log_file, "r") as f:
            for line in f:
                try:
                    log = json.loads(line)
                    if level and log.get("level") != level:
                        continue
                    yield f"data: {line}\n\n"
                except json.JSONDecodeError:
                    continue

    # 监听新日志 (简化版 tail -f)
    last_size = log_file.stat().st_size if log_file.exists() else 0

    while True:
        await asyncio.sleep(1)

        if not log_file.exists():
            continue

        current_size = log_file.stat().st_size
        if current_size > last_size:
            with open(log_file, "r") as f:
                f.seek(last_size)
                for line in f:
                    try:
                        log = json.loads(line)
                        if level and log.get("level") != level:
                            continue
                        yield f"data: {line}\n\n"
                    except json.JSONDecodeError:
                        continue
            last_size = current_size


@router.get("/logs/stream")
async def stream_logs(level: Optional[str] = None):
    """实时日志流 (SSE)."""
    log_file = Path("logs/agent.log")
    return StreamingResponse(
        log_stream_generator(log_file, level), media_type="text/event-stream"
    )
