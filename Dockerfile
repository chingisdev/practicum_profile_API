FROM python:3.10

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UVICORN_WORKERS_NUM 16

COPY pyproject.toml poetry.lock docker-entrypoint.sh /backend/

RUN apt update \
    && apt install -y gcc \
    && pip install --upgrade pip \
    && pip install "poetry==1.5.1" \
    && poetry config virtualenvs.create false \
    && poetry install --without dev

RUN apt-get update && apt-get install -y netcat-openbsd

COPY src /bachend/src

EXPOSE 8080
RUN sed -i 's/\r$//' /backend/docker-entrypoint.sh
RUN chmod +x /backend/docker-entrypoint.sh
CMD ["/backend/docker-entrypoint.sh"]