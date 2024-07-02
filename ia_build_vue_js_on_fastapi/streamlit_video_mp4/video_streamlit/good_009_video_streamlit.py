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
streamlit run good_009_video_streamlit.py


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

# Load VTT content from file
vtt_file_path = "../data/vroux_black_history_month_light_FR.vtt"
with open(vtt_file_path, 'r', encoding='utf-8') as vtt_file:
    vtt_content = vtt_file.read()

# Load SRT content from file
srt_file_path = "../data/vroux_black_history_month_light_FR.srt"
with open(srt_file_path, 'r', encoding='utf-8') as srt_file:
    srt_content = srt_file.read()

# Display the video
video_path = "../data/208314_very_small.mp4"

vtt = io.BytesIO(vtt_content.encode('utf-8'))
srt = io.BytesIO(srt_content.encode('utf-8'))

st.video(video_path, subtitles={"French VTT": vtt, "French SRT": srt})

