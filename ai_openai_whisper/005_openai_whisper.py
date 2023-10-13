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

python 005_openai_whisper.py

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


"""

import whisper
import pandas as pd
import json


# english
# audio_input = "audio_files_sources/english/sample_1.mp3"
# file_output = "003_openai_whisper_en_sample_1_output.txt"
# language_selected="english"

# russian
audio_input = "audio_files_sources/foreign/ru_sample_1.mp3"
file_output = "003_openai_whisper_ru_sample_1_output.txt"
language_selected="russian"

# spanish
# audio_input = "audio_files_sources/foreign/sp_sample_1.mp3"
# file_output = "003_openai_whisper_sp_sample_1_output.txt"
# language_selected="spanish"

# arabic
# audio_input = "audio_files_sources/foreign/ar_sample_1.mp3"
# file_output = "003_openai_whisper_ar_sample_1_output.txt"
# language_selected="arabic"

audio = whisper.load_audio(audio_input)
audio = whisper.pad_or_trim(audio)

model = whisper.load_model("base")
mel = whisper.log_mel_spectrogram(audio).to(model.device)

_, probs = model.detect_language(mel)

# dump the possible languages

# in normal output
# print(f"probs: {probs}")

# in json format
# print(f"obj: {json.dumps(probs, indent=4)}")

# detect the spoken language
# _, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")




