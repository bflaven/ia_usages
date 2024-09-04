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
python -m pip uninstall mlflow


# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_using_mlflow

# launch the file
python 005_using_mlflow.py


# source
https://github.com/manuelgilm/mlflow_for_ml_dev/tree/mlflow_for_ml_dev_legacy

"""

import mlflow
from mlflow_utils import get_mlflow_experiment

# add your
my_experiment_name = "bf_testing_mlflow7"

experiment = get_mlflow_experiment(experiment_name=my_experiment_name)
print("Name: {}".format(experiment.name))

with mlflow.start_run(run_name="bf_logging_metrics", experiment_id = experiment.experiment_id) as run:
    # Your machine learning code goes here

    mlflow.log_metric("random_metric", 0.01)

    metrics = {
        "mse": 0.01,
        "mae": 0.01,
        "rmse": 0.01,
        "r2": 0.01
    }

    mlflow.log_metrics(metrics)

    # print run info
    print("run_id: {}".format(run.info.run_id))
    print("experiment_id: {}".format(run.info.experiment_id))
    print("status: {}".format(run.info.status))
    print("start_time: {}".format(run.info.start_time))
    print("end_time: {}".format(run.info.end_time))
    print("lifecycle_stage: {}".format(run.info.lifecycle_stage))

    
