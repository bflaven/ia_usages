#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
# NO CONDA ENV
conda create --name chainlit_python python=3.9.13
conda info --envs
source activate chainlit_python
conda deactivate
# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
# examples
conda env remove -n po_launcher_e2e_cypress
conda env remove -n parse_website

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements_chainlit_python.txt


# to install
pip install -r requirements_chainlit_python.txt



[path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/ai_chatgpt_prompts/project_4_chainlit/

[file]
chainlit run 001_chainlit_python.py -w

The -w flag tells Chainlit to enable auto-reloading, so you don’t need to restart the server every time you make changes to your application. Your chatbot UI should now be accessible at http://localhost:8000.



# other module
# go to the env

# for chainlit
pip install chainlit




Source: https://docs.chainlit.io/pure-python

"""
 
import chainlit as cl


@cl.on_message
def main(message: str):
    # Your custom logic goes here...

    # Send a response back to the user
    cl.Message(
        content=f"Received: {message}",
    ).send()
