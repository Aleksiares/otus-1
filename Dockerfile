FROM python:3.14-slim AS requirements-builder

RUN pip install --no-cache-dir uv

WORKDIR /build/

COPY pyproject.toml uv.lock /build/

# Экспортируем зависимости и устанавливаем в системный Python
RUN uv export --frozen --no-dev -o requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

FROM python:3.14-slim

ARG ENV_FILE=local.env
COPY ${ENV_FILE} .env

WORKDIR /app/

# Копируем установленные пакеты из builder stage
COPY --from=requirements-builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=requirements-builder /usr/local/bin /usr/local/bin

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY src /app/src
COPY alembic.ini /app/
COPY migrations /app/migrations

CMD ["python", "-m", "src.app.runner"]