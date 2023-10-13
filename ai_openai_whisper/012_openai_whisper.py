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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ai_openai_whisper/


python 012_openai_whisper.py

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


- source
https://wandb.ai/wandb_fc/gentle-intros/reports/OpenAI-Whisper-How-to-Transcribe-Your-Audio-to-Text-for-Free-with-SRTs-VTTs---VmlldzozNDczNTI0

https://github.com/openai/whisper/discussions/98


"""


# english
audio_input = "audio_files_sources/english/sample_1.mp3"
file_output = "003_openai_whisper_en_sample_1_output..srt"
language_selected="english"

# russian
# audio_input = "audio_files_sources/foreign/ru_sample_1.mp3"
# file_output = "003_openai_whisper_ru_sample_1_output.txt"
# language_selected="russian"

# arabic
# audio_input = "audio_files_sources/foreign/ar_sample_1.mp3"
# file_output = "003_openai_whisper_ar_sample_1_output.txt"
# language_selected="arabic"

# chinese
# audio_input = "audio_files_sources/foreign/cn_sample_1.mp3"
# file_output = "003_openai_whisper_cn_sample_1_output.txt"
# language_selected="chinese"

# spanish
# audio_input = "audio_files_sources/foreign/sp_sample_1.mp3"
# file_output = "003_openai_whisper_sp_sample_1_output.txt"
# language_selected="spanish"


import whisper
from datetime import timedelta
import os


def transcribe_audio(path):
    model = whisper.load_model("base") # Change this to your desired model
    print("Whisper model loaded.")
    transcribe = model.transcribe(audio=path, fp16=False, verbose=True, language=language_selected)
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        srtFilename = os.path.join("output_srtfiles_writer", f"{file_output}")
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    return srtFilename

# launch
transcribe_audio(audio_input)
