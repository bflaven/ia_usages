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


python 006_openai_whisper_pytube.py

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


"""

import whisper
import pandas as pd
import json
from pytube import YouTube


# youtube_video_url = "https://www.youtube.com/watch?v=3haowENzdLo"
 
# a video made by me
youtube_video_url = "https://www.youtube.com/watch?v=W7mAMECbNsY"
youtube_video_content = YouTube(youtube_video_url)

# V1
# for stream in youtube_video_content.streams:
#   print(stream)
  
# V2 select audio only 
audio_streams = youtube_video_content.streams.filter(only_audio=True)

# for stream in audio_streams:
#   print(stream)

# output
"""
<Stream: itag="139" mime_type="audio/mp4" abr="48kbps" acodec="mp4a.40.5" progressive="False" type="audio">
<Stream: itag="140" mime_type="audio/mp4" abr="128kbps" acodec="mp4a.40.2" progressive="False" type="audio">
<Stream: itag="251" mime_type="audio/webm" abr="160kbps" acodec="opus" progressive="False" type="audio">

"""

audio_stream = audio_streams[1]
# print(audio_stream)

# audio_streams.download("video_download_from_yt.mp4")
# abr="48kbps"
# abr="128kbps"
# abr="160kbps"

yt = youtube_video_content.streams.filter(only_audio=True, subtype='mp4', abr='48kbps').first().download('video_download_from_yt')


print(f'\n\n audio download done {yt}')


# Other commanns 
# ffmpeg -version

# presentation starts from 32:04 and ends at 1:13:59 
# QA starts from 1:13:59
# https://www.metric-conversions.org/time/minutes-to-seconds.htm

# ffmpeg -ss 1924 -i "/content/earnings_call_microsoft_q4_2022.mp4/Microsoft (MSFT) Q4 2022 Earnings Call.mp4" -t 2515 "earnings_call_microsoft_q4_2022_filtered.mp4"
# 
# 
# 