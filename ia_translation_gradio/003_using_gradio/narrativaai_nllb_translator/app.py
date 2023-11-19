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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_translation_gradio/003_using_gradio/narrativaai_nllb_translator/


# launch the file
python app.py


# check
The demo pop in a browser on 
http://localhost:7860 
or 
http://127.0.0.1:7860


More examples

https://huggingface.co/spaces/Geonmo/nllb-translation-demo


"""

import gradio as gr
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
from ui import title, description, examples
from langs import LANGS

TASK = "translation"
CKPT = "facebook/nllb-200-distilled-600M"

model = AutoModelForSeq2SeqLM.from_pretrained(CKPT)
tokenizer = AutoTokenizer.from_pretrained(CKPT)

device = 0 if torch.cuda.is_available() else -1


def translate(text, src_lang, tgt_lang, max_length=400):
    """
    Translate the text from source lang to target lang
    """
    translation_pipeline = pipeline(TASK,
                                    model=model,
                                    tokenizer=tokenizer,
                                    src_lang=src_lang,
                                    tgt_lang=tgt_lang,
                                    max_length=max_length,
                                    device=device)

    result = translation_pipeline(text)
    return result[0]['translation_text']


gr.Interface(
    translate,
    [
        gr.components.Textbox(label="Text"),
        gr.components.Dropdown(label="Source Language", choices=LANGS),
        gr.components.Dropdown(label="Target Language", choices=LANGS),
        gr.components.Slider(8, 512, value=400, step=8, label="Max Length")
    ],
    ["text"],
    examples=examples,
    # article=article,
    cache_examples=False,
    title=title,
    description=description
).launch()



 



