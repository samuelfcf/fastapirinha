#!/bin/sh

# DB migrations
poetry run alembic upgrade head

# app strat
poetry run uvicorn --host 0.0.0.0 --port 9999 src.app:app