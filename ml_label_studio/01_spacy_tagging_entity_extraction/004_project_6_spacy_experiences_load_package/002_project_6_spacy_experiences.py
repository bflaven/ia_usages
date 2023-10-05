#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
# NO CONDA ENV

conda create --name tagging_entity_extraction python=3.9.13
conda info --envs
source activate tagging_entity_extraction

conda deactivate
# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]




# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > tagging_entity_extraction.txt



# to install
pip install -r tagging_entity_extraction.txt

[path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/tagging_entity_extraction/project_6_spacy_experiences/

[file]
python 002_project_6_spacy_experiences.py


Source: https://medium.com/mlearning-ai/automatic-skill-extraction-from-resumes-using-spacy-710507624a1e

"""

# Source: let’s consider three fake resumes:
resume1 = """John Doe 123 Main St Anytown, USA johndoe@email.com Objective: Seeking a challenging position as a software engineer in a reputable organization. Education: B.S. in Computer Science, Anytown University, 2020 Skills: - Python - JavaScript - React - SQL - Git """

resume2 = """Jane Smith 456 Elm St Anytown, USA janesmith@email.com Objective: Looking for a role as a data analyst to utilize my analytical and technical skills. Education: M.S. in Data Science, Anytown University, 2021 Skills: - Python - R - SQL - Tableau - Machine Learning"""

resume3 = """Bob Johnson 789 Oak St Anytown, USA bobjohnson@email.com Objective: Aspiring web developer with experience in HTML, CSS, and JavaScript. Education: A.A.S. in Web Development, Anytown Community College, 2019
Skills: - HTML - CSS - JavaScript - PHP - WordPress """

# PART_1

# Step_1: Import necessary libraries and load the language model
import spacy 
from spacy.language import Language 
from spacy.matcher import PhraseMatcher 
from spacy.tokens import Span

# Step_2: Create a list of relevant skills
skills_list = [ "Python", "JavaScript", "React", "SQL", "Git", "R", "Tableau", "Machine Learning", "HTML", "CSS", "PHP", "WordPress" ]

# Step_3: Create a PhraseMatcher and add the skills to it
nlp = spacy.load("en_core_web_sm")
skill_patterns = list(nlp.pipe(skills_list)) 
matcher = PhraseMatcher(nlp.vocab, attr="LOWER") 
matcher.add("SKILL", skill_patterns)

# Step_4: Define the custom component for skill extraction
@Language.component("skill_component") 
def skill_component(doc): 
    matches = matcher(doc) 
    spans = [Span(doc, start, end, label="SKILL") for match_id, start, end in matches] 
    doc.ents = spans         
    return doc


# Step_5: Add the custom component to the pipeline
nlp.add_pipe("skill_component", after="ner") 
print(nlp.pipe_names)

# Step_6: Process the resumes and extract skills
resume_texts = [resume1, resume2, resume3] 
for idx, text in enumerate(resume_texts): 
    doc = nlp(text) 
    unique_skills = set() 
    print(f"\n--- Skills in Resume {idx + 1}:")
    for ent in doc.ents: 
        if ent.label_ == "SKILL": unique_skills.add(ent.text) 
        for skill in unique_skills:
            # Output the skills found in resume
            # print(skill) 
            print()

# PART_2
# Step_1 Create a list of skills relevant to data analysis:

data_analysis_skills = [ "Python", "R", "SQL", "Excel", "Tableau", "Power BI", "Data Cleaning", "Data Visualization", "Machine Learning", "Statistics", "Big Data", "Hadoop", "Spark" ]

# Step_2 Next, use the existing custom component for skill extraction and process the resumes to find the data analysis skills present in each resume.

resume_skills = [] 
for idx, text in enumerate(resume_texts): 
    doc = nlp(text) 
    skills = [ent.text for ent in doc.ents 
              if ent.label_ == "SKILL"] 
    resume_skills.append(skills) 
    print(resume_skills)

# Step_3: calculate the ratio of data analysis skills for each resume.

data_analysis_skill_counts = []

for skills in resume_skills:
    unique_skills = set(
        skill for skill in skills if skill in data_analysis_skills)
    count = len(unique_skills)
    ratio = count / len(data_analysis_skills)
    data_analysis_skill_counts.append(ratio)

print(data_analysis_skill_counts)

# Step_4: Finally, find the resume with the highest ratio of data analysis skills.

highest_ratio_index = data_analysis_skill_counts.index(
    max(data_analysis_skill_counts))

# Result of the analysis
print(
    f"Resume {highest_ratio_index + 1} is the most suitable for a data analysis role.")
