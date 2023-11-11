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

# install langdetect
pip install langdetect
conda install -c conda-forge langdetect
See https://pypi.org/project/langdetect/


# go to path
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_translation_gradio/002_mlearning_ai/

# launch the file
python 001_langdetect.py





"""

from langdetect import detect

# EN (eng_Latn stands for English in Latin.)
# text = "War doesn't show who's right, just who's left."

# DE (deu_Latn stands for German in Latin)
text = "Die Grenzen meiner Sprache bedeuten die Grenzen meiner Welt."

# AR (arb_Arab stands for Standard Arabic in Arabic)
# text = "ومنح ذلك بايسرز التقدم 122-121 ولم يتأخروا مرة أخرى في المباراة التي كانوا يتقدمون فيها بما يصل إلى 18 نقطة في الشوط الأول، قبل أن يعيد أنتيتوكونمبو فريق باكس إلى المباراة."

# ES (spa_Latn stands for Spanish in Latin)
# text = "Tener en la despensa o la nevera legumbres cocidas permite preparar salteados sencillos en cuestión de minutos. Se pueden completar con ingredientes de temporada y ese huevo que lo mejora todo"

# IT (ita_Latn stands for Italian in Latin)
# text = "Nulla da fare, trovare un’impresa interessata a realizzare la nuova stazione Pigneto è impossibile. Anche la seconda gara per realizzare il nodo di scambio (in teoria previsto per il Giubileo) è andata deserta. Nessuno – e c’era un mese di tempo – si è presentato a fronte dei 101 milioni di lavori in palio."



predictions = detect(text)
print(predictions)

