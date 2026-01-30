"""系统设置路由。"""

from fastapi import APIRouter, Body, Depends

from rainyun.data.models import Settings
from rainyun.data.store import DataStore
from rainyun.web.deps import get_store, require_auth
from rainyun.web.responses import success_response

router = APIRouter(prefix="/api/system", tags=["system"], dependencies=[Depends(require_auth)])


@router.get("/settings")
def get_settings(store: DataStore = Depends(get_store)) -> dict:
    data = store.load() if store.data is None else store.data
    return success_response(data.settings.to_dict())


@router.put("/settings")
def update_settings(
    payload: dict = Body(default_factory=dict), store: DataStore = Depends(get_store)
) -> dict:
    data = store.load() if store.data is None else store.data
    settings = Settings.from_dict(payload)
    store.update_settings(settings)
    return success_response(settings.to_dict())
