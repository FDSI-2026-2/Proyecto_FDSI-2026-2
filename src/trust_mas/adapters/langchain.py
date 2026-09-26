"""Adaptador de LangChain para el puerto de generacion de texto."""

from __future__ import annotations

from typing import Protocol


class InvokableChatModel(Protocol):
    """Minimo contrato de los clientes de chat de LangChain."""

    def invoke(self, prompt: str):  # pragma: no cover - protocolo de tercero
        ...


class TextGenerationError(RuntimeError):
    """Fallo normalizado de un proveedor de generacion de texto."""


class LangChainTextGenerator:
    """Oculta ``invoke`` y ``content`` de LangChain tras ``TextGenerator``."""

    def __init__(self, client: InvokableChatModel) -> None:
        self._client = client

    def complete(self, prompt: str) -> str:
        try:
            response = self._client.invoke(prompt)
        except Exception as exc:
            raise TextGenerationError("el proveedor LLM no pudo generar una respuesta") from exc
        content = getattr(response, "content", response)
        return content if isinstance(content, str) else str(content)
