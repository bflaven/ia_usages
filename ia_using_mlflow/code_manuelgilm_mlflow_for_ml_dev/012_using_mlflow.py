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
python 012_using_mlflow.py

Check 18_model_schema.py


# source
https://github.com/manuelgilm/mlflow_for_ml_dev/tree/mlflow_for_ml_dev_legacy

# video
https://www.youtube.com/playlist?list=PLQqR_3C2fhUUkoXAcomOxcvfPwRn90U-g

# other
https://mlflow.org/docs/latest/getting-started/intro-quickstart/index.html



"""

import mlflow
from mlflow_utils import create_mlflow_experiment
from mlflow.models.signature import ModelSignature
from mlflow.models.signature import infer_signature
from mlflow.types.schema import Schema
from mlflow.types.schema import ParamSchema
from mlflow.types.schema import ParamSpec
from mlflow.types.schema import ColSpec
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import pandas as pd
from typing import Tuple


def get_train_data() -> Tuple[pd.DataFrame]:
    """
    Generate train and test data.

    :return: x_train,y_train
    """
    x, y = make_classification()
    features = [f"feature_{i+1}" for i in range(x.shape[1])]
    df = pd.DataFrame(x, columns=features)
    df["label"] = y

    return df[features], df["label"]


if __name__ == "__main__":
    x_train, y_train = get_train_data()
    cols_spec = []
    data_map = {
        'int64': 'integer',
        'float64': 'double',
        'bool': 'boolean',
        'str': 'string',
        "date": 'datetime'
    }

    for name, dtype in x_train.dtypes.to_dict().items():
        cols_spec.append(ColSpec(name=name, type=data_map[str(dtype)]))

    input_schema = Schema(inputs=cols_spec)
    output_schema = Schema([ColSpec(name="label", type="integer")])

    parameter = ParamSpec(name="model_name", dtype="string", default="model1")
    param_schema = ParamSchema(params=[parameter])

    model_signature = ModelSignature(inputs=input_schema, outputs=output_schema, params=param_schema)
    print("MODEL SIGNATURE")
    print(model_signature.to_dict())

    model_signature = infer_signature(x_train, y_train, params={"model_name": "model1"})
    print("MODEL SIGNATURE")
    print(model_signature.to_dict())

    experiment_id = create_mlflow_experiment(
        experiment_name="Model Signature",
        artifact_location="model_signature_artifacts",
        tags={"purpose": "learning"},
    )

    with mlflow.start_run(run_name="model_signature_run") as run:
        mlflow.sklearn.log_model(
            sk_model=RandomForestClassifier(),
            artifact_path="model_signature",
            signature=model_signature,
        )
