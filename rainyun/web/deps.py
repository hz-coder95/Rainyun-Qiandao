"""FastAPI 依赖注入。"""

from rainyun.data.store import DataStore


_store = DataStore()


def get_store() -> DataStore:
    if _store.data is None:
        _store.load()
    return _store


def require_auth() -> None:
    """鉴权占位，待接入 Token 校验。"""

    return None
