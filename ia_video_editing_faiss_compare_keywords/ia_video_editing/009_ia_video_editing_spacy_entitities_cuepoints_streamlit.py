#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_using_faiss python=3.9.13
conda info --envs
source activate ia_using_faiss
conda deactivate


# BURN AFTER READING
source activate ia_using_faiss

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_using_faiss

# BURN AFTER READING
conda env remove -n ia_using_faiss
conda env remove -n ia_seo_llm


# other libraries
python -m pip install spacy 

# spacy
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
python -m spacy validate

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_video_editing_faiss_compare_keywords/ia_video_editing/


# launch the file
streamlit run 008_ia_video_editing_spacy_entitities_cuepoints_streamlit.py

"""
import streamlit as st

data = "source/putin_issues_EN_20241122_013120_013320_CS_8000_small.mp4"

st.write("Click to go to that moment in video.")

time_stamps = [
    (st.button("Part A", "a"), 60),  # bool, moment (seconds)
    (st.button("Part B", "b"), 90),
    (st.button("Part C", "c"), 110),
]

placeholder = st.empty()

time_chosen = [v for k, v in time_stamps if k == True]  # return [int] associated with a clicked button
if time_chosen:
    placeholder.empty()
    placeholder.video(data, start_time=time_chosen[0])







