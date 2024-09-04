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
cd /Users/brunoflaven/Documents/01_work/blog_articles/_using_mlflow/code_manuelgilm_mlflow_for_ml_dev/

# launch the file
python 015_using_mlflow.py

Check 19_serving_multiple_models.py


# source
https://github.com/manuelgilm/mlflow_for_ml_dev/tree/mlflow_for_ml_dev_legacy

# video
https://www.youtube.com/playlist?list=PLQqR_3C2fhUUkoXAcomOxcvfPwRn90U-g

# other
https://mlflow.org/docs/latest/getting-started/intro-quickstart/index.html



"""

import mlflow
from mlflow_utils import create_mlflow_experiment
from mlflow.models.signature import infer_signature
from mlflow.models.signature import ModelSignature
from mlflow.types import ColSpec
from mlflow.types import Schema
from mlflow.types import ParamSpec
from mlflow.types import ParamSchema

import numpy as np


class CustomModel(mlflow.pyfunc.PythonModel):
    def predict_model1(self, model_input):
        # do some processing for model 1
        return 3 * model_input

    def predict_model2(self, model_input):
        # do some processing for model 2
        return 4 * model_input

    def predict_model3(self, model_input):
        # do some processing for model 3
        return 5 * model_input

    def predict(self, context, model_input, params):
        if params["model_name"] == "model_1":
            return self.predict_model1(model_input=model_input)

        elif params["model_name"] == "model_2":
            return self.predict_model2(model_input=model_input)

        elif params["model_name"] == "model_3":
            return self.predict_model3(model_input=model_input)

        else:
            raise Exception("Model Not Found!")


if __name__ == "__main__":
    experiment_id = create_mlflow_experiment(
        experiment_name="Serving Multiple Models",
        artifact_location="serving_multiple_models",
        tags={"purpose": "learning"},
    )
    input_schema = Schema(inputs=[ColSpec(type="integer", name="input")])
    output_schema = Schema(inputs=[ColSpec(type="integer", name="output")])
    param_spec = ParamSpec(name="model_name", dtype="string", default=None)
    param_schema = ParamSchema(params=[param_spec])
    model_signature = ModelSignature(
        inputs=input_schema, outputs=output_schema, params=param_schema
    )


    with mlflow.start_run(run_name="3_multiple_models", experiment_id=experiment_id) as run:

        mlflow.pyfunc.log_model(artifact_path="model", python_model=CustomModel(), signature=model_signature)

        model_uri = f"runs:/{run.info.run_id}/model"
        loaded_model = mlflow.pyfunc.load_model(model_uri=model_uri)

        for n in range(3):
            print(f"PREDICTION FROM MODEL {n+1}")
            print(loaded_model.predict(data={"input":np.int32(10)}, params={"model_name":f"model_{n+1}"}))
            print("\n")

        print(f"RUN_ID: {run.info.run_id}")








