FROM python:3.11.2-bullseye AS builder

RUN apt-get update && apt-get install -y -qq python-dev cmake build-essential pkg-config libgoogle-perftools-dev \
 && apt-get clean

ENV POETRY_VERSION=1.3.2
RUN pip install --no-cache-dir poetry==$POETRY_VERSION

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root

COPY . .

ENTRYPOINT ["poetry", "run", "python", "main.py"]
