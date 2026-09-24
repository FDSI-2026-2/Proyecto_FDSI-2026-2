# Pruebas y Operación Local

Esta guía es independiente del sistema operativo. Solo requiere Python y usa
un entorno virtual local; Ollama y Docker son opcionales.

## Preparación

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

En PowerShell, activa el entorno con `.venv\Scripts\Activate.ps1` y usa el
mismo comando `python -m pip install -r requirements.txt`.

## Pruebas de código

Ejecuta la suite y genera cobertura:

```bash
python -m pytest tests -q --cov=src/trust_mas --cov-report=term-missing --cov-report=xml:coverage.xml
```

La prueba debe finalizar sin fallos. `coverage.xml` se usa después por
SonarQube Cloud; no contiene secretos.

Para revisar los controles de seguridad que protegen la comunicación:

```bash
python -m pytest tests/test_identity.py tests/test_provenance.py tests/test_bus_integration.py -q
```

Estas pruebas verifican firma, rol, replay, procedencia alterada, capacidades
manipuladas y delegación atenuada.

## Pruebas de uso

La demostración determinista no usa un LLM ni red:

```bash
python demo.py
```

Comprueba manualmente que el resultado incluya lo siguiente:

1. El tráfico normal termina en `ACCEPT`.
2. La suplantación de rol termina en `REJECT`.
3. El reenvío del mismo nonce termina en `REJECT`.
4. El contenido externo con una acción no autorizada termina en `REJECT` o
   `QUARANTINE`.
5. La auditoría final informa una cadena íntegra.

La demo es una prueba de comportamiento, no una medición experimental. Para
evaluar las hipótesis del proyecto aún faltan las topologías no lineales y el
banco factorial A1-A5.

## Modelo Local con Ollama

Instala Ollama desde su instalador oficial para tu sistema operativo. Usa tres
terminales distintas: una para el servicio, otra para descargar el modelo y
otra para ejecutar el proyecto.

Terminal 1:
```bash
ollama serve
```

Terminal 2:
```bash
ollama pull llama3.2:3b
```

Terminal 3, con el entorno virtual activo:

```bash
TRUSTMAS_LLM=ollama OLLAMA_MODEL=llama3.2:3b python demo_orchestrator.py
```

En PowerShell:

```powershell
$env:TRUSTMAS_LLM = "ollama"
$env:OLLAMA_MODEL = "llama3.2:3b"
python demo_orchestrator.py
```

Este flujo usa un LLM real alojado localmente y conserva las capas A, B y C en
cada arista de LangGraph. No ejecuta transferencias, correo ni otras
herramientas externas: `action` sigue siendo metadato validado por el bus.
No conectes herramientas con efectos reales hasta implementar un gateway de
herramientas que obligue a pasar por `MessageBus.route()`.

Si Ollama no está disponible, la suite y `demo.py` siguen siendo totalmente
locales y no requieren modelo alguno.

## SonarQube Local

La instancia local usa Docker. Verifica primero que el comando `docker ps`
funcione con tu usuario. La instalación y permisos de Docker dependen del
sistema operativo; sigue la documentación oficial de Docker para tu plataforma.

```bash
docker run -d --name trust-mas-sonarqube -p 9000:9000 sonarqube:community
```

Abre `http://localhost:9000`, cambia la contraseña inicial de `admin`, crea un
proyecto local y genera un token de análisis. Después de generar
`coverage.xml`, ejecuta el scanner en un contenedor, sin instalar
`sonar-scanner` en el sistema:

```bash
docker run --rm --network host \
  -e SONAR_HOST_URL=http://localhost:9000 \
  -e SONAR_TOKEN=tu_token \
  -v "$PWD:/usr/src" \
  sonarsource/sonar-scanner-cli \
  -Dsonar.projectKey=trust-mas-local
```

Detén y elimina la instancia cuando termines:

```bash
docker stop trust-mas-sonarqube
docker rm trust-mas-sonarqube
```

## SonarQube Cloud en GitHub

El workflow `.github/workflows/sonar.yml` ejecuta tests y crea `coverage.xml`
en cada push y pull request. El paso de SonarQube Cloud se omite hasta que
configures los tres valores siguientes; después se ejecuta automáticamente.
Antes del primer análisis:

1. Inicia sesión con GitHub en SonarQube Cloud e importa el repositorio.
2. En GitHub, abre `Settings > Secrets and variables > Actions`.
3. Crea el secreto `SONAR_TOKEN` con un token generado en SonarQube Cloud.
4. Crea las variables `SONAR_PROJECT_KEY` y `SONAR_ORGANIZATION` con los
   valores mostrados por SonarQube Cloud.
5. Haz push y revisa la anotación del workflow y el panel del proyecto.

El token solo vive en GitHub Secrets. No debe aparecer en `sonar-project.properties`,
en archivos `.env`, commits ni capturas de pantalla. Los repositorios privados
pueden requerir un plan de SonarQube Cloud compatible.

## Escáneres Complementarios

Ejecuta estos comandos en un entorno de desarrollo con las herramientas
instaladas:

```bash
bandit -r src demo.py demo_orchestrator.py
semgrep scan --config auto src demo.py demo_orchestrator.py
pip-audit -r requirements.txt
ruff check src tests demo.py demo_orchestrator.py
mypy src --ignore-missing-imports
```

Bandit, Semgrep y `pip-audit` complementan SonarQube: no sustituyen las
pruebas de protocolo ni las revisiones de diseño de seguridad.
