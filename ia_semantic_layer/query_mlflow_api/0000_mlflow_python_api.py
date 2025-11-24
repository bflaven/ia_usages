#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[check]
pip --version
python --version

[env]
Recommended: Use Built-in venv

Create a new environment:
python -m venv mlflow_python_api

Activate the environment:
source mlflow_python_api/bin/activate

Install packages inside the environment:
pip install package_name

pip install mlflow
pip install mlflow==3.3.1
python -m pip install mlflow==3.3.1

python -m pip install --upgrade pip setuptools wheel

brew install cmake
brew install apache-arrow
export CMAKE_PREFIX_PATH=$(brew --prefix apache-arrow)/lib/cmake


Deactivate:
deactivate

To easily reproduce environments:
pip freeze > requirements.txt

Install everything in a new environment:
pip install -r requirements.txt


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



