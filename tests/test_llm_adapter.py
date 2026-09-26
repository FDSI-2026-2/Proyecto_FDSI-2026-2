from types import SimpleNamespace

import pytest

from trust_mas.adapters.langchain import LangChainTextGenerator, TextGenerationError


class FakeLangChainClient:
    def __init__(self, response) -> None:
        self.response = response
        self.prompts: list[str] = []

    def invoke(self, prompt: str):
        self.prompts.append(prompt)
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


def test_adaptador_normaliza_el_contenido_de_langchain():
    client = FakeLangChainClient(SimpleNamespace(content="respuesta"))
    generator = LangChainTextGenerator(client)
    assert generator.complete("prompt") == "respuesta"
    assert client.prompts == ["prompt"]


def test_adaptador_normaliza_respuesta_sin_content():
    assert LangChainTextGenerator(FakeLangChainClient(42)).complete("prompt") == "42"


def test_adaptador_traduce_fallos_del_proveedor():
    generator = LangChainTextGenerator(FakeLangChainClient(ConnectionError("sin servicio")))
    with pytest.raises(TextGenerationError, match="proveedor LLM"):
        generator.complete("prompt")
