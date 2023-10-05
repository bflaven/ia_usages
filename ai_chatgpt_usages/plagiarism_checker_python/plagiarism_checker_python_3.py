"""


[env]
# Conda Environment
# NO CONDA ENV
conda create --name plagiarism_checker_python python=3.10.9
conda info --envs
source activate plagiarism_checker_python
conda deactivate
# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]


# update conda 
conda update -n base -c defaults conda


[path]
cd /Users/brunoflaven/Documents/03_git/BlogArticlesExamples/ai_chatgpt_usages/plagiarism_checker_python


[file]
streamlit run plagiarism_checker_python_3.py


# other module
pip install pandas streamlit numpy requests watchdog
pip install plotly
pip install altair
pip install matplotlib

[source]
Inspired by https://github.com/Kalebu/Plagiarism-checker-Python

"""


from pathlib import Path
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import streamlit.components.v1 as stc
import numpy as np
import pandas as pd
import time
import csv
import re
import plotly.figure_factory as ff
import altair as alt
import matplotlib.pyplot as plt
import math

st.markdown(
    """
    <style>
        .stProgress > div > div > div > div {
            background-color: red;
        }
    </style>""",
    unsafe_allow_html=True,
)


# values
# path = "./source_papers"
path = "./source_codes"

dir_list = os.listdir(path)

student_files = [doc for doc in dir_list if doc.endswith('.txt')]
student_notes = [open(_file, encoding='utf-8').read() for _file in Path(path).glob('*.txt')]

def vectorize(Text): return TfidfVectorizer().fit_transform(Text).toarray()
def similarity(doc1, doc2): return cosine_similarity([doc1, doc2])


vectors = vectorize(student_notes)
s_vectors = list(zip(student_files, vectors))
plagiarism_results = set()


def check_plagiarism():
    global s_vectors
    for student_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((student_a, text_vector_a))
        del new_vectors[current_index]
        for student_b, text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            student_pair = sorted((student_a, student_b))
            score = (student_pair[0], student_pair[1], sim_score)
            plagiarism_results.add(score)
    return plagiarism_results


def percent(num1, num2):
    num1 = float(num1)
    num2 = float(num2)
    percentage = '{0:.2f}'.format((num1 / num2 * 100))
    return percentage


def conclusion(progress_value):
    if progress_value <= 0.2:
            conclusion = "Acceptable"
            col2.metric("Conclusion", conclusion)
    elif 0.2 < progress_value <= 0.7:
            conclusion = "Caution"
            col2.metric("Conclusion", conclusion)
    elif progress_value > 0.7:
            conclusion = "Plagiarist"
            col2.metric("Conclusion", conclusion)
       
        
# Put the result in a dictionary and then send it to panda
result = {}
result = check_plagiarism()
# print(result)

# Column names to be added
column_names = ["Student_a", "Student_b", 'Score']

df = pd.DataFrame(result, columns=column_names)
df.to_csv('output_checker_data_7.csv',
                            index=False)

# https://docs.streamlit.io/library/api-reference/data

show = st.checkbox('Show result')

if show:
    st.write('Here is the df...')
    df_show = pd.read_csv('output_checker_data_7.csv', header=None)
    st.write(df_show)

    # with Streamlit parse a specific column from a dataframe and show each comparison index from this column, ranged between zero to one in a progress bar that from grey color to red color

    # You can use Streamlit to display a progress bar that ranges from grey to red color based on a specific column value from a dataframe. Here is an example code snippet that demonstrates how to achieve this:


    # Load sample data
    # df = pd.read_csv("sample_data.csv")

    # Select the column to compare
    # selected_column = st.selectbox("Select a column", df.columns)

    # Create a progress bar for each row in the column
    for index, row in df.iterrows():
        
        label_student_a = f''+row["Student_a"]+''
        label_student_b = f''+row["Student_b"]+''
        
        # st.write(label_student_a)
        # st.write(label_student_b)
        
        
        progress_value = row["Score"]
        
        st.markdown("### Case_"+str(index)+" `"+label_student_a +
                    "` vs `"+label_student_b+"`  ")
        
        
        col1, col2 = st.columns(2)
        col1.metric("Percentage",
                    ""+percent(progress_value, 1)+"%")
        
        # add a function to generate the second indicator
        conclusion(progress_value)
            
        
        
        # NOT SIGNIFICANT
        # st.markdown("_Visual rendering for Plagiarism for Case_" + str(index)+"_")
        # st.progress(int(progress_value), text="Plagiarism Checker Result between "+label_student_a+" and "+label_student_b+" ")

        # st.progress((int(progress_value)))


# In the above code, we first load a sample data file and display a dropdown to select the column to compare. Then, we iterate through each row in the selected column and create a progress bar using the st.progress function. The value of the progress bar is set to the value of the selected column for that row. This will display a progress bar for each row in the selected column, ranging from grey to red color based on the value of the column.

# Note that the values in the selected column should be in the range of zero to one for this to work properly. If the values are not in this range, you can normalize them using a function like sklearn.preprocessing.MinMaxScaler before displaying them in the progress bar.




    