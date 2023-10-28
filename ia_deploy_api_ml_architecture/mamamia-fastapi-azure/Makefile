# Makefile
# ::: DESCRIPTION :::
# FastAPI API, docker deployment
# Get a simple API made with FastAPI with Docker
#::: COMMANDS :::
# cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture/advanced_docker_compose_fastapi/003_avanishcodes_docker_compose/
# make ok
# make up
# make check
# make run
# make remove
# make rund
# make ccont
# make help
# make ccont

export PROJECT=fastapi

#VALUES
MAKEDESC = FastAPI API, docker deployment

targets: help

ok: ## See if you are in the right Makefile
	@echo "\n--- You are working in $(MAKEDESC) ---\n\n"

# up: ## Build the docker image for the application
# 	docker build -t $(PROJECT)-image .

up: ## Up the image
	docker-compose up --build

down: ## Down the image
	docker-compose down

check: ## Check if the image is built
	docker images

ps: ## Check if the container is running
	docker ps

kill: ## Remove the container
	docker rm -f $(docker ps -aq)

prune: ## Prune the system
	docker system prune




help: ## Display this help message
	@awk -F '##' '/^[a-z_]+:[a-z ]+##/ { print "\033[34m"$$1"\033[0m" "\n" $$2 }' Makefile
