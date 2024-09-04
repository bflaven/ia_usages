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
python 009_using_mlflow.py

Check 14_inference.py, 15_inference2.py


# source
https://github.com/manuelgilm/mlflow_for_ml_dev/tree/mlflow_for_ml_dev_legacy

# video
https://www.youtube.com/playlist?list=PLQqR_3C2fhUUkoXAcomOxcvfPwRn90U-g

# other
https://mlflow.org/docs/latest/getting-started/intro-quickstart/index.html



"""

import pandas as pd
from mlflow.models import infer_signature
import mlflow
from mlflow_utils import get_mlflow_experiment

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# 14_inference.py
my_experiment_name = "bf_testing_mlflow7"


if __name__ == "__main__":

    run_id = "91a43b3b9be54e7b9d364e4b3dcb3166"

    X, y = make_classification(
        n_samples=1000, n_features=10, n_informative=5, n_redundant=5, random_state=42)
    X = pd.DataFrame(X, columns=["feature_{}".format(i) for i in range(10)])
    y = pd.DataFrame(y, columns=["target"])

    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=43)

    # load model
    
    # INFO: you can find the model in tabs "Artifacts" 
    # model_uri = 'runs:/91a43b3b9be54e7b9d364e4b3dcb3166/random_forest_classifier'
    
    # model_uri = f'runs:/{run_id}/random_forest_classifier'
    
    # INFO: you can find the model in tabs "Artifacts" 
    # on a MAC for instance
    model_uri = f"/Users/brunoflaven/Documents/01_work/blog_articles/_using_mlflow/bf_testing_mlflow7_artifacts/{run_id}/artifacts/random_forest_classifier"
    

    # on a PC for instance
    # model_uri = f"file:///C:/Users/manue/Documents/projects/mlflow_for_ml_dev/bf_testing_mlflow7_artifacts/{run_id}/artifacts/random_forest_classifier"
    


    rfc = mlflow.sklearn.load_model(model_uri=model_uri)

    y_pred = rfc.predict(X_test)
    y_pred = pd.DataFrame(y_pred, columns=["prediction"])

    print(y_pred.head())



    
