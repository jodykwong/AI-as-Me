"""灵感池 API."""
from fastapi import APIRouter, HTTPException
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel
from ai_as_me.inspiration import InspirationPool, InspirationConverter

router = APIRouter()


class InspirationResponse(BaseModel):
    """灵感响应模型."""
    id: str
    content: str
    source: str
    priority: str
    status: str
    maturity: float
    mentions: int
    created_at: str


class InspirationCreate(BaseModel):
    """创建灵感请求模型."""
    content: str
    priority: str = "medium"
    tags: List[str] = []


@router.get("/inspirations", response_model=List[InspirationResponse])
async def list_inspirations(
    status: Optional[str] = None,
    min_maturity: Optional[float] = None
):
    """获取灵感列表."""
    pool = InspirationPool(Path("soul/inspiration"))
    inspirations = pool.list_inspirations(status=status, min_maturity=min_maturity)
    
    return [
        InspirationResponse(
            id=insp.id,
            content=insp.content,
            source=insp.source,
            priority=insp.priority,
            status=insp.status,
            maturity=insp.maturity,
            mentions=insp.mentions,
            created_at=insp.created_at.isoformat()
        )
        for insp in inspirations
    ]


@router.post("/inspirations")
async def create_inspiration(data: InspirationCreate):
    """创建新灵感."""
    from ai_as_me.inspiration.models import Inspiration
    pool = InspirationPool(Path("soul/inspiration"))
    
    insp = Inspiration(
        content=data.content,
        source="api",
        priority=data.priority,
        tags=data.tags
    )
    insp_id = pool.add(insp)
    
    return {"id": insp_id, "status": "created"}


@router.get("/{inspiration_id}", response_model=InspirationResponse)
async def get_inspiration(inspiration_id: str):
    """获取单个灵感."""
    pool = InspirationPool(Path("soul/inspiration"))
    insp = pool.get_inspiration(inspiration_id)
    
    if not insp:
        raise HTTPException(status_code=404, detail="Inspiration not found")
    
    return InspirationResponse(
        id=insp.id,
        content=insp.content,
        source=insp.source,
        priority=insp.priority,
        status=insp.status,
        maturity=insp.maturity,
        mentions=insp.mentions,
        created_at=insp.created_at.isoformat()
    )


@router.post("/{inspiration_id}/convert")
async def convert_inspiration(inspiration_id: str, target_type: str):
    """转换灵感为规则或任务."""
    pool = InspirationPool(Path("soul/inspiration"))
    insp = pool.get_inspiration(inspiration_id)
    
    if not insp:
        raise HTTPException(status_code=404, detail="Inspiration not found")
    
    converter = InspirationConverter()
    
    if target_type == "rule":
        result = converter.to_rule(insp)
    elif target_type == "task":
        result = converter.to_task(insp)
    else:
        raise HTTPException(status_code=400, detail="Invalid target type")
    
    return {"success": True, "result": result}
