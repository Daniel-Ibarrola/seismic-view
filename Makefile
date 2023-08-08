.DEFAULT_GOAL: help

help:
	@echo "Available commands:"
	@echo
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build: ## Build docker image:
	docker compose build

dev: ## Start in development mode. Server port=13342. WebSockerServer port=13345
	docker compose up

up: ## Start in production mode. Server port=13342. WebSockerServer port=13345
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

down: ## Remove all containers:
	docker compose down --remove-orphans

logs: ## View the logs
	docker compose logs --tail=25 app
