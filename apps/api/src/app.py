from fastapi import FastAPI

from api.rest.chat_history import router as chat_history_router
from api.rest.chat_presence import router as chat_presence_router
from api.websocket.chat_socket import router as chat_socket_router
from settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.include_router(chat_history_router)
    app.include_router(chat_presence_router)
    app.include_router(chat_socket_router)

    @app.get("/healthz")
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
