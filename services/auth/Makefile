.DEFAULT_GOAL: help

help:
	@echo "Available commands:"
	@echo
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build:  ## Build docker image
	docker compose build

dev:  ## Start the development server on port 5000
	docker compose up -d && docker compose logs -f

up: ## Start the app in production mode
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

down: ## Remove all containers
	docker compose down --remove-orphans

destroy: ## Remove all containers and images
	docker compose down --remove-orphans && docker image rm ew-auth

stop: ## Stop the app
	docker compose stop

restart: ## Restart the app
	docker composer restart

test:  ## Run all tests
	docker compose run --rm --no-deps --entrypoint=pytest ew-auth /tests/

unit-tests: ## Run unit tests
	docker compose run --rm --no-deps --entrypoint=pytest ew-auth /tests/unit

e2e-tests:  ## Run end to end test
	docker compose run --rm --no-deps --entrypoint=pytest ew-auth /tests/e2e

logs:  ## View the logs
	docker compose logs --tail=25 ew-auth

add-user:  ## Add a new user to the database (requires email and password args).
	docker exec -it earthworm-auth flask add-user $(email) $(password)

add-email: ## Add a new email to the list of valid emails (requires email arg).
	docker exec -it earthworm-auth flask add-email $(email)

list-users: ## List the users in the database
	docker exec -it earthworm-auth flask list-users

remove-user: ## Remove a user from the database (requires email arg)
	docker exec -it earthworm-auth flask remove-user $(email)

update-password: ## Update the password of a user (requires email and password args).
	docker exec -it earthworm-auth flaks update-password $(email) $(password)
