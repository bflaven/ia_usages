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
streamlit run 0007_semantic_layer_with_dbt_streamlit.py



"""


import streamlit as st
import duckdb
import pandas as pd
import yaml
import os

# Path to your DuckDB database (update this to match your dbt profile)
# DUCKDB_PATH = 'path/to/your/duckdb/database.duckdb'
DUCKDB_PATH = '/Users/brunoflaven/Documents/03_git/ia_usages/ia_semantic_layer/semantic_layer_with_dbt/db/duckdb-demo.duckdb'

# Path to your dbt schema YAML (optional: for reading metadata)
DBT_SCHEMA_YML = 'models/bank_app/schema.yml'

st.set_page_config(page_title="Bank Failures Dashboard", layout="wide")

st.title("🏦 Bank Failures Dashboard (dbt + Streamlit)")
st.markdown("Interactive dashboard showing aggregated bank failures by state, powered by dbt models.")

# Connect to DuckDB and query the clean_bank_failures model
try:
    con = duckdb.connect(DUCKDB_PATH, read_only=True)
    df = con.execute("SELECT * FROM clean_bank_failures ORDER BY total_failures DESC").df()
    con.close()
    
    if df.empty:
        st.warning("No data found in clean_bank_failures table.")
    else:
        # Sidebar Filters
        st.sidebar.header("🔍 Filters")
        
        # Filter by State (multiselect)
        all_states = df['State'].unique().tolist()
        selected_states = st.sidebar.multiselect(
            'Select State(s):',
            options=all_states,
            default=all_states
        )
        
        # Filter by minimum number of failures
        min_failures = st.sidebar.slider(
            'Minimum Failures:',
            min_value=int(df['total_failures'].min()),
            max_value=int(df['total_failures'].max()),
            value=int(df['total_failures'].min())
        )
        
        # Filter by minimum total assets
        min_assets = st.sidebar.slider(
            'Minimum Total Assets ($mil):',
            min_value=float(df['total_assets'].min()),
            max_value=float(df['total_assets'].max()),
            value=float(df['total_assets'].min())
        )
        
        # Apply filters
        filtered_df = df[
            (df['State'].isin(selected_states)) &
            (df['total_failures'] >= min_failures) &
            (df['total_assets'] >= min_assets)
        ]
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total States", len(filtered_df))
        with col2:
            st.metric("Total Bank Failures", int(filtered_df['total_failures'].sum()))
        with col3:
            st.metric("Total Assets ($mil)", f"{filtered_df['total_assets'].sum():,.2f}")
        
        st.markdown("---")
        
        # Display filtered data table
        st.subheader("📊 Filtered Data")
        st.dataframe(
            filtered_df.style.format({
                'total_failures': '{:,.0f}',
                'total_assets': '${:,.2f}M'
            }),
            use_container_width=True
        )
        
        st.markdown("---")
        
        # Charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("📈 Bank Failures by State")
            chart_data = filtered_df.set_index('State')['total_failures'].sort_values(ascending=False).head(10)
            st.bar_chart(chart_data)
        
        with col_chart2:
            st.subheader("💰 Total Assets by State")
            chart_data2 = filtered_df.set_index('State')['total_assets'].sort_values(ascending=False).head(10)
            st.bar_chart(chart_data2)
        
        st.markdown("---")
        
        # Optional: Show column descriptions from dbt YAML
        if os.path.isfile(DBT_SCHEMA_YML):
            with st.expander("📖 Column Descriptions (from dbt schema)"):
                with open(DBT_SCHEMA_YML, "r") as f:
                    docs = yaml.safe_load(f)
                    for model in docs.get("models", []):
                        if model["name"] == "clean_bank_failures":
                            for col in model.get("columns", []):
                                st.write(f"**{col['name']}**: {col.get('description', 'No description')}")
        
except Exception as e:
    st.error(f"❌ Could not fetch data: {e}")
    st.info("Make sure your DuckDB path is correct and dbt models have been built.")

st.markdown("---")
st.caption("📊 Data source: dbt model `clean_bank_failures` | Built with Streamlit")








