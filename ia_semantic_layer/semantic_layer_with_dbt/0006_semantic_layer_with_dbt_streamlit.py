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
streamlit run 0006_semantic_layer_with_dbt_streamlit.py

"""


import streamlit as st
import duckdb
import pandas as pd
import yaml
import os

# Path to your DuckDB database (use the same as your dbt profile)
# DUCKDB_PATH = 'path/to/your/duckdb/database.duckdb'
DUCKDB_PATH = '/Users/brunoflaven/Documents/03_git/ia_usages/ia_semantic_layer/semantic_layer_with_dbt/db/duckdb-demo.duckdb'




# Path to your dbt model (optional: for reading metadata)
DBT_SCHEMA_YML = 'models/bank_app/schema.yml'

st.title("Bank Failures Dashboard (dbt + Streamlit)")

# Connect to DuckDB and query the clean_bank_failures model
try:
    con = duckdb.connect(DUCKDB_PATH)
    df = con.execute("SELECT * FROM clean_bank_failures").df()
    st.subheader("Aggregated Bank Failures by State")
    st.dataframe(df)
except Exception as e:
    st.error(f"Could not fetch data: {e}")

# Optional: Show column comments (metadata) from dbt YAML
if os.path.isfile(DBT_SCHEMA_YML):
    st.subheader("Column Descriptions (from dbt)")
    with open(DBT_SCHEMA_YML, "r") as f:
        docs = yaml.safe_load(f)
        for model in docs.get("models", []):
            if model["name"] == "clean_bank_failures":
                for col in model.get("columns", []):
                    st.write(f"**{col['name']}**: {col.get('description', '')}")

st.info("This app fetches data built by dbt and displays metadata from your dbt project.")










