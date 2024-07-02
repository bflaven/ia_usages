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
streamlit run 011_video_streamlit.py


[source]
https://doc-video-subtitle-inputs.streamlit.app/
"""

import streamlit as st
import json
import pandas as pd

# add specific
from pathlib import Path
import io

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
                # REMOVE SPACE
                # srt_content += f"{word['word']} "
                srt_content += f"{word['word']}"

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
                # REMOVE SPACE
                # vtt_content += f"{word['word']} "
                vtt_content += f"{word['word']}"
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

# Function to display the player and transcript
def display_player_and_transcript(transcript, current_time):
    if transcript is not None:
        segments = transcript.get("segments", [])
        
        # Convert segments to a flat list of dictionaries for CSV conversion
        flattened_segments = []
        for segment in segments:
            for word in segment.get("words", []):
                flattened_segments.append({
                    "start": word["start"],
                    "end": word["end"],
                    "word": word["word"]
                })
        
        # Write segments to CSV
        csv_data = pd.DataFrame(flattened_segments)
        csv_string = csv_data.to_csv(index=False)
        
        # Display the CSV data
        st.subheader("Transcript as CSV:")
        st.dataframe(csv_data)

        # Allow users to download the CSV file
        st.download_button(
            label="Download Transcript CSV",
            data=csv_string.encode(),
            file_name="transcript.csv",
            mime="text/csv"
        )


# Load the JSON transcript
transcript_path = "data/vroux_black_history_month_light_FR.json"
with open(transcript_path, "r", encoding="utf-8") as f:
    transcript = json.load(f)

# Display the video
# video_path = "data/208314_small.mp4"
# st.video(video_path)


# Display the transcript in various formats
st.subheader("Transcript Formats")
st.text_area("SRT Format", generate_srt(transcript), height=300)
st.text_area("VTT Format", generate_vtt(transcript), height=300)
st.text_area("TXT Format", generate_txt(transcript), height=300)

# Display player and transcript as CSV
current_time = 0  # This can be set dynamically based on video playback time
display_player_and_transcript(transcript, current_time)




                    


