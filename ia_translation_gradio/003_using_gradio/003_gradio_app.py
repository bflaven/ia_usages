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
python 003_gradio_app.py


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

def sentence_builder(quantity, morning, activity_list, watch):
    return f"""{quantity} o'clock is a nice time take a {"morning" if morning else "later in the day"} glass of water {" and take a ".join(activity_list)} or watch a {watch}"""


demo = gr.Interface(
    sentence_builder,
    [   gr.Slider(2, 24, value=4, step = 2),
        gr.Checkbox(label="Is it before noon"),
        gr.CheckboxGroup(["juice", "beverage", "snack", "nap"]),
        gr.Dropdown(["Television series", "Movie", "Documentary", "Class"]),
     
    ],
    "text")

if __name__ == "__main__":
    demo.launch()


