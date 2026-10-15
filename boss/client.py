from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ChatResult:
    text: str
    usage: dict[str, Any]


class OpenAICompatibleClient:
    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
        timeout: int = 60,
        max_retries: int = 3,
    ):
        self.base_url = (base_url or os.getenv("THEBOSS_API_BASE", "")).rstrip("/")
        self.api_key = api_key if api_key is not None else os.getenv("THEBOSS_API_KEY", "")
        self.model = model or os.getenv("THEBOSS_MODEL", "")
        self.timeout = timeout
        self.max_retries = max_retries
        if not self.base_url:
            raise ValueError("THEBOSS_API_BASE is required")
        if not self.model:
            raise ValueError("THEBOSS_MODEL is required")
        if not (self.base_url.startswith("http://") or self.base_url.startswith("https://")):
            raise ValueError("THEBOSS_API_BASE must be an HTTP or HTTPS URL")

    def chat(
        self,
        messages: list[dict[str, Any]],
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> ChatResult:
        if not isinstance(messages, list) or not messages:
            raise ValueError("messages must be a non-empty list")
        if temperature < 0 or temperature > 2:
            raise ValueError("temperature must be between 0 and 2")
        if max_tokens <= 0:
            raise ValueError("max_tokens must be positive")

        body = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        payload = json.dumps(body).encode("utf-8")
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            request = urllib.request.Request(
                f"{self.base_url}/chat/completions",
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            if self.api_key:
                request.add_header("Authorization", f"Bearer {self.api_key}")
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    raw = response.read().decode("utf-8")
                parsed = json.loads(raw)
                choice = parsed["choices"][0]["message"]["content"]
                if choice is None:
                    choice = ""
                if isinstance(choice, list):
                    choice = " ".join(str(c) for c in choice)
                if not isinstance(choice, str):
                    raise RuntimeError("model returned non-text content")
                return ChatResult(text=choice, usage=parsed.get("usage", {}))
            except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError, json.JSONDecodeError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    delay = 2 ** attempt
                    if isinstance(exc, urllib.error.HTTPError) and getattr(exc, "code", None) == 429:
                        delay = 15 * (attempt + 1)
                    time.sleep(delay)
                    continue
                break
        raise RuntimeError(f"chat completion failed after {self.max_retries + 1} attempts: {last_error}") from last_error
