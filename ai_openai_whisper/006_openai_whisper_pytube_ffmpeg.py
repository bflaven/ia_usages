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


python 006_openai_whisper_pytube_ffmpeg.py

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
pip install pytube

pip install ffmpeg-python


"""

import whisper
import pandas as pd
import json
from pytube import YouTube
import os

# ffmpeg -version

# presentation starts from 32:04 and ends at 1:13:59 
# QA starts from 1:13:59
# https://www.metric-conversions.org/time/minutes-to-seconds.htm


# ffmpeg -ss 1924 -i "/Users/brunoflaven/Documents/01_work/blog_articles/openai_whisper/test_earnings_call_microsoft_q4_2022/Microsoft (MSFT) Q4 2022 Earnings Call.mp4" -t 2515 "earnings_call_microsoft_q4_2022_filtered.mp4"


# if you need to cut the video to get the audio only bacause there is music at the beginning
cmd = 'ffmpeg -ss 1924 -i "test_earnings_call_microsoft_q4_2022/Microsoft (MSFT) Q4 2022 Earnings Call.mp4" -t 2515 "earnings_call_microsoft_q4_2022_filtered.mp4"'
os.system(cmd)

print(f'\n\n EXTRACTED MADE')


# subprocess.call('ffmpeg -r 10 -i frame%03d.png -r ntsc '+str(out_movie), shell=True)


