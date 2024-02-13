#!/bin/sh
echo "running migrations..."
poetry run alembic upgrade head

echo "Pupulating db..."
python init_db.py

poetry run gunicorn src.app:app