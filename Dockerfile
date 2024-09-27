FROM python:3.12-slim

WORKDIR /app

EXPOSE 8000
ENV PYTHONPATH=/app

COPY pyproject.toml /app
COPY poetry.lock* /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi

COPY documents /app/documents
COPY templates /app/templates
COPY src /app/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]