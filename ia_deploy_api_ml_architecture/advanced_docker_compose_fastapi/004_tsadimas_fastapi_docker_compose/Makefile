# Makefile
# ::: DESCRIPTION :::
# FastAPI API, docker deployment
# Get a simple API made with FastAPI with Docker


#VALUES
MAKEDESC = FastAPI API, docker deployment

ci-docker-compose := docker-compose -f .ci/docker-compose.yml

targets: help

ok: ## See if you are in the right Makefile
	@echo "\n--- You are working in $(MAKEDESC) ---\n\n"

down: ## Down the image
	docker-compose down

up: ## Up the image
	docker-compose up --build

ps: ## Check if the container is running
	docker ps

ntw: ## Check existing networks
	docker network ls
	
kill: ## Remove the container
	docker rm -f $(docker ps -aq)

prune: ## Prune the system
	docker system prune

help: ## Display this help message
	@awk -F '##' '/^[a-z_]+:[a-z ]+##/ { print "\033[34m"$$1"\033[0m" "\n" $$2 }' Makefile
