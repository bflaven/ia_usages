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
pip install sacremoses
conda install -c conda-forge gradio

conda install -c conda-forge sentencepiece
https://pypi.org/project/sentencepiece/

conda install -c conda-forge sacremoses
https://pypi.org/project/sentencepiece/


Model: https://www.gradio.app/guides/using-hugging-face-integrations

# go to path
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_translation_gradio/003_using_gradio/

# launch the file
python 006_gradio_app_translate.py


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
from transformers import pipeline

title = "Translate Machine"

pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-en-es")

def predict(text):
  return pipe(text)[0]["translation_text"]

demo = gr.Interface(
  fn=predict,
  inputs='text', # input in english only
  outputs='text', # output in spanish only
)
if __name__ == "__main__":
    demo.launch()

