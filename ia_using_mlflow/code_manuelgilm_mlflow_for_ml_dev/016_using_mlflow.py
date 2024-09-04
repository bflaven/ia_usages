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
python 016_using_mlflow.py

Check 20_online_inference.py


# source
https://github.com/manuelgilm/mlflow_for_ml_dev/tree/mlflow_for_ml_dev_legacy

# video
https://www.youtube.com/playlist?list=PLQqR_3C2fhUUkoXAcomOxcvfPwRn90U-g

# other
https://mlflow.org/docs/latest/getting-started/intro-quickstart/index.html



"""

import json
import requests

# mlflow models serve -m runs:/<run_id>/model -p 5000
# mlflow models serve -m runs:/f970458fb6444fb496987d28f223941f/model -p 5000 --env-manager virtualenv
# model_uri = 'runs:/f970458fb6444fb496987d28f223941f/model'

data = {
    "dataframe_split": {"columns": ["input"], "data": [15]},
    "params": {"model_name": "model_1"},
}

headers = {"Content-Type": "application/json"}
endpoint = "http://127.0.0.1:5000/invocations"

r = requests.post(endpoint, data=json.dumps(data), headers=headers)
print(r.status_code)
print(r.text)







