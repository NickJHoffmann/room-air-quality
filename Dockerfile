# syntax=docker/dockerfile:1
FROM python:3.11-alpine AS base
WORKDIR /workdir
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

FROM base AS build-base
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.6.1
RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml .

FROM build-base AS build-dev
COPY . .
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction 

FROM build-dev AS dev
CMD ["uvicorn", "src.room_air_quality.main:app", "--reload"]
