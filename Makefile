.DEFAULT_GOAL: help

help:
	@echo "Available commands:"
	@echo
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build: ## Build docker image:
	docker compose build

dev: ## Start in development mode. Server port=13342. WebSockerServer port=13345
	docker compose up -d && docker compose logs -f

up: ## Start in production mode. Server port=13342. WebSockerServer port=13345
	docker compose -f docker-compose.prod.yml up -d

down: ## Remove all containers:
	docker compose down --remove-orphans

destroy: ## Remove all containers and images
	docker compose down --remove-orphans && docker image rm ew-seismicview

stop:  ## Stop all containers
	docker compose stop

logs: ## View the logs
	docker compose logs --tail=25 seismicview

server-tests: ## Test the server
	docker compose run --rm --no-deps --entrypoint=pytest ew-viewer-ws /tests/


client-tests: ## Test the client
	docker compose run --rm --no-deps --entrypoint="npm run test" ew-viewer-client