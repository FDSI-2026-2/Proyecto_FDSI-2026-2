"""Composicion de proveedores LLM reales (Gemini u Ollama).

Se elige con variables de entorno, nunca con claves en el código:

    TRUSTMAS_LLM   gemini | ollama            (por defecto: gemini)
    GOOGLE_API_KEY clave de Gemini            (obligatoria con gemini)
    GEMINI_MODEL   p. ej. gemini-2.0-flash    (por defecto: gemini-2.0-flash)
    OLLAMA_MODEL   p. ej. llama3.1            (por defecto: llama3.1)
    OLLAMA_HOST    URL del servidor Ollama    (opcional)

Ambos se adaptan a `TextGenerator`, el puerto propio que usan el nucleo y el
banco de pruebas. LangChain queda limitado a esta capa de infraestructura.
"""

from __future__ import annotations

import os
from typing import Optional

from .adapters.langchain import LangChainTextGenerator
from .ports import TextGenerator

PROVIDERS = ("gemini", "ollama")
DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"
DEFAULT_OLLAMA_MODEL = "llama3.1"


class LLMConfigError(RuntimeError):
    pass


def build_text_generator(
    provider: Optional[str] = None, model: Optional[str] = None, temperature: float = 0.7
) -> TextGenerator:
    provider = (provider or os.environ.get("TRUSTMAS_LLM") or "gemini").lower()
    if provider == "gemini":
        if not os.environ.get("GOOGLE_API_KEY"):
            raise LLMConfigError(
                "Falta GOOGLE_API_KEY. Consigue una clave gratuita en https://aistudio.google.com/apikey "
                "y exportala como variable de entorno (nunca la pegues en el codigo)."
            )
        from langchain_google_genai import ChatGoogleGenerativeAI

        return LangChainTextGenerator(
            ChatGoogleGenerativeAI(
                model=model or os.environ.get("GEMINI_MODEL", DEFAULT_GEMINI_MODEL), temperature=temperature
            )
        )
    if provider == "ollama":
        try:
            from langchain_ollama import ChatOllama
        except ImportError as exc:
            raise LLMConfigError(
                "Para usar Ollama instala el paquete opcional: pip install langchain-ollama "
                "(y ten un servidor Ollama corriendo con el modelo descargado)."
            ) from exc
        model_name = model or os.environ.get("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
        host = os.environ.get("OLLAMA_HOST")
        if host:
            return LangChainTextGenerator(ChatOllama(model=model_name, temperature=temperature, base_url=host))
        return LangChainTextGenerator(ChatOllama(model=model_name, temperature=temperature))
    raise LLMConfigError(f"proveedor LLM desconocido: {provider!r} (opciones: {PROVIDERS})")
