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
ccd /Users/brunoflaven/Documents/03_git/ia_usages/ia_using_mlflow/code_manuelgilm_mlflow_for_ml_dev/

# launch the file
python 003_using_mlflow.py


# source
https://github.com/manuelgilm/mlflow_for_ml_dev/tree/mlflow_for_ml_dev_legacy

"""

import mlflow 
from mlflow_utils import create_mlflow_experiment, get_mlflow_experiment



# start a run on default experiment

"""
#start a new mlflow run
mlflow.start_run()

# Your machine learning code goes here
mlflow.log_param("learning_rate",0.01)

#end the mlflow run
mlflow.end_run()
"""

# name a run on default experiment
"""
with mlflow.start_run(run_name="bf_mlflow_runs") as run:
        # Your machine learning code goes here
        mlflow.log_param("learning_rate",0.01)
        print("RUN ID")
        print(run.info.run_id)

        print(run.info)
"""

# create an experiment bf_testing_mlflow7 and add a run in it
experiment_id = create_mlflow_experiment(
    experiment_name="bf_testing_mlflow7",
    artifact_location="bf_testing_mlflow7_artifacts",
    tags={"env": "dev", "version": "1.0.0"},
)
experiment = get_mlflow_experiment(experiment_id=experiment_id)
print("Name: {}".format(experiment.name))
with mlflow.start_run(run_name="bf_testing_run", experiment_id = experiment.experiment_id) as run:

    # Your machine learning code goes here
    mlflow.log_param("learning_rate",0.01)
    # print run info    
    print("run_id: {}".format(run.info.run_id))
    print("experiment_id: {}".format(run.info.experiment_id))
    print("status: {}".format(run.info.status))
    print("start_time: {}".format(run.info.start_time))
    print("end_time: {}".format(run.info.end_time))
    print("lifecycle_stage: {}".format(run.info.lifecycle_stage))
