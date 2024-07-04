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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_build_vue_js_on_fastapi/streamlit_video_mp4/video_streamlit/


# launch the file
streamlit run 003_video_streamlit.py


[source]
https://doc-video-subtitle-inputs.streamlit.app/
"""

import streamlit as st
from pathlib import Path
import io


# Set the title of the Streamlit app
st.title("Video Player")

vtt = '''
WEBVTT

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

srt = '''
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


st.video("../data/208314_very_small.mp4", subtitles={"English VTT": vtt, "English SRT": srt})

# st.video("../data/208314_very_small.mp4", subtitles={"English VTT": vtt})

# st.video("../data/208314_very_small.mp4", subtitles={"English SRT": srt})




