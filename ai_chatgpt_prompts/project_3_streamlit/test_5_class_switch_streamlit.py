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
streamlit run test_5_class_switch_streamlit.py


https://stackoverflow.com/questions/65602056/how-to-set-and-access-environment-variables-in-python-file-for-streamlit-app

https://techcommunity.microsoft.com/t5/healthcare-and-life-sciences/integrating-azure-openai-with-streamlit-with-example-source-code/ba-p/3809006

https://github.com/ajitdash/pview/blob/main/explaincode.py


pip install openai
pip install streamlit
pip install python-dotenv

"""
import streamlit as st

# personal configuration
import config_values.values_conf as conf

### 1. VALUES ###
TEXT_TITLE_APP = conf.TEXT_TITLE_APP
TEXT_SUBHEADER_APP = conf.TEXT_SUBHEADER_APP
TEXT_WARNING = conf.TEXT_WARNING
TEXT_OUTPUT = conf.TEXT_OUTPUT

LABEL_EXPANDER = conf.LABEL_EXPANDER

# Usecase Title
MENU_SIDEBAR_USECASE_TITLE_OPTIONS = conf.MENU_SIDEBAR_USECASE_TITLE_OPTIONS

TEXT_HELP_1 = conf.TEXT_HELP_1


class CaseChatGptDrawMainAppBody:

    def __init__(self):
        self.options = MENU_SIDEBAR_USECASE_TITLE_OPTIONS
        self.menu = st.sidebar.selectbox(
            "Menu options", self.options, help=TEXT_HELP_1)

    def detectVersion(self):
        st.sidebar.markdown('* * *')
        st.sidebar.markdown('**VERSIONS**')
        st.sidebar.write("streamlit ::", st.__version__)

    def doApp(self):
        
        st.header(f'{TEXT_TITLE_APP}')
        st.markdown(f'{TEXT_SUBHEADER_APP}')
        st.warning(f'{TEXT_WARNING}')
        
        selected_case = self.options.index(self.menu)
        for i, option in enumerate(self.options):
            if i == selected_case:
                st.markdown(f'{option}')

    def run(self):
        self.doApp()
        self.detectVersion()


# Example usage
app = CaseChatGptDrawMainAppBody()
app.run()
