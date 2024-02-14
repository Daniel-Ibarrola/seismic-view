.DEFAULT_GOAL: help

help:
	@echo "Available commands:"
	@echo
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'


dev: ## Start in development mode. Server port=13342. WebSockerServer port=13345
	docker compose up -d && docker compose logs -f

staging: ## Start in staging mode (http)
    docker compose up -f docker-compose.staging.yml up -d

prod: ## Start in production mode (https).
	docker compose -f docker-compose.prod.yml up -d

down: ## Remove all containers:
	docker compose down --remove-orphans

stop:  ## Stop all containers
	docker compose stop

logs: ## View the logs
	docker compose logs --tail=25 seismicview

server-tests: ## Test the server
	docker compose run --rm --no-deps --entrypoint=pytest ew-viewer-ws /tests/

client-tests: ## Test the client
	docker compose run --rm --no-deps --entrypoint="npm run test" ew-viewer-client

auth-tests: ## Test the auth server
	docker compose run --rm --no-deps --entrypoint=pytest ew-viewer-auth /tests/