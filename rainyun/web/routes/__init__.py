"""API 路由汇总。"""

from .accounts import router as accounts_router
from .actions import router as actions_router
from .servers import router as servers_router
from .system import router as system_router

__all__ = [
    "accounts_router",
    "actions_router",
    "servers_router",
    "system_router",
]
