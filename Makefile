test.services:
	docker compose --file docker-compose.tests.yml up

test.services.down:
	docker compose --file docker-compose.tests.yml down