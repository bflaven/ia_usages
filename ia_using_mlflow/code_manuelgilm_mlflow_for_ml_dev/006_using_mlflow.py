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
python 006_using_mlflow.py

Check 09_logging_artifacts.py, 10_logging_artifacts2.py

# source
https://github.com/manuelgilm/mlflow_for_ml_dev/tree/mlflow_for_ml_dev_legacy

# video
https://www.youtube.com/playlist?list=PLQqR_3C2fhUUkoXAcomOxcvfPwRn90U-g

"""

import mlflow
from mlflow_utils import get_mlflow_experiment


#. 09_logging_artifacts.py
# add your experiment
my_experiment_name = "bf_testing_mlflow7"

experiment = get_mlflow_experiment(experiment_name=my_experiment_name)
print("Name: {}".format(experiment.name))
with mlflow.start_run(run_name="logging_artifacts", experiment_id=experiment.experiment_id) as run:

        # your machine learning code goes here

        # create a text file that says hello world
        with open("hello_world.txt", "w") as f:
            f.write("Hello World!")

        # log the text file as an artifact
        mlflow.log_artifact(local_path="hello_world.txt", artifact_path="text_files")

        # print run info
        print("run_id: {}".format(run.info.run_id))
        print("experiment_id: {}".format(run.info.experiment_id))
        print("status: {}".format(run.info.status))
        print("start_time: {}".format(run.info.start_time))
        print("end_time: {}".format(run.info.end_time))
        print("lifecycle_stage: {}".format(run.info.lifecycle_stage))


"""
# 10_logging_artifacts2.py
# add your experiment
my_experiment_name = "bf_testing_mlflow7"

experiment = get_mlflow_experiment(experiment_name=my_experiment_name)
print("Name: {}".format(experiment.name))

with mlflow.start_run(run_name="bf_logging_artifacts", experiment_id=experiment.experiment_id) as run:

    # your machine learning code goes here
    mlflow.log_artifacts(local_dir="./run_artifacts",artifact_path="run_artifacts")

    # print run info
    print("run_id: {}".format(run.info.run_id))
    print("experiment_id: {}".format(run.info.experiment_id))
    print("status: {}".format(run.info.status))
    print("start_time: {}".format(run.info.start_time))
    print("end_time: {}".format(run.info.end_time))
    print("lifecycle_stage: {}".format(run.info.lifecycle_stage))    
"""