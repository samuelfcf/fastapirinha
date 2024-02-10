FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/
COPY . .

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 9999
CMD [ "poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "9999", "src.app:app" ]