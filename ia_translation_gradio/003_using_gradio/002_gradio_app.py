#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda ia_translation_facebook_nllb
conda create --name ia_translation_facebook_nllb python=3.9.13
conda info --envs
source activate ia_translation_facebook_nllb
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_translation_facebook_nllb

# update conda 
conda update -n base -c defaults conda


# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# install gradio
pip install gradio
conda install -c conda-forge gradio



# go to path
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_translation_gradio/003_using_gradio/

# launch the file
python 002_gradio_app.py


# check
The demo pop in a browser on 
http://localhost:7860 
or 
http://127.0.0.1:7860


More examples

https://github.com/gradio-app/gradio
https://github.com/yiskw713/gradio_sample
"""

import gradio as gr

title = "Multiple Interfaces"

#app 1
def user_greeting(name):
    return "Hi! " + name + " Welcome to your first Gradio application!😎"

#app 2
def user_help(do):
    return "So today we will do " + do + "using Gradio. Great choice!"

#interface 1
app1 =  gr.Interface(fn = user_greeting, inputs="text", outputs="text")
#interface 2

app2 =  gr.Interface(fn = user_help, inputs="text", outputs="text")

demo = gr.TabbedInterface([app1, app2], ["Welcome", "What to do"])

if __name__ == "__main__":
    demo.launch()


    