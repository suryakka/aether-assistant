from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from aether.config.settings import Settings
from aether.container import Container

router = APIRouter()


@router.get("/health")
@inject
async def health(settings: Settings = Depends(Provide[Container.config])) -> dict:
    return {
        "status": "ok",
        "service": "aether-backend",
        "version": settings.app_version,
    }


@router.get("/config")
@inject
async def get_config(settings: Settings = Depends(Provide[Container.config])) -> dict:
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "llm": {
            "provider": settings.llm_provider,
            "model": settings.llm_model,
            "base_url": settings.llm_base_url,
        },
    }
