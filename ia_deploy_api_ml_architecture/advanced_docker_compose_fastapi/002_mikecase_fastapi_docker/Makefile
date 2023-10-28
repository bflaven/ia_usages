# Makefile
# ::: DESCRIPTION :::
# FastAPI API, docker deployment
# Get a simple API made with FastAPI with Docker
#::: COMMANDS :::
# make ok
# make up
# make check
# make run
# make remove
# make rund
# make ccont
# make help
# make ccont


#VALUES
MAKEDESC = FastAPI API, docker deployment

targets: help

ok: ## See if you are in the right Makefile
	@echo "\n--- You are working in $(MAKEDESC) ---\n\n"

up: ## Build the docker image for the application
	docker build --pull --rm -f "Dockerfile" -t fastapi-app:latest "."

run: ## Run the docker container
	docker-compose -f "docker-compose.yml" up -d --build		
	@echo "\n--- Check http://127.0.0.1:8005/docs, http://0.0.0.0:8005/docs, http://localhost:8005/docs ---\n\n"


down: ## Down the image
	docker-compose down

ps: ## Check if the container is running
	docker ps

kill: ## Remove all containers
	docker rm -f $(docker ps -aq)

prune: ## Prune the system
	docker system prune

help: ## Display this help message
	@awk -F '##' '/^[a-z_]+:[a-z ]+##/ { print "\033[34m"$$1"\033[0m" "\n" $$2 }' Makefile
