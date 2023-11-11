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
python 004_gradio_app_translate.py


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

title = "Translate Machine"

### TRANSLATE ### 
checkpoint = 'facebook/nllb-200-distilled-600M'

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

# INPUT_FR
# text = """La Chine reprend les pandas géants qu’elle avait prêtés aux zoos américains. A quelques jours de la rencontre entre les présidents américain, Joe Biden, et chinois, Xi Jinping, le 15 novembre à San Francisco, les ursidés vedettes du zoo de Washington ont repris le chemin de leur pays natal, à la grande déception des Américains."""

# INPUT_ES
# text = """Navarra es la primera comunidad que ofrece justicia restaurativa a las víctimas de abusos en la Iglesia. El servicio se ofrecerá a partir de enero, tras dos intervenciones pioneras, con el objetivo de ayudar a la reparación moral de los afectados"""


# INPUT_EN
# text = """F.B.I. Seizes Eric Adams's Phones as Campaign Investigation Intensifies. Days after a raid at Mr. Adams's chief fund-raiser's home, federal agents took the mayor's phones and iPad, two people with knowledge of the matter said."""

# INPUT_IT
# text = """Trovare un impresa interessata a realizzare la nuova stazione Pigneto è impossibile. Anche la seconda gara per realizzare il nodo di scambio (in teoria previsto per il Giubileo) è andata deserta. Nessuno – e c'era un mese di tempo – si è presentato a fronte dei 101 milioni di lavori in palio."""


### UX ### 
def translate_builder(input_lang, target_lang):
    return f"""{input_lang} {target_lang}"""


# INPUT LANGUAGES
input_lang = ['ita_Latn', 'eng_Latn', 'spa_Latn', 'fra_Latn']

# TARGET LANGUAGES
target_lang = ['ita_Latn', 'eng_Latn', 'spa_Latn', 'fra_Latn']



translateDemoUx = gr.Interface(
    translate_builder,
    [
        gr.Dropdown(input_lang),
        gr.Dropdown(target_lang),
    ],
    "text")




if __name__ == "__main__":
    translateDemoUx.launch()


