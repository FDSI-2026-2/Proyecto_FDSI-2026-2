"""Puertos que el nucleo usa para comunicarse con infraestructura externa."""

from __future__ import annotations

from typing import Protocol


class TextGenerator(Protocol):
    """Genera texto a partir de un prompt sin exponer una API de proveedor."""

    def complete(self, prompt: str) -> str:  # pragma: no cover - protocolo
        ...
