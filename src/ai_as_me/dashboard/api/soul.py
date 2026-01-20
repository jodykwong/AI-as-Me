"""Soul API - Soul 状态查询."""

from fastapi import APIRouter
from pathlib import Path

router = APIRouter()


def _safe_read_file(file_path: Path, default: str = "未配置") -> str:
    """安全读取文件内容."""
    try:
        if file_path.exists():
            return file_path.read_text(encoding="utf-8")
        return default
    except Exception as e:
        return f"读取失败: {e}"


@router.get("/soul/status")
async def get_soul_status() -> dict:
    """获取 Soul 完整状态."""
    soul_dir = Path("soul")

    profile = _safe_read_file(soul_dir / "profile.md")
    mission = _safe_read_file(soul_dir / "mission.md")

    # 统计规则
    rules_dir = soul_dir / "rules"
    try:
        core_rules = (
            len(list((rules_dir / "core").glob("*.md")))
            if (rules_dir / "core").exists()
            else 0
        )
        learned_rules = (
            len(list((rules_dir / "learned").glob("*.md")))
            if (rules_dir / "learned").exists()
            else 0
        )
    except Exception:
        core_rules = 0
        learned_rules = 0

    return {
        "profile": profile,
        "mission": mission,
        "rules": {
            "core": core_rules,
            "learned": learned_rules,
            "total": core_rules + learned_rules,
        },
    }


@router.get("/soul/profile")
async def get_profile() -> dict:
    """获取 Profile."""
    return {"content": _safe_read_file(Path("soul/profile.md"))}


@router.get("/soul/mission")
async def get_mission() -> dict:
    """获取 Mission."""
    return {"content": _safe_read_file(Path("soul/mission.md"))}
