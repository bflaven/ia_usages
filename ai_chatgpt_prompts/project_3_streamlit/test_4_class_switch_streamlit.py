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
streamlit run test_4_class_switch_streamlit.py


https://stackoverflow.com/questions/65602056/how-to-set-and-access-environment-variables-in-python-file-for-streamlit-app

https://techcommunity.microsoft.com/t5/healthcare-and-life-sciences/integrating-azure-openai-with-streamlit-with-example-source-code/ba-p/3809006

https://github.com/ajitdash/pview/blob/main/explaincode.py


pip install openai
pip install streamlit
pip install python-dotenv

"""

import streamlit as st


class CaseChatGptDrawMainAppBody:
    def __init__(self):
        self.options = ['USA', 'China', 'Russia', 'Italy']
        self.menu = st.sidebar.selectbox("Menu options", self.options)

    def run(self):
        if self.menu == 'USA':
            self.show_usa_content()
        elif self.menu == 'China':
            self.show_china_content()
        elif self.menu == 'Russia':
            self.show_russia_content()
        elif self.menu == 'Italy':
            self.show_italy_content()
        else:
            self.show_default_content()

    def show_usa_content(self):
        st.write("Content for USA")

    def show_china_content(self):
        st.write("Content for China")

    def show_russia_content(self):
        st.write("Content for Russia")

    def show_italy_content(self):
        st.write("Content for Italy")

    def show_default_content(self):
        st.write("Default content")


# Create an instance of the class and run it
app = CaseChatGptDrawMainAppBody()
app.run()



