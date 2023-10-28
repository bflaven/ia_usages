#!/usr/bin/python
# -*- coding: utf-8 -*-
#
"""

# Go to the dir
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_deploy_api_ml_architecture/deploy-on-azure-help/

python az_update_existing_application.py


"""
import subprocess
import time
import os


# Define the path
# path = "/Users/brunoflaven/Documents/01_work/blog_articles/ia_deploy_api_ml_architecture/simple-app-fastapi-azure"


path = "/Users/brunoflaven/Documents/01_work/blog_articles/ia_deploy_api_ml_architecture/mamamia-fastapi-azure"


# Define the variables
# container_registry_name = "wannatrycontainerregistry"
# app_service_name = "try-fastapi"


"""

# To delete
fastapi-poc-app
fastapi-poc-rg
pokatry1containerregistry

"""

container_registry_name = "pokatry1containerregistry"
app_generic_var = "fastapi-poc"

# Define the Azure CLI commands

# You will be ask to validate your login through a browser
command1 = f"az login"

command2 = f"az acr build --platform linux/amd64 -t {container_registry_name}.azurecr.io/{app_generic_var}:latest -r {container_registry_name} ."

command3 = f"az containerapp update --name {app_generic_var}-app --resource-group {app_generic_var}-rg --image {container_registry_name}.azurecr.io/{app_generic_var}:latest"


# Change directory to the specified path
try:
    os.chdir(path)
    print(f"OK you are in {path}")
    time.sleep(2)
except OSError:
    print(f"Could not change directory to {path}")
    exit(1)

# Execute the first command
print (command1)
subprocess.run(command1, shell=True)

# Wait for 10 seconds
time.sleep(10)

# Execute the second command
print (command2)
subprocess.run(command2, shell=True)

# Wait for 10 seconds
time.sleep(10)

# Execute the second command
print (command3)
subprocess.run(command3, shell=True)


print ('\n\n--- The existing app has been updated. Check on Azure ---\n\n')


"""

az config set core.allow_broker=true
az account clear
az login

"""
