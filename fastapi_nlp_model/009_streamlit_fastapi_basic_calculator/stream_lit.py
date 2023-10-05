#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name streamlit_fastapi python=3.9.13
conda info --envs
source activate streamlit_fastapi
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n streamlit_fastapi

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/fastapi_nlp_model/009_streamlit_fastapi_basic_calculator/

# Launch the streamlit app
streamlit run stream_lit.py

# check
http://localhost:8501/


"""
import streamlit as st
import json
import requests

st.title("Basic Caculator App 🧮")

# taking user inpputs
option = st.selectbox('What operation You want to perform?',
                     ('Addition', 'Subtraction', 'Multiplication', 'Division'))
st.write("")
st.write("Select the numbers from slider below 👇")
x = st.slider("X", 0, 100, 20)
y = st.slider("Y", 0, 130, 10)

#converting the inputs into a json format
inputs = {"operation": option,   "x": x,  "y": y}

# when the user clicks on button it will fetch the API
if st.button('Calculate'):
    res = requests.post(url = "http://127.0.0.1:8000/calculate", data = json.dumps(inputs))

    # st.code(inputs)
    st.subheader(f"Response from API 🚀  =  {res.text}")





