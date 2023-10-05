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
python plagiarism_checker_python_2.py
streamlit run plagiarism_checker_python_2.py


# other module
pip install pandas streamlit numpy requests watchdog

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


path = "./source_papers"
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


# for data in check_plagiarism():
#     print(data)

# print(check_plagiarism())

# dictionary
result = {}
result = check_plagiarism()
print(result)

# Column names to be added
column_names = ["Student_a", "Student_b", 'Score']

df = pd.DataFrame(result, columns=column_names)
df.to_csv('output_checker_data_7.csv',
                            index=False)

# for check_result in check_plagiarism():
#     # print(check_result)
#     df = pd.DataFrame.from_dict(check_result)
#     print(df)
#     df.to_csv('output_checker_data_3.csv', index=False)


# with open('output_checker_data_1.csv', 'w') as f:
#     w = csv.DictWriter(f, data.keys())
#     w.writeheader()
#     w.writerow(data)

# source model https://pythonguides.com/python-dictionary-to-csv/
# MODEL
# employee_info = ['emp_id', 'emp_name', 'skills']

# new_dict = [
#     {'emp_id': 456, 'emp_name': 'George', 'skills': 'Python'},
#     {'emp_id': 892, 'emp_name': 'Adam', 'skills': 'Java'},
#     {'emp_id': 178, 'emp_name': 'Gilchrist', 'skills': 'Mongo db'},
#     {'emp_id': 155, 'emp_name': 'Elon', 'skills': 'Sql'},
#     {'emp_id': 299, 'emp_name': 'Mask', 'skills': 'Ruby'},
# ]

# with open('test4.csv', 'w') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=employee_info)
#     writer.writeheader()
#     writer.writerows(new_dict)

# my_dictionary = {'values': 678, 'values2': 167, 'values6': 998}

# with open('test6.csv', 'w') as f:
#     for key in my_dictionary.keys():
#         f.write("%s, %s\n" % (key, my_dictionary[key]))
        

# with open('output_checker_data_2.csv', 'w') as f:
#     for key in check_plagiarism().keys():
#         f.write("%s, %s\n" % (key, check_plagiarism()[key]))


print('\n --- DONE')

 
# https://docs.streamlit.io/library/api-reference/data

# {('bruno.txt', 'juma.txt', 0.1652086147306484), ('bruno.txt', 'fatma.txt', 0.9593414202444362), ('john.txt', 'juma.txt', 0.5410614647865478), ('fatma.txt', 'juma.txt', 0.1784308055205517), ('bruno.txt', 'john.txt', 0.13446069777825573), ('fatma.txt', 'john.txt', 0.145222031275702)}
