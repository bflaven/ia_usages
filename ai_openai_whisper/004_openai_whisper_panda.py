#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name openai_whisper python=3.9.13
conda info --envs
source activate openai_whisper
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n openai_whisper

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_openai_whisper/

python 004_openai_whisper_panda.py

[Source]
Source: https://github.com/openai/whisper/tree/main
git clone https://github.com/openai/whisper.git

[MODELS AND LANGUAGES]
Available models and languages
There are five model sizes, four with English-only versions, offering speed and accuracy tradeoffs. Below are the names of the available models and their approximate memory requirements and relative speed.

tiny
base
small
medium
large

See https://github.com/openai/whisper/tree/main#available-models-and-languages


pip install -U openai-whisper
pip install setuptools-rust

pip install pandas

"""
"""

- english
060123_john_willinsky_economics_knowledge_public.mp3
sample_0.mp3
sample_1.mp3
sample_2.mp3
sample_3.mp3
sample_4.mp3

- foreign
ar_sample_1.mp3
cn_sample_1.mp3
fr_sample_1.mp3
ru_sample_1.mp3
sp_sample_1.mp3

- more audio samples
https://commons.wikimedia.org/wiki/Category:Audio_files_of_speeches
https://audio-samples.github.io/
https://audio-lingua.ac-versailles.fr/?lang=en


"""

import whisper
import pandas as pd

# english
# audio_input = "audio_files_sources/english/sample_1.mp3"
# file_output = "003_openai_whisper_en_sample_1_output.txt"
# language_selected="english"

# russian
# audio_input = "audio_files_sources/foreign/ru_sample_1.mp3"
# file_output = "003_openai_whisper_ru_sample_1_output.txt"
# language_selected="russian"

# spanish
audio_input = "audio_files_sources/english/sample_1.mp3"
file_output = "003_openai_whisper_en_sample_1_output.txt"
file_output_csv = "003_openai_whisper_en_sample_1_output.csv"
language_selected="english"


# load audio and pad/trim it to fit 30 seconds
model = whisper.load_model("base")
result = model.transcribe(audio_input, fp16=False, verbose=True, language=language_selected)



# for i, seg in enumerate(result['segments']):
#   print(i+1, "- ", seg['text'])


df = pd.DataFrame.from_dict(result['segments'])

# displaying the DataFrame
# print('DataFrame:\n', df) 
# print('df.head(5):\n', df.head(5)) 



# saving the DataFrame as a CSV file 
gfg_csv_data = df.to_csv(file_output_csv, index = False) 

print(f'\n\n--- panda csv file for {audio_input} into {file_output_csv}')
