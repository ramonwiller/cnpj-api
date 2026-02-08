FROM python:3.13-slim-bookworm

# Evita .pyc e melhora logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# No container, poetry deve usar o mesmo Python onde as deps foram instaladas (evita venv vazio ao rodar como user app)
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Dependências do sistema (asyncpg, psycopg, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Dependências Python (cacheável)
# -------------------------------
COPY pyproject.toml poetry.lock* /app/

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# -------------------------------
# Código da aplicação
# -------------------------------
COPY app /app/app
COPY migrations /app/migrations
COPY alembic.ini /app/alembic.ini

# -------------------------------
# Usuário não-root (UID 1000). Padrão do projeto.
# -------------------------------
RUN groupadd --gid 1000 app \
    && useradd --uid 1000 --gid app --shell /bin/bash --create-home --home-dir /home/app app \
    && chown -R app:app /app

# -------------------------------
# Start script
# -------------------------------
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8000

USER app

CMD ["/start.sh"]