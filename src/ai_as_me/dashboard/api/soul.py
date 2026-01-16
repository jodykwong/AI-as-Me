"""Soul API - Soul 状态查询."""
from fastapi import APIRouter
from pathlib import Path

router = APIRouter()


@router.get("/soul/status")
async def get_soul_status():
    """获取 Soul 完整状态."""
    soul_dir = Path("soul")
    
    # 读取 profile
    profile_file = soul_dir / "profile.md"
    profile = profile_file.read_text(encoding='utf-8') if profile_file.exists() else "未配置"
    
    # 读取 mission
    mission_file = soul_dir / "mission.md"
    mission = mission_file.read_text(encoding='utf-8') if mission_file.exists() else "未配置"
    
    # 统计规则
    rules_dir = soul_dir / "rules"
    core_rules = len(list((rules_dir / "core").glob("*.md"))) if (rules_dir / "core").exists() else 0
    learned_rules = len(list((rules_dir / "learned").glob("*.md"))) if (rules_dir / "learned").exists() else 0
    
    return {
        "profile": profile,
        "mission": mission,
        "rules": {
            "core": core_rules,
            "learned": learned_rules,
            "total": core_rules + learned_rules
        }
    }


@router.get("/soul/profile")
async def get_profile():
    """获取 Profile."""
    profile_file = Path("soul/profile.md")
    if not profile_file.exists():
        return {"content": "未配置"}
    return {"content": profile_file.read_text(encoding='utf-8')}


@router.get("/soul/mission")
async def get_mission():
    """获取 Mission."""
    mission_file = Path("soul/mission.md")
    if not mission_file.exists():
        return {"content": "未配置"}
    return {"content": mission_file.read_text(encoding='utf-8')}
