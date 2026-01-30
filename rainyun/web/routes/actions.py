"""操作类路由。"""

from fastapi import APIRouter, Depends

from rainyun.data.store import DataStore
from rainyun.scheduler import MultiAccountRunner
from rainyun.web.deps import get_store, require_auth
from rainyun.web.responses import success_response

router = APIRouter(prefix="/api/actions", tags=["actions"], dependencies=[Depends(require_auth)])


@router.post("/checkin")
def run_checkin(store: DataStore = Depends(get_store)) -> dict:
    runner = MultiAccountRunner(store)
    results = runner.run()
    payload = [
        {"account_id": item.account_id, "success": item.success, "message": item.message}
        for item in results
    ]
    return success_response(payload)
