#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name azure_fastapi python=3.9.13
conda info --envs
source activate azure_fastapi
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n azure_fastapi

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture/fastapi_tiangolo_advanced_settings/

# LAUNCH THE FILE
python main_1.py

export MY_NEW_NAME="Prisca Jore"
It will change...

- requirements
pip install pydantic-settings


+ FastAPI Settings and Environment Variables
--- Source: https://fastapi.tiangolo.com/advanced/settings/




"""
import os

name = os.getenv("MY_NEW_NAME", "Bruno Flaven...")
print(f"Hello {name} from Python")





