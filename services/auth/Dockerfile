FROM python:3.11-alpine

COPY pyproject.toml /pyproject.toml
COPY requirements/ /requirements/
COPY src/ /src/
COPY tests/ /tests/

# Install curl to perform health checks
RUN apk add --no-cache curl

RUN mkdir -p /logs &&  \
    pip install -r /requirements/dev.txt &&  \
    pip install -e .

WORKDIR /src
