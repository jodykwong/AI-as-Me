"""API 路由."""
from .inspirations import router as inspirations_router
from .rules import router as rules_router
from .stats import router as stats_router
from .logs import router as logs_router

__all__ = ['inspirations_router', 'rules_router', 'stats_router', 'logs_router']
