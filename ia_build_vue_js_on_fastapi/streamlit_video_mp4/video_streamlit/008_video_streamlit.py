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
streamlit run 008_video_streamlit.py


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
# video_path = "data/vroux_black_history_month_light.mp4"
# subtitles_path="data/vroux_black_history_month_light_FR.vtt"
# st.video(video_path, subtitles=Path(subtitles_path))                 

# display .vtt
# st.write(subtitles_path)
# display json
# st.json(transcript)



# VTT
vtt_content = '''WEBVTT

1
00:00.000 --> 00:05.000
Dans les écoles, sur les terrains de basket, comme à la Maison Blanche, chaque année en 

2
00:05.000 --> 00:11.000
février, les États -Unis fêtent le Black History Month, le mois de l'histoire des noirs. 

3
00:11.000 --> 00:16.000
Cela fait bientôt 100 ans de ce rendez -vous historique existe, mais d 'où vient cette 

4
00:16.000 --> 00:17.000
célébration ? 

5
00:18.000 --> 00:21.000
C'est Carter Gottwin Woodson qui a eu cette idée. 

6
00:21.000 --> 00:27.000
Ce fils de deux esclaves affranchis est considéré comme le père de l'histoire afro -américaine. 

7
00:27.000 --> 00:33.000
Il est seulement le deuxième homme noir à avoir obtenu un diplôme de l'université de Harvard. 

8
00:33.000 --> 00:38.000
Et 50 ans après l'abolition de l'esclavage, il lance l'idée d'une Negro History Week 

9
00:38.000 --> 00:41.000
dans la première édition à lieu en 1926. 

10
00:41.000 --> 00:46.000
Woodson veut encourager les afro-américains à s'intéresser davantage à leur histoire 

11
00:46.000 --> 00:49.000
et surtout, il veut que celle-ci soit enseignée dans les écoles. 

12
00:50.000 --> 00:54.000
Il choisit la deuxième semaine de février pour cette célébration car c'est à la 

13
00:54.000 --> 00:59.000
fois l'anniversaire d'Abraham Lincoln et de Frédéric Douglas, les deux grandes figures 

14
00:59.000 --> 01:00.000
de l'abolitionnisme aux États -Unis. 

15
01:01.000 --> 01:05.000
Peu à peu, le rendez -vous s'impose dans les Etats et les villes les plus progressistes. 

16
01:05.000 --> 01:09.000
Woodson meurt en 1950, mais son idée lui survit. 

17
01:09.000 --> 01:15.000
En 1976, pour le bicentenaire des États-Unis, le président Gerald Ford en fait une célébration 

18
01:15.000 --> 01:20.000
officielle et la semaine devient un mois de l'histoire des noirs. 

19
01:20.000 --> 01:26.000
En 2016, Barack Obama en fait le 40e anniversaire par ses mots depuis nos origines, 

20
01:26.000 --> 01:29.000
l'histoire des noirs, c'est l'histoire des États-Unis. 
'''

# SRT
srt_content = '''1
00:00:00,000 --> 00:00:05,140
Dans les écoles, sur les terrains de basket, comme à la Maison Blanche, chaque année en 

2
00:00:05,140 --> 00:00:11,240
février, les États -Unis fêtent le Black History Month, le mois de l 'histoire des noirs. 

3
00:00:11,500 --> 00:00:16,520
Cela fait bientôt 100 ans de ce rendez -vous historique existe, mais d 'où vient cette 

4
00:00:16,520 --> 00:00:17,520
célébration ? 

5
00:00:18,740 --> 00:00:21,680
C'est Carter Gottwin Woodson qui a eu cette idée. 

6
00:00:21,940 --> 00:00:27,640
Ce fils de deux esclaves affranchis est considéré comme le père de l 'histoire afro -américaine. 

7
00:00:27,640 --> 00:00:33,160
Il est seulement le deuxième homme noir à avoir obtenu un diplôme de l 'université de Harvard. 

8
00:00:33,540 --> 00:00:38,860
Et 50 ans après l'abolition de l'esclavage, il lance l'idée d'une Negro History Week 

9
00:00:38,860 --> 00:00:41,460
dans la première édition à lieu en 1926. 

10
00:00:41,860 --> 00:00:46,540
Woodson veut encourager les afro-américains à s'intéresser davantage à leur histoire 

11
00:00:46,540 --> 00:00:49,980
et surtout, il veut que celle-ci soit enseignée dans les écoles. 

12
00:00:50,200 --> 00:00:54,380
Il choisit la deuxième semaine de février pour cette célébration car c 'est à la 

13
00:00:54,380 --> 00:00:59,220
fois l 'anniversaire d 'Abraham Lincoln et de Frédéric Douglas, les deux grandes figures 

14
00:00:59,220 --> 00:01:00,940
de l'abolitionnisme aux États -Unis. 

15
00:01:01,240 --> 00:01:05,480
Peu à peu, le rendez -vous s'impose dans les Etats et les villes les plus progressistes. 

16
00:01:05,800 --> 00:01:09,640
Woodson meurt en 1950, mais son idée lui survit. 

17
00:01:09,900 --> 00:01:15,940
En 1976, pour le bicentenaire des États-Unis, le président Gerald Ford en fait une célébration 

18
00:01:15,940 --> 00:01:20,460
officielle et la semaine devient un mois de l'histoire des noirs. 

19
00:01:20,460 --> 00:01:26,660
En 2016, Barack Obama en fait le 40e anniversaire par ses mots depuis nos origines, 

20
00:01:26,860 --> 00:01:29,440
l 'histoire des noirs, c'est l'histoire des États -Unis. 
'''

# Display the video
video_path = "../data/208314_very_small.mp4"

vtt = io.BytesIO(vtt_content.encode('utf-8'))
srt = io.BytesIO(srt_content.encode('utf-8'))

st.video(video_path, subtitles={"French VTT": vtt, "French SRT": srt})

