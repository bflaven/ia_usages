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
python 002_using_mlflow.py


# source
https://github.com/manuelgilm/mlflow_for_ml_dev/tree/mlflow_for_ml_dev_legacy

"""

import mlflow 
from mlflow_utils import get_mlflow_experiment


# create a new mlflow experiment
"""
experiment_id = mlflow.create_experiment(
        name="bf_testing_mlflow6",
        artifact_location="bf_testing_mlflow6_artifacts",
        tags={"env": "dev", "version": "1.0.0"},
)
print('\n --- create a new mlflow experiment ')
print(experiment_id)
"""

# retrieve the mlflow experiment
# your_experiment_id = "535653524660435959"
# your_experiment_id = "709085486030106489" # bf_testing_mlflow4
# your_experiment_id = "959587270460853254" # bf_testing_mlflow5
# your_experiment_id = "533547054311470371" # bf_testing_mlflow6

"""
experiment = get_mlflow_experiment(experiment_id=your_experiment_id)

print("Name: {}".format(experiment.name))
print("Experiment_id: {}".format(experiment.experiment_id))
print("Artifact Location: {}".format(experiment.artifact_location))
print("Tags: {}".format(experiment.tags))
print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))
print("Creation timestamp: {}".format(experiment.creation_time))
"""

#delete the mlflow experiment
# your_experiment_id = "535653524660435959"
# your_experiment_id = "709085486030106489" # bf_testing_mlflow4
# your_experiment_id = "959587270460853254" # bf_testing_mlflow5
# your_experiment_id = "533547054311470371" # bf_testing_mlflow6

# mlflow.delete_experiment(experiment_id=your_experiment_id)


