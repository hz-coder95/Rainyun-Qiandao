"""服务器管理路由。"""

from fastapi import APIRouter, Depends

from rainyun.config import Config
from rainyun.data.store import DataStore
from rainyun.web.deps import get_store, require_auth
from rainyun.web.errors import ApiError
from rainyun.web.responses import success_response

try:
    from rainyun.server.manager import ServerManager
except Exception as exc:  # pragma: no cover - 可选依赖
    ServerManager = None
    _server_manager_error = str(exc)

router = APIRouter(prefix="/api/servers", tags=["servers"], dependencies=[Depends(require_auth)])


@router.post("/check/{account_id}")
def check_servers(account_id: str, store: DataStore = Depends(get_store)) -> dict:
    data = store.load() if store.data is None else store.data
    account = next((item for item in data.accounts if item.id == account_id), None)
    if not account:
        raise ApiError("账户不存在", status_code=404)
    if not account.api_key:
        raise ApiError("未配置 API_KEY", status_code=400)
    if ServerManager is None:
        raise ApiError(f"服务器管理模块不可用: {_server_manager_error}", status_code=400)

    config = Config.from_account(account, data.settings)
    manager = ServerManager(account.api_key, config=config)
    result = manager.check_and_renew()
    return success_response(result)
