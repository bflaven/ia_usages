# 005_j0kim_fastapi_docker_virtualenv

The post is here to getting started with FastAPI and Docker.
It leverages on virtualenv and not on anaconda.

- See at [https://dev.to/j0kim/getting-started-with-fastapi-and-docker-204j](https://dev.to/j0kim/getting-started-with-fastapi-and-docker-204j)

```bash

# In a terminal, require to have docker install
# clone the dir
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture/advanced_docker_compose_fastapi/

mkdir 005_j0kim_fastapi_docker

# go to the dir
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture/advanced_docker_compose_fastapi/005_j0kim_fastapi_docker/

# if needed
rm -R 005_j0kim_fastapi_docker

# 1. Use virtualenv

# Install virtualenv
pip install virtualenv

# additionnal requirements
pip install pyqt5
pip install pyqtwebengine

# solution for pip
rm -r ~/Library/Caches/pip/selfcheck/
python -m pip install --upgrade pip

# Create the env with virtualenv
python -m virtualenv fastapi-simple-app-env

# Activate the env
source fastapi-simple-app-env/bin/activate

# if you need to get out from the env
deactivate 

# if you need to remove out from the env
rm -rf hello-app-env
rm -rf fastapi-simple-app-env


# Install the requirements
pip install fastapi uvicorn

# f needed to update pip
pip install --upgrade pip

# Freeze the requirements.txt
pip freeze > requirements.txt

# Create the app
mkdir src
touch src/main.py

# Add a Dockerfile
# be sure to be in the root directory
touch Dockerfile


# NUKE DOCKER IMAGES
docker ps
docker rm -f $(docker ps -aq)
docker system prune


# Build your Docker image
docker build -t fastapi-simple-app-env .

# Run the docker image
docker run -p 8000:8000 --name fastapi-simple-app-name fastapi-simple-app-env
```

