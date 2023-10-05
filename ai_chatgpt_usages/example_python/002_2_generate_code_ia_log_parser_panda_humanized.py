#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
002_1_generate_code_ia_log_parser_panda.py
source Python for GPT query  
QUERY :: Can you write a log parser in Python to detect specific part of data contained in .log file, extract this sample of data, retrieve it and load it with the Panda library inside a dataframe (df) then export this sample as .csv file then write a small application with the Streamlit framework to manipulate this new .csv file


CAUTION :: below the first part, the log parser + loading in a panda dataframe

"""

"""


[env]
# Conda Environment
conda create --name unstructured_data_python_parsing python=3.9.7
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
python generate_code_ia_log_parser_panda_humanized.py



# other module
pip install requests
pip install pandas
pip install streamlit
pip install numpy

[source]
https://github.com/bflaven/BlogArticlesExamples/tree/master/unstructured_data_python_parsing


"""
import pandas as pd
import re

def parse_log_file(file_path, pattern):
    data = []
    with open(file_path, "r") as f:
        for line in f:
            if re.search(pattern, line):
                data.append(line)
    return data

def extract_data(log_data):
    extracted_data = []
    for line in log_data:
        line_data = line.strip().split(" ")
        extracted_data.append(line_data)
    return extracted_data

def create_dataframe(data):
    # df = pd.DataFrame(data, columns=["Timestamp", "Level", "Message"])
    df = pd.DataFrame(data)

    return df

def export_to_csv(df, file_path):
    df.to_csv(file_path, index=False)

if __name__ == "__main__":
    
    
    # log_file = "sample.log"
    # pattern = "ERROR"
    
    log_file = "fake_sample_log_3.log"
    pattern = "DEBUG"


    log_data = parse_log_file(log_file, pattern)
    extracted_data = extract_data(log_data)
    df = create_dataframe(extracted_data)
    csv_file = "generate_code_ia_log_parser_panda_humanized_sample_error_data.csv"
    export_to_csv(df, csv_file)



    
