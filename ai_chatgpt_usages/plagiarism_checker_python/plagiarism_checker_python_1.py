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
python plagiarism_checker_python_1.py


# other module
pip install pandas streamlit numpy requests watchdog




[source]
Inspired by https://github.com/Kalebu/Plagiarism-checker-Python

"""


from pathlib import Path
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

path = "./source_papers"
dir_list = os.listdir(path)

# print("Files and directories in '", path, "' :")

# print the list
# print(dir_list)

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


for data in check_plagiarism():
    print(data)
