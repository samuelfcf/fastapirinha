#!/bin/sh
echo "running migrations..."
poetry run alembic upgrade head

echo "Pupulating db..."
python init_db.py

poetry run uvicorn --host 0.0.0.0 --port 9999 src.app:app