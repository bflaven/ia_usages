# simple-app-fastapi-azure

**You need to have an app to deploy! Right? Here is a simple one below. You can find some more on my github account in `simple-app-fastapi-azure` and in `mamamia-fastapi-azure`**

**This how-to is also avaliable at https://flaven.fr/2023/10/step-by-step-introducing-to-azure-cloud-deployment-deploying-a-fastapi-ml-feature-api/**

**This POC has everything required to be deployed on Azure.**


- *The question is "How-to: Deploying a containerized FastAPI app to Azure Container Apps".*
- *This how-to has been inspired by [https://blog.pamelafox.org/2023/03/deploying-containerized-fastapi-app-to.html](https://blog.pamelafox.org/2023/03/deploying-containerized-fastapi-app-to.html)*


## 1. Create a simple FastAPI App named "simple-app-fastapi-azure" to deploy to Azure

```bash

# go to the dir
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture

# make a directory named "simple-app-fastapi-azure"
mkdir simple-app-fastapi-azure

# get into the directory named "simple-app-fastapi-azure"
cd simple-app-fastapi-azure

# command to delete the all directory
rm -R simple-app-fastapi-azure

# create the FastAPI files
# you can create all the files at once
touch main.py requirements.txt Dockerfile .dockerignore
# and the cut and paste the code for each file.
```


**For the code to put in each file. See below. The code is reduced to the minimum.**

- **1. main.py**
```bash
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from fastapi import FastAPI, File, status
from fastapi.responses import RedirectResponse
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
 
app = FastAPI()

# home
@app.get("/")
async def home():
    # return RedirectResponse("/docs")
    return {'Azure FastAPI test api': 'It is running'}

    
    
```

- **2. requirements.txt**
```bash
fastapi
uvicorn
```

- **3. Dockerfil**
```bash
# Choose our version of Python
FROM python:3.9

# Set up a working directory
WORKDIR /code

# Copy just the requirements into the working directory so it gets cached by itself
COPY requirements.txt .

# Install the dependencies from the requirements file
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the code
COPY . .

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
```

- **4. .dockerignore**

I have picked an extended model for .dockerignore on this site: <a href="https://shisho.dev/blog/posts/how-to-use-dockerignore/" target="_blank" rel="noopener">https://shisho.dev/blog/posts/how-to-use-dockerignore/</a>


```bash
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
Makefile
README.md
```



**If you have a development environment, you can test your API.  A development environment is made with tools like Anaconda, Poetry, Venv... etc. I am using Anaconda.**

```bash

# V1
# launch the app
uvicorn main:app --reload

# in a browser you can check type URL
http://127.0.0.1:8000
http://localhost:8000
# I have declared in my hosts file cypress.mydomain.priv pointed to 127.0.0.1
http://cypress.mydomain.priv:8000

# ctrl+c to stop the server

# V2
# launch the app
uvicorn main:app --host 0.0.0.0 --port 80 --reload

# in a browser you can check type URL
http://127.0.0.1
http://localhost
# I have declared in my hosts file cypress.mydomain.priv pointed to 127.0.0.1
http://cypress.mydomain.priv


# See more at https://fastapi.tiangolo.com/deployment/manually/
```


## 2. Using Docker to load locally this simple FastAPI App named "simple-app-fastapi-azure"


**You need to install Docker. Check https://www.docker.com/**



```bash
# get into the dir
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture/simple-app-fastapi-azure

# START with increment the tags e.g test1, test2, test3... etc

# build the Docker image named "bf-fastapi-demo:test2"
docker build --tag bf-fastapi-demo:test2 .
# The application Docker has to be up and running

# run a container named "test2-bf-fastapi-container". It is an instance of an image named "bf-fastapi-demo:test1"
docker run -d --name test2-bf-fastapi-container -p 80:80 bf-fastapi-demo:test2

# The Dockerfile tells FastAPI to use a port of 80, so the run command publishes the container's port 80 as port 80 on the local computer. I visit localhost:80 to confirm that my API is up and running. 🏃🏽‍♀️

# check the app locally
http://localhost:80

# list the images
docker ps

# stop the container test2-bf-fastapi-container
docker stop test2-bf-fastapi-container

# remove the container test2-bf-fastapi-container
docker rm -f test2-bf-fastapi-container

# remove the image with bf-fastapi-demo:test2
docker rmi --force bf-fastapi-demo:test2

# END If you change the code, you can restart from START above and redo the commands.

# NUKE DOCKER IMAGES AND CONTAINERS
# remove all containers
docker rm -f $(docker ps -aq)

# remove everything
docker system prune

```

## 3. install Azure CLI
**You need to install Azure CLI.**

Check https://learn.microsoft.com/en-us/cli/azure/install-azure-cli

```bash

# SOME COMMANDS FOR Azure CLI

# Install the azure-cli
brew update && brew install azure-cli

# Check the install
az --version


```


## 4. Deploy to Azure this simple FastAPI App named "simple-app-fastapi-azure"


- ### 4.1 Push image to registry


```bash
# Go to the dir
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_deploy_api_ml_architecture/simple-app-fastapi-azure/


# Deploying Option #2: Step-by-step az commands
# STEP_1. check the install
az --version

# STEP_2. Requirement, you must be logged
az login

# STEP_3. Create a resource group
# Careful you can reuse an existing one but in this example I created from scratch
# COMMAND MODEL :: az group create --location eastus --name fastapi-aca-rg

# COMMAND GOOD
az group create --location eastus --name fastapi-try-rg

# if you need to delete
az group delete --name fastapi-try-rg


# STEP_4. Create a container registry wannatrycontainerregistry for the resource group "fastapi-try-rg"

# COMMAND MODEL :: az acr create --resource-group fastapi-aca-rg \ --name pamelascontainerregistry --sku Basic

# COMMAND GOOD
az acr create --resource-group fastapi-try-rg --name wannatrycontainerregistry --sku Basic


# STEP_5. Log into the registry so that later commands can push images to it:
# COMMAND MODEL :: az acr login --name pamelascontainerregistry

# COMMAND GOOD
az acr login --name wannatrycontainerregistry



# STEP_6. uploads the code to cloud and builds it there:
# COMMAND MODEL :: az acr build --platform linux/amd64 -t pamelascontainerregistry.azurecr.io/fastapi-try:latest -r pamelascontainerregistry .

# must be in a directory with a Dockerfile
# cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture/simple-app-fastapi-azure

# COMMAND GOOD
az acr build --platform linux/amd64 -t wannatrycontainerregistry.azurecr.io/fastapi-try:latest -r wannatrycontainerregistry .

```

- **4.2 Deploy to Azure Container App**


```bash
# You must be in the directory of your app 
# cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture/simple-app-fastapi-azure


# STEP_1: (OPTIONNAL) Upgrade the extension and register the necessary providers:
az extension add --name containerapp --upgrade
az provider register --namespace Microsoft.App
az provider register -n Microsoft.OperationalInsights --wait

# STEP_2: Create an environment for the container app:
# COMMAND MODEL :: az containerapp env create --name fastapi-aca-env \
    --resource-group fastapi-aca-rg --location eastus

# COMMAND GOOD
az containerapp env create --name fastapi-try-env --resource-group fastapi-try-rg --location eastus



# This will output the URL aka defaultDomain e.g : 
# orangesmoke-cceb35b3.eastus.azurecontainerapps.io
# purpleground-2c63d040.eastus.azurecontainerapps.io


# STEP_3: You must enable the admin:
# Run 'az acr update -n pamelascontainerregistry --admin-enabled true' to enable admin first.

# COMMAND GOOD
az acr update -n wannatrycontainerregistry --admin-enabled true

# STEP_4: Generate credentials to use for the next step:
# COMMAND MODEL :: az acr credential show --name pamelascontainerregistry

# output where you get the password

# COMMAND GOOD
az acr credential show --name wannatrycontainerregistry

# OUPUT where you can find the password.
{
  "passwords": [
    {
      "name": "password",
      "value": "FAKE+Ubb8iqWTtnDVDZg1ylHcCtHTTogZDt6iULcbKC+XXXXXXXXX"
    },
    {
      "name": "password2",
      "value": "FAKE+lwCMl71GlToW8YyeAsGaskVE4X8oLE2S8HipB+XXXXXXXXX"
    }
  ],
  "username": "wannatrycontainerregistry"
}


# STEP_5: Create the container app, passing in the username and password from the credentials:

# COMMAND MODEL 
az containerapp create --name fmm-fastapi-app \
    --resource-group fmm-fastapi-rg \
    --image pamelascontainerregistry.azurecr.io/fastapi-aca:latest \
    --environment fastapi-aca-env \
    --registry-server pamelascontainerregistry.azurecr.io \
    --registry-username pamelascontainerregistry \
    --registry-password PASSWORD_HERE \
    --ingress external \
    --target-port 80

# COMMAND GOOD
# Do not forget to replace the password with one show earlier

az containerapp create --name try-fastapi-app \
    --resource-group try-fastapi-rg \
    --image wannatrycontainerregistry.azurecr.io/try-fastapi:latest \
    --environment try-fastapi-env \
    --registry-server wannatrycontainerregistry.azurecr.io \
    --registry-username wannatrycontainerregistry \
    --registry-password T/ PASSWORD_HERE \
    --ingress external \
    --target-port 80



# Output you have your f... latestRevisionFqdn where it is the url where the app live ! Bingo

```

**Normally you are good! You have your app deployed**

- **4.3 If you need to clean up everything on Azure**

CAUTION: I like to undo thing or I should even say nuke things. This command is the perfect one, you “kill” all your azure environment from group to app deployed. With great power comes great responsibility.

```bash
# CAUTION: with this command, you will remove and clean up everything
az group delete --name try-fastapi-rg
```

**4.4 If you need to update an existing application on Azure**

Here the most useful 2 commands as you may change some stuff in your application, every time you want to deploy just perform these 2 commands. You must be in the root application directory and ensure that the application is running locally with Docker.

```bash
# You must be in the directory of your app 
# cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture/simple-app-fastapi-azure/

# Do not forget to login if needed. Requirement, you must be logged
# az login


# Make any code updates just re-build the image (step_1) and tell the container app to update (step_2):
# COMMAND MODEL :: STEP_1 
az acr build --platform linux/amd64 \
    -t pamelascontainerregistry.azurecr.io/fastapi-aca:latest \
    -r pamelascontainerregistry .

# COMMAND MODEL :: STEP_2
az containerapp update --name fastapi-aca-app \
  --resource-group fastapi-aca-rg \
  --image pamelascontainerregistry.azurecr.io/fastapi-aca:latest


# COMMAND_GOOD_1
az acr build --platform linux/amd64 \
    -t wannatrycontainerregistry.azurecr.io/try-fastapi:latest \
    -r wannatrycontainerregistry .

# COMMAND_GOOD_2
az containerapp update --name try-fastapi-app \
  --resource-group try-fastapi-rg \
  --image wannatrycontainerregistry.azurecr.io/try-fastapi:latest 

# show the log
az webapp log tail --name wannatrycontainerregistry --resource-group try-fastapi-rg

# show the group
az group show --name try-fastapi-rg
```

- **4.5 The magic command “all-in-one”**


```bash
A unique command that “Create or update a container app as well as any associated resources (ACR, resource group, container apps environment, GitHub Actions, etc.).”
# COMMAND UNIQUE MODEL
az containerapp up \
  -g fastapi-aca-rg \
  -n fastapi-aca-app \
  --registry-server pamelascontainerregistry.azurecr.io \
  --ingress external \
  --target-port 80 \
  --source .

# CAUTION the registry-server must exist

# COMMAND_GOOD UNIQUE
az containerapp up \
  -g try-fastapi-rg \
  -n try-fastapi-app \
  --registry-server wannatrycontainerregistry.azurecr.io \
  --ingress external \
  --target-port 80 \
  --source .
```




