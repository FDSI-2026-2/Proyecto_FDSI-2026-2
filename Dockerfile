# Entorno reproducible del banco de pruebas TRUST-MAS.
#
#   docker build -t trust-mas .
#   docker run --rm trust-mas                                    # tests
#   docker run --rm -v "$PWD/results:/app/results" trust-mas python run_experiment.py --preset completo
#   docker run --rm -e GOOGLE_API_KEY trust-mas python demo_orchestrator.py
FROM python:3.11-slim@sha256:da047cb8f9d1d98e5c070f5300ba9f7274e33b8fc0e5be5ed88740aed1b95ba9

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

WORKDIR /app
COPY --chown=root:root requirements-test.lock ./
RUN python -m pip install --no-cache-dir --only-binary=:all -r requirements-test.lock

RUN groupadd --system trustmas && useradd --system --gid trustmas --create-home trustmas && \
    install --directory --owner=trustmas --group=trustmas /app/results
COPY --chown=root:root src/ src/
COPY --chown=root:root tests/ tests/
COPY --chown=root:root docs/ docs/
COPY --chown=root:root demo.py demo_escenas.py demo_orchestrator.py run_experiment.py README.md ./

USER trustmas
CMD ["python", "-m", "pytest", "tests", "-q", "-p", "no:cacheprovider"]
