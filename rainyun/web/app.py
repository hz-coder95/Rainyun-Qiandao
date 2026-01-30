"""FastAPI 应用入口。"""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from rainyun.web.errors import ApiError
from rainyun.web.responses import error_response
from rainyun.web.routes import accounts_router, actions_router, servers_router, system_router

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(title="Rainyun Web API")

    @app.exception_handler(ApiError)
    async def api_error_handler(request: Request, exc: ApiError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content=error_response(exc.message, code=1)
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(status_code=500, content=error_response("系统异常", code=1))

    app.include_router(accounts_router)
    app.include_router(servers_router)
    app.include_router(system_router)
    app.include_router(actions_router)
    return app


app = create_app()
