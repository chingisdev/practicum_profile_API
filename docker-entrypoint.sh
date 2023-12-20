#!/bin/bash

wait_for_service() {
  host="$1"
  port="$2"

  echo "Waiting for $host:$port..."

  while ! nc -z "$host" "$port"; do
    sleep 1
  done

  echo "$host:$port is available."
}

wait_for_service redis 6379
wait_for_service mongodb 27017
wait_for_service auth_api 8000
wait_for_service kafka 9092

gunicorn -k uvicorn.workers.UvicornWorker -w ${UVICORN_WORKERS_NUM} --timeout 120 src.main:app -b 0.0.0.0:8080 --preload