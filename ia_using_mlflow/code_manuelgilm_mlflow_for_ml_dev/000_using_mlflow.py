#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name using_mlflow python=3.9.13
conda info --envs
source activate using_mlflow
conda deactivate

# BURN AFTER READING
source activate using_mlflow

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n using_mlflow
conda env remove -n locust_poc

# BURN AFTER READING
conda env remove -n using_mlflow

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
pip install mlflow
python -m pip install mlflow

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_using_mlflow/code_manuelgilm_mlflow_for_ml_dev/

# launch the file
python 000_using_mlflow.py
rye run python 000_using_mlflow.py

# source
https://github.com/djliden/llmops-examples/tree/main
https://medium.com/@dliden/comparing-llms-with-mlflow-1c69553718df
https://mlflow.org/docs/latest/llms/langchain/guide/index.html
https://mlflow.org/docs/latest/llms/llm-evaluate/notebooks/huggingface-evaluation.html

"""

import mlflow 
from mlflow_for_ml_dev.utils.utils import get_root_project


# Get the main directory
# print(get_root_project())

# Create location
# artifact_location = get_root_project() / "experiments" / "mlruns"
# mlflow.set_tracking_uri(artifact_location.as_uri())
# print(artifact_location)


# Create experiment
# experiment_name = "main-concepts-01"
# experiment_id = mlflow.create_experiment(name=experiment_name)
# print(experiment_id)




