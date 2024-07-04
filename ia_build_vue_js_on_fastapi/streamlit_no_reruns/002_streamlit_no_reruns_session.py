#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name llm_integration_api_costs python=3.9.13
conda info --envs
source activate fmm_fastapi_poc
conda deactivate


# BURN AFTER READING
source activate fmm_fastapi_poc



# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n llm_integration_api_costs

# BURN AFTER READING
conda env remove -n mistral_integration


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
pip install openai
pip install mistralai
pip install langchain-mistralai
pip install beautifulsoup4

python -m pip install beautifulsoup4
python -m pip install openai

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_build_vue_js_on_fastapi/streamlit_no_reruns/

# launch the file
streamlit run 001_streamlit_no_reruns_checkbox.py

https://www.youtube.com/watch?v=dPdB7zyGttg

https://discuss.streamlit.io/t/how-to-prevent-the-reloading-of-the-whole-page-when-i-let-the-user-to-perform-an-action/10800/9
https://blog.streamlit.io/introducing-submit-button-and-forms/


"""
import streamlit as st
import pandas as pd
import plotly.express as px

# Header
st.title("Fruits List")

# Create a dictionary
_dic = {
    "Name": ["Apple", "Banana", "Cherry", "Date", "Elderberry"],
    "Quantity": [10, 15, 7, 25, 5]
}

# Load dictionary into a pandas dataframe
_df = pd.DataFrame(_dic)

# Use the btn but use session to avoid streamlit to make a global post
# create a button
load = st.button('Load data')

# initialize session state
if "load_state" not in st.session_state:
    st.session_state.load_state = False



# Create a button to load the dataframe
if load or st.session_state.load_state:
    st.session_state.load_state = True
    st.write(_df)
    
    # Add radio options for plot type
    opt = st.radio('Plot type', ['Bar', 'Pie'])

    # Display the appropriate plot
    if opt == 'Bar':
        fig = px.bar(_df, x='Name', y='Quantity', title='Bar Plot of Fruits')
        st.plotly_chart(fig)
    elif opt == 'Pie':
        fig = px.pie(_df, names='Name', values='Quantity', title='Pie Chart of Fruits')
        st.plotly_chart(fig)

