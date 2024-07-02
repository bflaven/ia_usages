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
cd /Users/brunoflaven/Documents/01_work/blog_articles/streamlit_no_reruns/

# launch the file
streamlit run 004_streamlit_no_reruns.py

https://www.youtube.com/watch?v=dPdB7zyGttg

https://discuss.streamlit.io/t/how-to-prevent-the-reloading-of-the-whole-page-when-i-let-the-user-to-perform-an-action/10800/9
https://blog.streamlit.io/introducing-submit-button-and-forms/


"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Title of the app
st.title("Media Player: Video and Audio")

#File uploader for audio (.mp3) and video (.mp4, .m4v) files
uploaded_file = st.file_uploader("Envoyer un fichier audio (.mp3, .wav, .m4a) ou vidéo (.mp4, .m4v, .mkv)", type=["mp3", ".wav", ".m4a", "mp4", "m4v", "mkv"])

if uploaded_file is not None:
    # Check the file type and display the appropriate player
    file_type = uploaded_file.type
    
    if file_type == "audio/mpeg":
        # Display the audio player for MP3 files
        st.audio(uploaded_file, format="audio/mp3")
        
    elif file_type == "audio/wav":
        # Display the audio player for WAV files
        st.audio(uploaded_file, format="audio/wav")
        
    elif file_type == "audio/x-m4a" or file_type == "audio/m4a":
        # Display the audio player for M4A files
        st.audio(uploaded_file, format="audio/m4a")
        
    elif file_type == "video/mp4":
        # Display the video player for MP4 files
        st.video(uploaded_file)
        
    elif file_type == "video/x-m4v":
        # Display the video player for M4V files
        st.video(uploaded_file)
        
    elif file_type == "video/x-matroska":
        # Display the video player for MKV files
        st.video(uploaded_file)




# Display video player if a video file is uploaded
# if all_file is not None:
#     st.video(all_file)

# Display audio player if an audio file is uploaded
# if audio_file is not None:
#     st.audio(audio_file)






