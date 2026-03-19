from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml


_DEFAULT_MODELS = {
    "anthropic": "claude-sonnet-4-20250514",
    "openai": "gpt-4o",
}

_DEFAULT_BASE_URLS = {
    "anthropic": "https://api.anthropic.com",
    "openai": "https://api.openai.com",
}


@dataclass
class Config:
    provider: str = "anthropic"
    api_key: str = ""
    model: str = ""
    base_url: str | None = None
    max_tokens: int = 8192

    def resolve_model(self) -> str:
        return self.model or _DEFAULT_MODELS.get(self.provider, "")

    def resolve_base_url(self) -> str:
        url = self.base_url or _DEFAULT_BASE_URLS.get(self.provider, "")
        # Strip trailing /v1 or /v1/ to avoid double-prefixing in client code
        url = url.rstrip("/")
        if url.endswith("/v1"):
            url = url[:-3]
        return url


def _load_yaml_config(path: Path) -> dict:
    if path.is_file():
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, dict) else {}
    return {}


def load_config(
    *,
    provider: str | None = None,
    api_key: str | None = None,
    model: str | None = None,
    base_url: str | None = None,
) -> Config:
    """Load config with priority: CLI flags > env vars > project config > user config."""

    # Layer 1: user config (~/.quick-reviewer/config.yaml)
    user_cfg = _load_yaml_config(Path.home() / ".quick-reviewer" / "config.yaml")

    # Layer 2: project config (.quick-reviewer.yaml in cwd)
    project_cfg = _load_yaml_config(Path.cwd() / ".quick-reviewer.yaml")

    # Merge: project overrides user
    merged = {**user_cfg, **project_cfg}

    # Layer 3: env vars
    env_provider = os.environ.get("QR_PROVIDER")
    env_model = os.environ.get("QR_MODEL")
    env_base_url = os.environ.get("QR_BASE_URL")
    env_anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    env_openai_key = os.environ.get("OPENAI_API_KEY")

    if env_provider:
        merged["provider"] = env_provider
    if env_model:
        merged["model"] = env_model
    if env_base_url:
        merged["base_url"] = env_base_url

    # Resolve API key from env based on provider
    resolved_provider = provider or merged.get("provider", "anthropic")
    if resolved_provider == "anthropic" and env_anthropic_key:
        merged["api_key"] = env_anthropic_key
    elif resolved_provider == "openai" and env_openai_key:
        merged["api_key"] = env_openai_key

    # Layer 4: CLI flags (highest priority)
    if provider is not None:
        merged["provider"] = provider
    if api_key is not None:
        merged["api_key"] = api_key
    if model is not None:
        merged["model"] = model
    if base_url is not None:
        merged["base_url"] = base_url

    return Config(
        provider=merged.get("provider", "anthropic"),
        api_key=merged.get("api_key", ""),
        model=merged.get("model", ""),
        base_url=merged.get("base_url"),
        max_tokens=int(merged.get("max_tokens", 8192)),
    )
