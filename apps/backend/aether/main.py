from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from aether.config.settings import settings
from aether.container import Container, create_container
from aether.infrastructure.logging.setup import setup_logging
from aether.presentation.api import routes as api_routes
from aether.presentation.ws import session as ws_session
from aether.presentation.api.routes import router as api_router
from aether.presentation.ws.session import router as ws_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    container: Container = app.state.container
    llm = container.llm_adapter()
    yield
    await llm.close()


def create_app(container: Container | None = None) -> FastAPI:
    setup_logging()

    if container is None:
        container = create_container()

    container.wire(modules=[api_routes, ws_session])

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )
    app.state.container = container

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:1420",
            "http://127.0.0.1:1420",
            "tauri://localhost",
            "https://tauri.localhost",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)
    app.include_router(ws_router)

    return app


app = create_app()
