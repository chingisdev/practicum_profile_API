#!make
include .ugc.env.development
export

test.services:
	docker compose --file docker-compose.tests.yml up -d

test.services.down:
	docker compose --file docker-compose.tests.yml down

test:
	python -m pytest -vvv

auth.logs:
	docker compose --file docker-compose.tests.yml logs auth_api