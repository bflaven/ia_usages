#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
# NO CONDA ENV

conda create --name ai_chatgpt_prompts python=3.9.13
conda info --envs
source activate ai_chatgpt_prompts
conda deactivate
# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > ai_chatgpt_prompts.txt


# to install
pip install -r ai_chatgpt_prompts.txt

[path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/ai_chatgpt_prompts/project_3_streamlit/

[file]
streamlit run 001_project_3_python_streamlit_app_chatgpt_api.py

https://stackoverflow.com/questions/65602056/how-to-set-and-access-environment-variables-in-python-file-for-streamlit-app

https://techcommunity.microsoft.com/t5/healthcare-and-life-sciences/integrating-azure-openai-with-streamlit-with-example-source-code/ba-p/3809006

https://github.com/ajitdash/pview/blob/main/explaincode.py


pip install openai
pip install streamlit
pip install python-dotenv

"""

import os
import streamlit as st
from dotenv import load_dotenv


# WAY_1
# Everything is accessible via the st.secrets dict:

st.write("OPENAI_API_KEY_LOCAL:", st.secrets["OPENAI_API_KEY_LOCAL"])
st.write("DB password:", st.secrets["db_password"])
st.write("My cool secrets:", st.secrets["my_cool_secrets"]["things_i_like"])

# # And the root-level secrets are also accessible as environment variables:


st.write(
    "Has environment variables been set:",
    os.environ["db_username"] == st.secrets["db_username"],
)



# WAY_2
load_dotenv()  # Load environment variables from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Get API key from environment variable

st.code( "OPENAI_API_KEY: "+OPENAI_API_KEY)



