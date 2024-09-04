#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name using_mlflow python=3.9.13
conda info --envs
source activate using_mlflow
conda deactivate


# BURN AFTER READING
source activate using_mlflow

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n using_mlflow
conda env remove -n locust_poc



# BURN AFTER READING
conda env remove -n using_mlflow


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
pip install mlflow
python -m pip install mlflow
python -m pip install python-dotenv
python -m pip install openai
python -m pip install langchain-community langchain-core
python -m pip install crewai 
python -m pip install crewai-tools 



# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_using_mlflow/controlling-large-language-model-output-with-pydantic/

# launch the file
python 014_crewai.py


# source
https://github.com/search?q=from+crewai+import+Agent%2C+Task%2C+Crew+ollama+language%3APython&type=code&l=Python



"""
from crewai import Agent, Task, Crew
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser


# import os
# os.environ["OPENAI_API_KEY"] = "NA"

# llm = ChatOllama(
#     model="mistral:latest",
#     base_url = "http://localhost:11434")

llm = ChatOllama(model="mistral:latest")


general_agent = Agent(role = "Math Professor",
                      goal = """Provide the solution to the students that are asking mathematical questions and give them the answer.""",
                      backstory = """You are an excellent math professor that likes to solve math questions in a way that everyone can understand your solution""",
                      allow_delegation = False,
                      verbose = True,
                      llm = llm)

task = Task(description="""what is 3 + 5""",
             agent = general_agent,
             expected_output="A numerical answer.")

crew = Crew(
            agents=[general_agent],
            tasks=[task],
            verbose=True
        )

result = crew.kickoff()

print("######################")
print(result)



















