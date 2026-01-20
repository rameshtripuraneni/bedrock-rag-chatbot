FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml /app/pyproject.toml
RUN pip install -U pip && pip install -e .

COPY src /app/src
COPY scripts /app/scripts
COPY data /app/data

EXPOSE 8000
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
