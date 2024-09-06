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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_using_mlflow/controlling-large-language-model-output-with-pydantic/

# launch the file
python 016_crewai_ok.py


# source
https://github.com/fabiodemo/crewai-test/blob/main/main-crewai.py
https://github.com/search?q=from+crewai+import+Agent%2C+Task%2C+Crew+ollama+language%3APython&type=code&l=Python


"""
import requests
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama

try:
    ollama_model = Ollama(model="mistral:latest")


    # Define your agents with roles and goals
    researcher = Agent(
    role="Product Owner",
    goal="Provide the requirements of a product",
    backstory="""You work at a leading tech company.
    Your expertise lies in create the detail requirements for an application or product.""",
    verbose=True,
    allow_delegation=False,
    tools=[],
    llm=ollama_model,
    )
    writer = Agent(
    role="SAP CAP developer",
    goal="Use the output from Product Owner to write codes to implement the product requirements by using SAP CAP program",
    backstory="""You are an expert of SAP CAP appliction. You can write down the code to complete the project requirements""",
    verbose=True,
    tools=[],
    allow_delegation=False,
    llm=ollama_model,
    )

    # Create tasks for your agents
    task1 = Task(
    description="""Create the requirements for the product: Book Management""",
    expected_output="Detailed requirements with user stories",
    agent=researcher,
    )

    task2 = Task(
    description="""Depends on the requirements, write down the code to complete the requirements.""",
    expected_output="SAP CAP application code delivered.",
    agent=writer,
    )

    # Instantiate your crew with a sequential process
    crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    llm=ollama_model,
    verbose=2,  # You can set it to 1 or 2 to different logging levels
    )

    # Get your crew to work!
    result = crew.kickoff()

    print("######################")
    print(result)

except Exception as e:
    print("Error:", e)


















