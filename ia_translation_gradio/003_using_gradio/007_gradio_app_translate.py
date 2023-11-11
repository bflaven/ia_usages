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
python 007_gradio_app_translate.py


# check
The demo pop in a browser on 
http://localhost:7860 
or 
http://127.0.0.1:7860


More examples

https://www.gradio.app/guides/using-hugging-face-integrations

"""
import gradio as gr

title = "Translate Machine"

# INPUT_EN
# text = """F.B.I. Seizes Eric Adams's Phones as Campaign Investigation Intensifies. Days after a raid at Mr. Adams's chief fund-raiser's home, federal agents took the mayor's phones and iPad, two people with knowledge of the matter said."""

# OUTPUT_ES
# El FBI se apodera de los teléfonos de Eric Adams mientras se intensifica la investigación de la campaña. Días después de una redada en la casa del Sr. Adams para recaudar fondos, agentes federales se llevaron los teléfonos del alcalde y el iPad, dos personas con conocimiento del asunto dijeron.

demo = gr.load("Helsinki-NLP/opus-mt-en-es", src="models")

if __name__ == "__main__":
    demo.launch()

