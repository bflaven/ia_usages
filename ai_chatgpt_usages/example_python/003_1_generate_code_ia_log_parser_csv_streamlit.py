#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
003_1_generate_code_ia_log_parser_csv_streamlit.py
source Python for GPT query  
QUERY :: Can you write a log parser in Python to detect specific part of data contained in .log file, extract this sample of data, retrieve it and load it with the Panda library inside a dataframe (df) then export this sample as .csv file then write a small application with the Streamlit framework to manipulate this new .csv file


CAUTION :: below the second part, the streamlit app
"""
"""
[env]
# Conda Environment
# NO CONDA ENV

conda create --name unstructured_data_python_parsing python=3.9.13
conda info --envs
source activate unstructured_data_python_parsing
conda deactivate
# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]


# update conda 
conda update -n base -c defaults conda


[path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/ai_chatgpt_usages/example_python



[file]
streamlit run 003_1_generate_code_ia_log_parser_csv_streamlit.py

# other module
pip install requests
pip install pandas
pip install streamlit
pip install numpy
pip install watchdog

[source]
https://github.com/bflaven/BlogArticlesExamples/tree/master/unstructured_data_python_parsing


"""
import pandas as pd
import streamlit as st

@st.cache
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def main():
    st.title("Log Parser")
    file_path = st.text_input("Enter the path to the .csv file:")
    if file_path:
        df = load_data(file_path)
        st.write("Data Preview:")
        st.write(df.head())
        if st.checkbox("Show Columns"):
            st.write(df.columns)
        if st.checkbox("Show Shape"):
            st.write("Number of rows:", df.shape[0])
            st.write("Number of columns:", df.shape[1])

if __name__ == "__main__":
    main()