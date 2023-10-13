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
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_openai_whisper/ffmpeg_python/

python 001_ffmpeg_python.py

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


pip install ffmpeg-python


"""


import ffmpeg

# TEST_1
# video = ffmpeg.input('sample_15s.mp4')
# video = video.trim(start=5, duration=5)
# video = ffmpeg.output(video, 'output_sample_5s.mp4')
# ffmpeg.run(video)

# TEST_2
# probe = ffmpeg.probe('output_sample_5s.mp4')
# video = next(
#     (stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
# width = int(video['width'])
# height = int(video['height'])
# print("Width:", width)
# print("Height:", height)

# TEST_3
# video = ffmpeg.input('sample_15s.mp4', ss=4)
# video = video.filter('scale', 500, -1)
# video = ffmpeg.output(video, 'output_sample_5s.png', vframes=1)
# ffmpeg.run(video)








