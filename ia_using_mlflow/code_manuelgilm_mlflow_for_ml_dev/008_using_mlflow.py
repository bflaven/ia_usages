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
python 008_using_mlflow.py

Check 12_logging_models.py


# source
https://github.com/manuelgilm/mlflow_for_ml_dev/tree/mlflow_for_ml_dev_legacy

# video
https://www.youtube.com/playlist?list=PLQqR_3C2fhUUkoXAcomOxcvfPwRn90U-g

# other
https://mlflow.org/docs/latest/getting-started/intro-quickstart/index.html



"""

import mlflow
from mlflow_utils import get_mlflow_experiment

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


#. 12_logging_models.py
# add your experiment
my_experiment_name = "bf_testing_mlflow7"

experiment = get_mlflow_experiment(experiment_name=my_experiment_name)
print("Name: {}".format(experiment.name))

with mlflow.start_run(run_name="bf_sklearn_logging_models", experiment_id=experiment.experiment_id) as run:

    
    X, y = make_classification(n_samples=1000, n_features=10, n_informative=5, n_redundant=5, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=43)

    # log model using autolog
    # mlflow.autolog()
    mlflow.sklearn.autolog()

    rfc = RandomForestClassifier(n_estimators=100, random_state=42)
    rfc.fit(X_train, y_train)
    y_pred = rfc.predict(X_test)

    
    # log model 
    mlflow.sklearn.log_model(sk_model=rfc, artifact_path="random_forest_classifier")
    

    # print info about the run
    print("run_id: {}".format(run.info.run_id))
    print("experiment_id: {}".format(run.info.experiment_id))
    print("status: {}".format(run.info.status))
    print("start_time: {}".format(run.info.start_time))
    print("end_time: {}".format(run.info.end_time))
    print("lifecycle_stage: {}".format(run.info.lifecycle_stage))

