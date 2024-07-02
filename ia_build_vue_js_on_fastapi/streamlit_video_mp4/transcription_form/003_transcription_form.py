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
cd /Users/brunoflaven/Documents/01_work/blog_articles/build_vue_js_on_fastapi/streamlit_video_mp4/transcription_form/


# launch the file
streamlit run 002_transcription_form.py


"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Function to convert dataframe to JSON

@st.cache_data
def df_to_json(df):
    return df.to_json(orient='records', date_format='iso')

# Function to convert dataframe to TXT
@st.cache_data
def df_to_txt(df):
    return df.to_string(index=False)

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


# Main Streamlit app
def main():
    st.title("CSV to DataFrame Converter")

    # File uploader in the main form
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)

        # Display the dataframe
        st.write("### Resulting DataFrame")
        st.dataframe(df)

        # Convert dataframe to JSON
        json_data = df_to_json(df)
        
        # Convert dataframe to TXT
        txt_data = df_to_txt(df)
        
        # Timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


        # Form to download JSON
        with st.form('form_1'):
            st.write("form_1")
            submitted1 = st.form_submit_button('Submit 1')
            
            
        # Form to download TXT
        with st.form("form_2"):
            st.write("form_2")
            csv = convert_df(df)

            submitted2 = st.form_submit_button('Submit 2')

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name="large_df.csv",
                mime="text/csv",
            )

            

if __name__ == "__main__":
    main()


