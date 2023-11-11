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

# install requirements
conda install pytorch torchvision -c pytorch
See https://pytorch.org/get-started/locally/

conda install -c huggingface transformers 
See https://github.com/huggingface/transformers



# go to path
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_translation_gradio/002_mlearning_ai/

# launch the file
python 002_translate.py


! STOP
Check https://pytorch.org/get-started/locally/
AutoModelForSeq2SeqLM requires the PyTorch library but it was not found in your environment. Checkout the instructions on the installation page: https://pytorch.org/get-started/locally/ and follow the ones that match your environment. Please note that you may need to restart your runtime after installation.


"""

checkpoint = 'facebook/nllb-200-distilled-600M'
# checkpoint = 'facebook/nllb-200-1.3B'
# checkpoint = 'facebook/nllb-200-3.3B'
# checkpoint = 'facebook/nllb-200-distilled-1.3B'


from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

# INPUT_FR
# text = """La Chine reprend les pandas géants qu’elle avait prêtés aux zoos américains. A quelques jours de la rencontre entre les présidents américain, Joe Biden, et chinois, Xi Jinping, le 15 novembre à San Francisco, les ursidés vedettes du zoo de Washington ont repris le chemin de leur pays natal, à la grande déception des Américains."""

# INPUT_ES
# text = """Navarra es la primera comunidad que ofrece justicia restaurativa a las víctimas de abusos en la Iglesia. El servicio se ofrecerá a partir de enero, tras dos intervenciones pioneras, con el objetivo de ayudar a la reparación moral de los afectados"""


# INPUT_EN
text = """F.B.I. Seizes Eric Adams's Phones as Campaign Investigation Intensifies. Days after a raid at Mr. Adams's chief fund-raiser's home, federal agents took the mayor's phones and iPad, two people with knowledge of the matter said."""

# INPUT_IT
# text = """Trovare un impresa interessata a realizzare la nuova stazione Pigneto è impossibile. Anche la seconda gara per realizzare il nodo di scambio (in teoria previsto per il Giubileo) è andata deserta. Nessuno – e c'era un mese di tempo – si è presentato a fronte dei 101 milioni di lavori in palio."""

# INPUT LANGUAGES
# input_lang = 'fra_Latn'
# input_lang = 'spa_Latn'
input_lang = 'eng_Latn'
# input_lang = 'ita_Latn'

# TARGET LANGUAGES
# target_lang = 'fra_Latn'
# target_lang = 'spa_Latn'
# target_lang = 'eng_Latn'
target_lang = 'ita_Latn'


# translation_pipeline = pipeline('translation', 
#                                 model=model, 
#                                 tokenizer=tokenizer, 
#                                 src_lang=input_lang, 
#                                 tgt_lang=target_lang, 
#                                 max_length = 400)

translation_pipeline = pipeline('translation', 
                                model=model, 
                                tokenizer=tokenizer, 
                                src_lang=input_lang, 
                                tgt_lang=target_lang, 
                                max_length = 400)


output = translation_pipeline(text)
print(output[0]['translation_text'])




