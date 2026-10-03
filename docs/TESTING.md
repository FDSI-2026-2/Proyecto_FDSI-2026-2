# Pruebas y Operacion Local

La suite sin red funciona con Python 3.11 o 3.12. Docker y los proveedores LLM son opcionales.

## Preparacion

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --only-binary=:all --require-hashes -r requirements-test.lock
```

En PowerShell, activa el entorno con `.venv\Scripts\Activate.ps1`.

Instala las herramientas de calidad solo si las vas a ejecutar localmente:

```bash
python -m pip install --only-binary=:all --require-hashes -r requirements-dev.lock
```

Los proveedores son extras separados del nucleo:

```bash
python -m pip install --only-binary=:all --require-hashes -r requirements-gemini.lock
# o
python -m pip install --only-binary=:all --require-hashes -r requirements-ollama.lock
```

## Pruebas

```bash
python -m pytest tests -q --cov=src/trust_mas --cov-report=term-missing --cov-report=xml:coverage.xml --cov-fail-under=90
```

La suite no requiere una clave ni acceso a red. Cubre identidad, procedencia,
confianza, auditoria, protocolos, topologias, banco de pruebas y el adaptador
del puerto `TextGenerator`.

Para probar manualmente el recorrido determinista:

```bash
python demo.py
python demo_escenas.py
```

El trafico normal debe terminar en `ACCEPT`; una suplantacion o un replay debe
terminar en `REJECT`; y la auditoria final debe informar una cadena integra.

## Calidad y Seguridad

Con `requirements-dev.txt` instalado, la comprobacion equivalente a la CI es:

```bash
ruff format --check .
ruff check .
mypy src
bandit -q -r src
semgrep --config=p/security-audit --error src
pip-audit -r requirements.txt
pip-audit -r requirements-gemini.txt
pip-audit -r requirements-ollama.txt
pre-commit run --all-files
```

Instala los hooks una vez por clon con `pre-commit install`.

La CI ejecuta ademas Gitleaks, una matriz de pruebas para Python 3.11/3.12,
Docker, Trivy y genera un SBOM CycloneDX de las dependencias resueltas.

Los archivos `requirements-*.txt` declaran dependencias directas. Sus archivos
`.lock` contienen el grafo resuelto y sus hashes para instalaciones
automatizadas. Tras editar un manifiesto, regenera su lock con
`pip-compile --generate-hashes --strip-extras --output-file
requirements-NOMBRE.lock requirements-NOMBRE.txt` usando Python 3.11 y
verifica la suite antes de enviarlo.

## Docker

```bash
docker build --tag trust-mas:local .
docker run --rm trust-mas:local
```

La imagen usa Python 3.11 y un usuario sin privilegios; ejecuta la suite de
pruebas como comando por defecto.

## Modelo Local con Ollama

Instala y arranca Ollama conforme a su documentacion oficial. Luego descarga
un modelo y ejecuta el orquestador desde el entorno virtual:

```bash
ollama pull llama3.1
TRUSTMAS_LLM=ollama OLLAMA_MODEL=llama3.1 python demo_orchestrator.py
```

`OLLAMA_HOST` permite apuntar a un servidor remoto. El proveedor se adapta a
`TextGenerator`; el nucleo no depende de LangChain ni de la API de Ollama.

## Gemini

```bash
export GOOGLE_API_KEY=tu-clave
TRUSTMAS_LLM=gemini python demo_orchestrator.py
```

No guardes la clave en archivos versionados. Usa GitHub Secrets para los
workflows y revoca cualquier token publicado accidentalmente.

## SonarQube Cloud

`.github/workflows/sonar.yml` publica cobertura en cada push y pull request.
El analisis de SonarQube Cloud es condicional hasta configurar `SONAR_TOKEN`,
`SONAR_PROJECT_KEY` y `SONAR_ORGANIZATION` en GitHub Actions. El token debe
existir solo como secreto del repositorio.
