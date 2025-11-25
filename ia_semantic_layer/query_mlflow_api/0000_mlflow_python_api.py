#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name mlflow_api_env python=3.9.13
conda info --envs
source activate mlflow_api_env
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n mlflow_api_env


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

conda install -c conda-forge mlflow

pip install beautifulsoup4
pip install requests

python -m pip install beautifulsoup4
python -m pip install requests

# [path]
cd /Users/brunoflaven/Documents/02_copy/_strategy_IA_fmm/mlflow_python_api/

# LAUNCH the file
python 0000_mlflow_python_api.py

MLflow Experiments Listing Script
Connects to a remote MLflow server with HTTP Basic Authentication
and retrieves all experiments.

MLflow Version: 3.3.1
Author: Generated for Bruno Flaven
Date: November 2025
"""

import os
import mlflow
from mlflow.tracking import MlflowClient

# Set authentication credentials as environment variables
os.environ['MLFLOW_TRACKING_USERNAME'] = "[username]"
os.environ['MLFLOW_TRACKING_PASSWORD'] = "[password]"

mlflow.set_tracking_uri("[site-mlflow]mlflow")
client = MlflowClient()

# Now you can use the client to list experiments, etc.
for exp in client.search_experiments():
    print(exp.name)



