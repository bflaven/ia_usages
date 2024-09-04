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
python -m pip uninstall crewai 
python -m pip install crewai==0.10.0
python -m pip install crewai-tools 



# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_using_mlflow/controlling-large-language-model-output-with-pydantic/

# launch the file
python 015_crewai_ok.py


# source
https://github.com/search?q=from+crewai+import+Agent%2C+Task%2C+Crew+ollama+language%3APython&type=code&l=Python

"""
import requests
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama

try:
    # response = requests.post('http://ollama:11434/api/generate',
    #                          json={"model": "mistral:latest",
    #                                "prompt": "Test connection"})
    # print("Connection successful:", response.json())

    # os.environ["OPENAI_API_KEY"] = "Your Key"
    #export OPENAI_API_KEY=sk-blablabla # on Linux/Mac
    ollama_model = Ollama(model="mistral:latest")

    # Define seus agentes com funções e metas
    researcher = Agent(
        role='Researcher',
        goal='Discover new insights',
        backstory="""You're a world class
            researcher working on a major data science company""",
        verbose=True,
        allow_delegation=False,
        llm=ollama_model,
    )

    writer = Agent(
        role='Writer',
        goal='Create engaging content',
        backstory="""You're a famous technical writer,
            specialized on writing data related content""",
        verbose=True,
        allow_delegation=False,
        llm=ollama_model,
    )

    # Crie tarefas para seus agentes
    task1 = Task(description='Investigate the latest AI trends',
                 agent=researcher)
    task2 = Task(description='Write a blog post on AI advancements',
                 agent=writer)

    # Instancie sua equipe com um processo sequencial - DOIS AGENTES
    crew = Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        llm=ollama_model,
        verbose=2,
        process=Process.sequential
    )

    # Coloque sua equipe para trabalhar
    result = crew.kickoff()

except Exception as e:
    # print("Connection failed:", e)
    print("Error:", e)


















