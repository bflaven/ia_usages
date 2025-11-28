#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name dbt_env python=3.9.13
conda info --envs
source activate dbt_env
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n dbt_env


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

conda activate semantic_layer_with_dbt

# pip install --upgrade pip
# pip install "mashumaro[msgpack]>=3.9,<3.15"
# pip install dbt-duckdb duckdb pandas
# dbt --version


# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_semantic_layer/semantic_layer_with_dbt


# LAUNCH the file
python 0002_semantic_layer_with_dbt_env.py

"""
from importlib.metadata import version, PackageNotFoundError

for pkg in ['dbt-core', 'dbt-duckdb', 'mashumaro']:
    try:
        print(f"{pkg}: {version(pkg)}")
    except PackageNotFoundError:
        print(f"{pkg}: not installed")








