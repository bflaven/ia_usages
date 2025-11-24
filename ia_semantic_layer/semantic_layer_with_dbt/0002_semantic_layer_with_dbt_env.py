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
conda create --name semantic_layer_with_dbt python=3.12.3

conda info --envs
source activate semantic_layer_with_dbt
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n semantic_layer_with_dbt


# update conda 
conda update -n base -c defaults conda


# Install packages inside the environment:
pip install package_name

pip install package_name
pip install package_name==3.3.1
python -m pip install package_name==3.3.1
python -m pip install --upgrade pip setuptools wheel


# To easily reproduce environments:
pip freeze > requirements.txt

#Install everything in a new environment:
pip install -r requirements.txt


# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_semantic_layer/semantic_layer_with_dbt


# LAUNCH the file
python 0002_semantic_layer_with_dbt_env.py

"""
from importlib.metadata import version, PackageNotFoundError

for pkg in ['dbt-core', 'dbt-duckdb', 'mashumaro']:
    try:
        print(f"{pkg}: {version(pkg)}")
    except PackageNotFoundError:
        print(f"{pkg}: not installed")








