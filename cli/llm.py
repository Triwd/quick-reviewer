from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from typing import Protocol

import httpx

from cli.config import Config


class LLMClient(Protocol):
    async def stream(
        self, system_prompt: str, user_prompt: str
    ) -> AsyncIterator[str]: ...


class AnthropicClient:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._base_url = config.resolve_base_url()
        self._model = config.resolve_model()

    async def stream(
        self, system_prompt: str, user_prompt: str
    ) -> AsyncIterator[str]:
        url = f"{self._base_url}/v1/messages"
        headers = {
            "x-api-key": self._config.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload = {
            "model": self._model,
            "max_tokens": self._config.max_tokens,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
            "stream": True,
        }

        async for chunk in self._stream_request(url, headers, payload, "anthropic"):
            yield chunk

    async def _stream_request(
        self,
        url: str,
        headers: dict,
        payload: dict,
        provider: str,
    ) -> AsyncIterator[str]:
        attempt = 0
        max_attempts = 3

        while True:
            attempt += 1
            try:
                async with httpx.AsyncClient(timeout=300.0) as client:
                    async with client.stream(
                        "POST", url, headers=headers, json=payload
                    ) as response:
                        if response.status_code == 429 and attempt < max_attempts:
                            wait = 2 ** attempt
                            await asyncio.sleep(wait)
                            continue
                        response.raise_for_status()

                        async for line in response.aiter_lines():
                            if not line.startswith("data: "):
                                continue
                            data = line[6:]
                            if data == "[DONE]":
                                return

                            event = json.loads(data)

                            if provider == "anthropic":
                                if event.get("type") == "content_block_delta":
                                    delta = event.get("delta", {})
                                    text = delta.get("text", "")
                                    if text:
                                        yield text
                            else:
                                choices = event.get("choices", [])
                                if choices:
                                    delta = choices[0].get("delta", {})
                                    text = delta.get("content", "")
                                    if text:
                                        yield text
                return
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429 and attempt < max_attempts:
                    wait = 2 ** attempt
                    await asyncio.sleep(wait)
                    continue
                raise


class OpenAIClient:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._base_url = config.resolve_base_url()
        self._model = config.resolve_model()

    async def stream(
        self, system_prompt: str, user_prompt: str
    ) -> AsyncIterator[str]:
        url = f"{self._base_url}/v1/chat/completions"
        headers = {
            "authorization": f"Bearer {self._config.api_key}",
            "content-type": "application/json",
        }
        payload = {
            "model": self._model,
            "max_tokens": self._config.max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": True,
        }

        attempt = 0
        max_attempts = 3

        while True:
            attempt += 1
            try:
                async with httpx.AsyncClient(timeout=300.0) as client:
                    async with client.stream(
                        "POST", url, headers=headers, json=payload
                    ) as response:
                        if response.status_code == 429 and attempt < max_attempts:
                            wait = 2 ** attempt
                            await asyncio.sleep(wait)
                            continue
                        response.raise_for_status()

                        async for line in response.aiter_lines():
                            if not line.startswith("data: "):
                                continue
                            data = line[6:]
                            if data == "[DONE]":
                                return

                            event = json.loads(data)
                            choices = event.get("choices", [])
                            if choices:
                                delta = choices[0].get("delta", {})
                                text = delta.get("content", "")
                                if text:
                                    yield text
                return
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429 and attempt < max_attempts:
                    wait = 2 ** attempt
                    await asyncio.sleep(wait)
                    continue
                raise


def create_client(config: Config) -> AnthropicClient | OpenAIClient:
    if config.provider == "anthropic":
        return AnthropicClient(config)
    return OpenAIClient(config)
