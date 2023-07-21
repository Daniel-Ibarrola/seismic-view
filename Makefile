
build:
	docker compose build

dev:
	docker compose up -d

up:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

down:
	docker compose down --remove-orphans


test: dev
	docker compose run --rm --no-deps --entrypoint=pytest app /tests/


logs:
	docker compose logs --tail=25 app

