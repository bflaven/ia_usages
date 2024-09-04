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
python 011_using_mlflow.py

Check 17_custom_models.py


# source
https://github.com/manuelgilm/mlflow_for_ml_dev/tree/mlflow_for_ml_dev_legacy

# video
https://www.youtube.com/playlist?list=PLQqR_3C2fhUUkoXAcomOxcvfPwRn90U-g

# other
https://mlflow.org/docs/latest/getting-started/intro-quickstart/index.html



"""


# 17_custom_models.py
my_experiment_name = "bf_custom_models"


import mlflow 
from mlflow_utils import create_mlflow_experiment

class CustomModel(mlflow.pyfunc.PythonModel):

    def __init__(self):
        pass 

    def fit(self):
        print("Fitting model...")

    def predict(self, context, model_input:[str]):
        return self.get_prediction(model_input)
    
    def get_prediction(self, model_input:[str]):
        # do something with the model input
        return " ".join([w.upper() for w in model_input])
    

if __name__=="__main__":

    experiment_id = create_mlflow_experiment(
        experiment_name= my_experiment_name,
        artifact_location= "bf_custom_model_artifacts",
        tags={"purpose":"learning"}
    )

    with mlflow.start_run(run_name="custom_model_run") as run:
        custom_model = CustomModel()

        custom_model.fit()

        mlflow.pyfunc.log_model(
            artifact_path="custom_model",
            python_model=custom_model)
        
        mlflow.log_param("param1", "value1")

        # load model
        custom_model = mlflow.pyfunc.load_model(f"runs:/{run.info.run_id}/custom_model")

        prediction = custom_model.predict(["hello", "world"])
        print(prediction)


