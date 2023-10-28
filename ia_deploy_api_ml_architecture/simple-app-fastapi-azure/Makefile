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

export TAG=test4

#VALUES
MAKEDESC = FastAPI API, docker deployment

targets: help

ok: ## See if you are in the right Makefile
	@echo "\n--- TAG :: $(TAG) -- Working with $(MAKEDESC) ---\n\n"

# START with increment the tags in TAG e.g test1, test2, test3... etc

up: ## Build the Docker image named "bf-fastapi-demo:[TAG]"
	docker build -t bf-fastapi-demo:$(TAG) .

run: ## Run a container named "[TAG]-bf-fastapi-container". It is an instance of an image named "bf-fastapi-demo:[TAG]"
	docker run -d --name $(TAG)-bf-fastapi-container -p 80:80 bf-fastapi-demo:$(TAG)


see: # The Dockerfile tells FastAPI to use a port of 80, so the run command publishes the container's port 80 as port 80 on the local computer. I visit localhost:80 to confirm that my API is up and running. 
	@echo "\n--- Check bf-fastapi-demo:$(TAG) the app bf-fastapi-demo:$(TAG) at http://localhost:80 ---\n\n"

ps: ## List the images
	docker ps

stop: ## Stop the container test2-bf-fastapi-container
	  docker stop $(TAG)-bf-fastapi-container

rm:  ## Remove the container test2-bf-fastapi-container
	 docker rm -f $(TAG)-bf-fastapi-container


rmi: ## Remove the image with bf-fastapi-demo:test2
	 docker rmi --force bf-fastapi-demo:$(TAG)

# END If you change the code, you can restart from START above and redo the commands.

nuke: ## Remove everything, NUKE DOCKER IMAGES AND CONTAINERS
	  docker system prune

help: ## Display this help message
	@awk -F '##' '/^[a-z_]+:[a-z ]+##/ { print "\033[34m"$$1"\033[0m" "\n" $$2 }' Makefile
