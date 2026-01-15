"""规则管理 API."""
from fastapi import APIRouter, HTTPException
from pathlib import Path
from typing import List, Dict
from pydantic import BaseModel
from ai_as_me.soul.versioning import RuleVersionManager
from ai_as_me.soul.loader import SoulLoader

router = APIRouter()


class RuleVersion(BaseModel):
    """规则版本模型."""
    version: str
    timestamp: str
    checksum: str
    message: str


class RuleInfo(BaseModel):
    """规则信息模型."""
    name: str
    current_version: str
    version_count: int


@router.get("/rules")
async def list_rules() -> Dict:
    """获取规则列表."""
    loader = SoulLoader(Path("soul"))
    return loader.list_rules()


@router.get("/rules/{rule_name}/history", response_model=List[RuleVersion])
async def get_rule_history(rule_name: str):
    """获取规则版本历史."""
    manager = RuleVersionManager(Path("soul/rules"))
    history = manager.get_history(rule_name)
    
    return [
        RuleVersion(
            version=v.version,
            timestamp=v.timestamp.isoformat(),
            checksum=v.checksum,
            message=v.message
        )
        for v in history
    ]


@router.post("/rules/{rule_name}/rollback")
async def rollback_rule(rule_name: str, version: str):
    """回滚规则到指定版本."""
    manager = RuleVersionManager(Path("soul/rules"))
    
    try:
        manager.rollback(rule_name, version)
        return {"success": True, "message": f"Rolled back to {version}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
