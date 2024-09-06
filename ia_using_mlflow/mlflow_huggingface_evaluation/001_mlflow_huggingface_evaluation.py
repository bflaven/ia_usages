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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_using_mlflow/mlflow_huggingface_evaluation/


# launch the file
python 001_mlflow_huggingface_evaluation.py


# source_1
huggingface-evaluation.ipynb


"""


### Install necessary dependencies

# Necessary imports
import warnings

import pandas as pd
from datasets import load_dataset
from transformers import pipeline

import mlflow
from mlflow.metrics.genai import EvaluationExample, answer_correctness, make_genai_metric

# Disable FutureWarnings
warnings.filterwarnings("ignore", category=FutureWarning)

### Load a pretrained Hugging Face pipeline

# mpt_pipeline = pipeline("text-generation", model="mosaicml/mpt-7b-chat")

mpt_pipeline = pipeline("text-generation", model="distilgpt2")
 
# samllest models
# distilgpt2_pipeline = pipeline("text-generation", model="distilgpt2")
# gpt2_pipeline = pipeline("text-generation", model="gpt2")
# bart_pipeline = pipeline("text-generation", model="facebook/bart-base")

# t5_pipeline = pipeline("text2text-generation", model="t5-small")
# opt_pipeline = pipeline("text-generation", model="facebook/opt-125m")



### Log the model using MLflow
mlflow.set_experiment("Evaluate Hugging Face Text Pipeline")

# Define the signature
signature = mlflow.models.infer_signature(
    model_input="What are the three primary colors?",
    model_output="The three primary colors are red, yellow, and blue.",
)

# Log the model using mlflow
with mlflow.start_run():
    model_info = mlflow.transformers.log_model(
        transformers_model=mpt_pipeline,
        artifact_path="mpt-7b",
        signature=signature,
        registered_model_name="mpt-7b-chat",
    )


print('OK')
### Load Evaluation Data

dataset = load_dataset("tatsu-lab/alpaca")
eval_df = pd.DataFrame(dataset["train"])
eval_df.head(10)