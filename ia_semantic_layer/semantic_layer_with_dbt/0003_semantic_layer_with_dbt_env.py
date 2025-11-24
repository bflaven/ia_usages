#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[check]
pip --version
python --version

[env]

env]
# Conda Environment
conda create --name semantic_layer_with_dbt python=3.9.13
conda create --name dbt_env python=3.12.3

conda info --envs
source activate semantic_layer_with_dbt
source activate dbt_env
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n semantic_layer_with_dbt
conda env remove -n dbt_env


# update conda 
conda update -n base -c defaults conda


# TODO
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_semantic_layer/semantic_layer_with_dbt/
conda create -n semantic_layer_with_dbt python=3.12
conda activate semantic_layer_with_dbt
pip install --upgrade pip
pip install "mashumaro[msgpack]>=3.9,<3.15"
# pip install dbt-duckdb duckdb pandas
dbt --version

pip install dbt-duckdb duckdb pandas
pip install "dbt-duckdb==1.10.0" "duckdb==0.10.0" "pandas==2.2.2"




conda activate semantic_layer_with_dbt
pip install --upgrade pip
pip install "mashumaro[msgpack]>=3.9,<3.15"

# pip install dbt-duckdb duckdb pandas

dbt --version




# To easily reproduce environments:
pip freeze > requirements.txt

#Install everything in a new environment:
pip install -r requirements.txt


# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_semantic_layer/semantic_layer_with_dbt


# LAUNCH the file
python 0003_semantic_layer_with_dbt_env.py

"""

import dbt.adapters.duckdb
import duckdb
import pandas as pd
print("All core packages loaded successfully!")







