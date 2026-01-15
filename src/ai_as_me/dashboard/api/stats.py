"""统计数据 API."""
from fastapi import APIRouter, Query
from pathlib import Path
from pydantic import BaseModel
from typing import Dict
from ai_as_me.stats.calculator import StatsCalculator

router = APIRouter()


class StatsResponse(BaseModel):
    """统计响应模型."""
    application_frequency: Dict[str, float]
    effectiveness_scores: Dict[str, float]
    pattern_accuracy: float
    time_range_days: int


@router.get("/stats", response_model=StatsResponse)
async def get_stats(days: int = Query(7, ge=1, le=365)):
    """获取系统统计数据."""
    try:
        calculator = StatsCalculator()
        stats = calculator.calculate_stats(days)
        
        return StatsResponse(
            application_frequency=stats.get("application_frequency", {}),
            effectiveness_scores=stats.get("effectiveness_scores", {}),
            pattern_accuracy=stats.get("pattern_accuracy", 0.0),
            time_range_days=days
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Evolution log not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats calculation failed: {str(e)}")
