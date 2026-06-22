from pathlib import Path

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _load_yaml_defaults() -> dict:
    config_path = Path(__file__).resolve().parents[2] / "config" / "default.yaml"
    if config_path.exists():
        with config_path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            return _flatten(data)
    return {}


def _flatten(data: dict, prefix: str = "") -> dict:
    result: dict = {}
    for key, value in data.items():
        full_key = f"{prefix}{key}" if not prefix else f"{prefix}_{key}"
        if isinstance(value, dict):
            result.update(_flatten(value, full_key))
        else:
            result[full_key] = value
    return result


_yaml_defaults = _load_yaml_defaults()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AETHER_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    app_name: str = Field(default=_yaml_defaults.get("app_name", "Aether Assistant"))
    app_version: str = Field(default=_yaml_defaults.get("app_version", "0.1.0"))
    app_host: str = Field(default=_yaml_defaults.get("app_host", "127.0.0.1"))
    app_port: int = Field(default=int(_yaml_defaults.get("app_port", 8787)))

    llm_provider: str = Field(default=_yaml_defaults.get("llm_provider", "ollama"))
    llm_base_url: str = Field(default=_yaml_defaults.get("llm_base_url", "http://127.0.0.1:11434"))
    llm_model: str = Field(default=_yaml_defaults.get("llm_model", "qwen3:8b"))
    llm_timeout_seconds: int = Field(default=int(_yaml_defaults.get("llm_timeout_seconds", 120)))


settings = Settings()
