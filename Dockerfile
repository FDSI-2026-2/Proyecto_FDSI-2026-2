# Entorno reproducible del banco de pruebas TRUST-MAS.
#
#   docker build -t trust-mas .
#   docker run --rm trust-mas                                    # tests
#   docker run --rm -v "$PWD/results:/app/results" trust-mas python run_experiment.py --preset completo
#   docker run --rm -e GOOGLE_API_KEY trust-mas python demo_orchestrator.py
FROM python:3.14-slim@sha256:a2b82f3c48559aa0a8446d9af49826b6e2b2016f4cd2afabfe6013ec53729170

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

WORKDIR /app
COPY --chown=root:root requirements-test.lock ./
RUN apt-get update && \
    apt-get install --no-install-recommends -y libpcre2-8-0=10.46-1~deb13u3 && \
    rm -rf /var/lib/apt/lists/* && \
    python -m pip install --no-cache-dir --only-binary=:all \
    pip==26.2 setuptools==84.0.0 wheel==0.48.0 && \
    python -m pip install --no-cache-dir --only-binary=:all --require-hashes -r requirements-test.lock

RUN groupadd --system trustmas && useradd --system --gid trustmas --create-home trustmas && \
    install --directory --owner=trustmas --group=trustmas /app/results
COPY --chown=root:root src/ src/
COPY --chown=root:root tests/ tests/
COPY --chown=root:root docs/ docs/
COPY --chown=root:root demo.py demo_escenas.py demo_orchestrator.py run_experiment.py README.md ./

USER trustmas
CMD ["python", "-m", "pytest", "tests", "-q", "-p", "no:cacheprovider"]
