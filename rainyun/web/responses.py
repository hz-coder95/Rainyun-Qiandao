"""统一响应结构。"""

from typing import Any


def success_response(data: Any = None, message: str = "ok") -> dict[str, Any]:
    return {"code": 0, "message": message, "data": data}


def error_response(message: str, code: int = 1) -> dict[str, Any]:
    return {"code": code, "message": message, "data": None}
