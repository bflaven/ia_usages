#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name ner_spacy_fastapi_database python=3.9.13
conda info --envs
source activate ner_spacy_fastapi_database
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ner_spacy_fastapi_database

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/fastapi_database/011_openai_sqlite_nlp_fastapi_streamlit

# Launch the streamlit app
streamlit run app_streamlit.py

# check
http://localhost:8501/

- requirement for streamlit
pip install streamlit

"""
import streamlit as st
import json
import requests

st.title("NLP sqlite App")


# st.markdown('**Example**')
# st.json({
#   "post_title": "Sample Post",
#   "post_body": "This is a sample post body with named entities like Apple and Microsoft.",
#   "post_origin_id": 12313213,
#   "api_result": ""
# })

# operation (endpoint)
operation = st.selectbox(
    'What operation do you want to perform?',
    ('summary', 'keywords', 'entities'))

# st.success(operation)

# 
st.write("Select a language below 👇")
lang = st.selectbox('Choose your language',
                     ('en', 'fr','es', 'ru'))

# st.success(lang)

st.write("Please fill out the fields below 👇")
# post_title
post_title = st.text_input('Post title', 'Sample Post', help="You can define your Post Title")
st.write('The current Post title is', post_title)


post_body = st.text_area("Text to analyze", "This is a sample post body with named entities like Apple and Microsoft.", help="You can define your Post Body")

# st.success(f'You wrote {len(txt)} characters.')


# post_title
post_origin_id = st.text_input(
    'Post Origin id', '12313213', help="You can define your Post ID. Caution: Please only use numbers, the field in the database is an integer. This could be an ID from another CMS to allow a possible connection")

# st.success('The current Post Origin id is', post_origin_id)

# Add empty keywords_ner


# converting the inputs into a json format
inputs = {"post_title": post_title,   "post_body": post_body,
          "post_origin_id": post_origin_id, "api_result": ""}

# st.json(inputs)

# when the user clicks on button it will fetch the API
if st.button('Send'):
    res = requests.post(url="http://127.0.0.1:8000/"+
                        operation+"/"+lang, data=json.dumps(inputs))


    data = json.loads(res.text)
    # st.code(data)
    # st.write(data['api_result'])
    
    # st.code(inputs)
    st.write(f"Response from API 🚀  =  {data['api_result']}")


