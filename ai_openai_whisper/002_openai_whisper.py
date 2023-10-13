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


python 002_openai_whisper.py

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
import whisper


model = whisper.load_model("base")

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

audio_input = "fr_sample_1.mp3"
file_output = "fr_sample_1_text_output.txt"

# load audio and pad/trim it to fit 30 seconds
# audio = whisper.load_audio("audio_files_sources/060123_john_willinsky_economics_knowledge_public.mp3")
# audio = whisper.load_audio("audio_files_sources/english/sample_4.mp3")
audio = whisper.load_audio("audio_files_sources/foreign/"+audio_input)

audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
# options = whisper.DecodingOptions()
options = whisper.DecodingOptions(fp16 = False)
result = whisper.decode(model, mel, options)

# print the recognized text
print(result.text)

with open(file_output, 'w') as f:
    f.write(result.text)

print(f'\n--- DONE for {audio_input} into {file_output}')

