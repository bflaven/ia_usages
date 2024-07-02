#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name llm_integration_api_costs python=3.9.13
conda info --envs
source activate fmm_fastapi_poc
conda deactivate


# BURN AFTER READING
source activate fmm_fastapi_poc



# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n llm_integration_api_costs

# BURN AFTER READING
conda env remove -n mistral_integration


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
pip install openai
pip install mistralai
pip install langchain-mistralai
pip install beautifulsoup4

python -m pip install beautifulsoup4
python -m pip install openai

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/build_vue_js_on_fastapi/streamlit_video_mp4/video_streamlit/

# launch the file
streamlit run 006_video_streamlit.py


[source]
https://doc-video-subtitle-inputs.streamlit.app/
"""

import streamlit as st
import json
import pandas as pd

# add specific
from pathlib import Path
import io

# Set the title of the Streamlit app
st.title("Video Player")


# st.video("sintel-short.mp4", subtitles="subtitles-en.vtt")
# st.video("sintel-short.mp4", subtitles=Path("subtitles-en.vtt"))
# st.video("sintel-short.mp4", subtitles={"English": "subtitles-en.srt", "Spanish": "subtitles-es.vtt"})
# st.video("sintel-short.mp4", subtitles={"":"", "German": "subtitles-de.vtt", "English": "subtitles-en.srt"})


   # Load the JSON transcript
transcript_path = "../data/vroux_black_history_month_light_FR.json"
with open(transcript_path, "r", encoding="utf-8") as f:
    transcript = json.load(f)


# Display the video
# video_path = "../data/208314_small.mp4"
# subtitles_path="../data/vroux_black_history_month_light_FR.vtt"
# st.video(video_path, subtitles=Path(subtitles_path))                 

# display .vtt
# st.write(subtitles_path)
# display json
# st.json(transcript)



# VTT
vtt_content = '''WEBVTT

1
00:00:01.700 --> 00:00:03.500
vtt_1 waterfall tree forest

2
00:00:04.700 --> 00:00:07.500
vtt_2 waterfall tree forest

3
00:00:08.700 --> 00:00:09.500
vtt_3 waterfall tree forest,
again and again

4
00:00:10.700 --> 00:00:11.500
vtt_4 Impressive and refreshing

5
00:00:12.700 --> 00:00:14.500
vtt_5 Thank you.

'''

# SRT
srt_content = '''1
1
00:00:01,700 --> 00:00:03,500
srt_1 waterfall tree forest

2
00:00:04,700 --> 00:00:07,500
srt_2 waterfall tree forest

3
00:00:08,700 --> 00:00:09,500
srt_3 waterfall tree forest,
again and again

4
00:00:10,700 --> 00:00:11,500
srt_4 Impressive and refreshing

5
00:00:12,700 --> 00:00:14,500
srt_5 Thank you.
'''

# Display the video
video_path = "../data/208314_very_small.mp4"

vtt = io.BytesIO(vtt_content.encode('utf-8'))
srt = io.BytesIO(srt_content.encode('utf-8'))

st.video(video_path, subtitles={"French VTT": vtt, "French SRT": srt})

