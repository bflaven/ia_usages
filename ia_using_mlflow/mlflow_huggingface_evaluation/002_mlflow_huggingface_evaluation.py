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
conda env remove -n locust_poc
conda env remove -n dam_step_process
conda env remove -n fmm_fastapi_poc

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
python -m pip install mlflow
python -m pip install transformers 
python -m pip install accelerate 
python -m pip install torch 
python -m pip install xformers 
  

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_using_mlflow/mlflow_huggingface_evaluation/

# launch the file
python 002_mlflow_huggingface_evaluation.py


# source_1
huggingface-evaluation.ipynb


"""


import mlflow
mlflow.set_tracking_uri(uri="http://<host>:<port>")

