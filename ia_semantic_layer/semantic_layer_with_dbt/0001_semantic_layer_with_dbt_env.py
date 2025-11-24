#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[check]
pip --version
python --version

[env]

pip install --upgrade pip


# 1. Install virtualenvwrapper:
pip install virtualenvwrapper

# 2. Add to your shell config (e.g., `~/.zshrc` or `~/.bashrc`):
export WORKON_HOME=$HOME/.virtualenvs

## Source the shell config or restart terminal afterward.
source $(which virtualenvwrapper.sh)

# 3. Commands for environment management:

## Create and activate a new environment
mkvirtualenv myenv
vcreate semantic_layer_with_dbt

## Deactivate (always use `deactivate` command)
vdeactivate

## Reactivate environment
workon myenv
vactivate semantic_layer_with_dbt

## Remove an environment
rmvirtualenv myenv
vremove semantic_layer_with_dbt

## List all environments
vlist


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
python 0001_semantic_layer_with_dbt_env.py

"""

""" """

try:
    import dbt.adapters.duckdb
    print("dbt-duckdb loaded successfully")
except ImportError as e:
    print(f"Failed to load dbt-duckdb: {e}")

try:
    import duckdb
    print("duckdb loaded successfully")
except ImportError as e:
    print(f"Failed to load duckdb: {e}")

try:
    import pandas as pd
    print("pandas loaded successfully")
except ImportError as e:
    print(f"Failed to load pandas: {e}")


"""
from importlib.metadata import version, PackageNotFoundError

for pkg in ['dbt-core', 'dbt-duckdb', 'mashumaro']:
    try:
        print(f"{pkg}: {version(pkg)}")
    except PackageNotFoundError:
        print(f"{pkg}: not installed")
"""








