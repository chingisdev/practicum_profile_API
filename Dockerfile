FROM python:3.10

WORKDIR /app

ENV UVICORN_WORKERS_NUM 16

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

RUN apt-get update && apt-get install -y netcat-openbsd

COPY src src
COPY docker-entrypoint.sh docker-entrypoint.sh

EXPOSE 8080
RUN sed -i 's/\r$//' /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh
CMD ["/app/docker-entrypoint.sh"]