FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/* && \
    pip install poetry

COPY pyproject.toml poetry.lock ./
COPY src ./src
COPY migrations ./migrations
COPY settings ./settings

RUN poetry config installer.max-workers 10 && \
    poetry install --no-interaction --no-ansi

COPY --chown=app:app ./src /src
COPY gconf.py .

ENV GUNICORN_CMD_ARGS="-c gconf.py"

COPY entrypoint.sh .
COPY init_db.py .
COPY alembic.ini .
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]