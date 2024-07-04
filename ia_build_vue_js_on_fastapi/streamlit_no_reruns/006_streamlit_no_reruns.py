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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_build_vue_js_on_fastapi/streamlit_no_reruns/

# launch the file
streamlit run 006_streamlit_no_reruns.py

https://www.youtube.com/watch?v=dPdB7zyGttg

https://discuss.streamlit.io/t/how-to-prevent-the-reloading-of-the-whole-page-when-i-let-the-user-to-perform-an-action/10800/9
https://blog.streamlit.io/introducing-submit-button-and-forms/


"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime


def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)


# Function to convert milliseconds to SRT time format
def convert_to_srt_time(milliseconds):
    hours = milliseconds // (60 * 60 * 1000)
    milliseconds %= (60 * 60 * 1000)
    minutes = milliseconds // (60 * 1000)
    milliseconds %= (60 * 1000)
    seconds = milliseconds // 1000
    milliseconds %= 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

# Function to convert seconds to VTT time format
def convert_to_vtt_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


# Function to generate .SRT content from transcript
def generate_srt(transcript):
    srt_content = ""
    segment_index = 1
    if transcript is not None:
        segments = transcript.get("segments", [])
        for segment in segments:
            start_time = int(segment["start"] * 1000)
            end_time = int(segment["end"] * 1000)
            srt_content += f"{segment_index}\n"
            srt_content += f"{convert_to_srt_time(start_time)} --> {convert_to_srt_time(end_time)}\n"
            for word in segment["words"]:
                srt_content += f"{word['word']} "
            srt_content += "\n\n"
            segment_index += 1
    return srt_content

# Function to generate .VTT content from transcript
def generate_vtt(transcript):
    vtt_content = "WEBVTT\n\n"
    segment_index = 1
    if transcript is not None:
        segments = transcript.get("segments", [])
        for segment in segments:
            start_time = convert_to_vtt_time(segment["start"])
            end_time = convert_to_vtt_time(segment["end"])
            vtt_content += f"{segment_index}\n"
            vtt_content += f"{start_time} --> {end_time}\n"
            for word in segment["words"]:
                vtt_content += f"{word['word']} "
            vtt_content += "\n\n"
            segment_index += 1
    return vtt_content

# Function to generate .TXT content from transcript
def generate_txt(transcript):
    txt_content = ""
    if transcript is not None:
        segments = transcript.get("segments", [])
        for segment in segments:
            for word in segment.get("words", []):
                txt_content += f"{word['word']} "
            txt_content += "\n"
    return txt_content.strip()

st.title("JSON File Loader")

uploaded_file = st.file_uploader("Choose a JSON file", type="json")

if uploaded_file is not None:
    # Load the JSON file into the transcript variable
    transcript = json.load(uploaded_file)
    
    # Display the loaded JSON data
    # st.write(transcript)
    st.success("JSON file loaded successfully!")


    if transcript is not None:
            srt_content = generate_srt(transcript)
            vtt_content = generate_vtt(transcript)
            txt_content = generate_txt(transcript)
            
            # add check box to avoid global post
            opt = st.radio('Download File type', ['.SRT', '.VTT', '.TXT'])

            # Display the appropriate plot
            if opt == '.SRT':

                st.download_button(
                    label="Download .SRT Transcription",
                    data=srt_content.encode(),
                    file_name="transcript.srt",
                    mime="text/srt",
                    type="secondary"
                )
                
            elif opt == '.VTT':

                st.download_button(
                    label="Download .VTT Transcription",
                    data=vtt_content.encode(),
                    file_name="transcript.vtt",
                    mime="text/vtt",
                    type="secondary"
                )

            elif opt == '.TXT':
                
                st.download_button(
                    label="Download .TXT Transcription",
                    data=txt_content.encode(),
                    file_name="transcript.txt",
                    mime="text/plain",
                    type="secondary"
                )
                

# You can also display the transcript variable for debugging purposes
# if 'transcript' in locals():
#     st.write("Transcript variable contents:", transcript)


# Add download buttons for .SRT, .VTT, and .TXT files
        






