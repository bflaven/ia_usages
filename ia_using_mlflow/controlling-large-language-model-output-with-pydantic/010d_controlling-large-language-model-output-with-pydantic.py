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

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_using_mlflow/controlling-large-language-model-output-with-pydantic/

# launch the file
python 010d_controlling-large-language-model-output-with-pydantic.py


# source
https://github.com/debianmaster/opensource-llm-experiments


"""

from langchain_community.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field, ValidationError
from typing import List
from typing import Optional


from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
from langchain_core.output_parsers import JsonOutputParser


model = Ollama(
    model="mistral:latest", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)

# model = OpenAI(model_name="text-davinci-003", temperature=0.0)


content = """
Champs-Elysees and Concorde to host Paralympics opening ceremony
Paris has chosen the Champs-Elysees and Place de la Concorde to host the opening ceremony of the 2024 Summer Paralympics on Wednesday. The event will welcome a grand parade with over 180 delegations and 4,400 para-athletes, marking a celebration in two of the city's most renowned landmarks.


Paris has chosen the iconic Champs-Elysees avenue and the historic Place de la Concorde to host the opening ceremony for the Summer Paralympics on Wednesday.

The prestigious avenue sweeping through the 8th arrondissement to the west of central Paris is dotted with cafes, palaces and luxury shops and connects the Arc de Triomphe in the west with Place de la Concorde in the east in a single straight line.


Tens of thousands of people daily throng the two-kilometre-(one mile)-long tree-lined artery with its wide sidewalks.

It has long been for French a place of celebrations and popular gatherings.

It was there in 1960 that American actress Jean Seberg appeared in Jean-Luc Godard's legendary new wave film "Breathless" selling copies of the New York Herald Tribune.

On Wednesday it will be the scene of a popular parade, open to everyone and involving up to more than 180 delegations and 4,400 para-olympians from around the world.

France has celebrated two football World Cup victories there, the traditional military parade on July 14, the Bastille Day national holiday, and the Tour de France cycle race ends there.

Hundreds of thousands of Parisians and tourists gather there to celebrate New Year's Eve.

Once fields and fallow land, the avenue started to take shape when Louis XIV's city planner first linked the Louvre to the Tuileries Garden in the mid-17th century.

At one end of the avenue is the Arc de Triomphe, commissioned by French Emperor Napoleon which now honours France's war dead, and was inaugurated in 1836.

France's WWII leader General Charles de Gaulle, chose it, of course, for his triumphant return from exile on August 26, 1944, after the Liberation of Paris from the Nazis.

However the prestigious thoroughfare has known scenes of unrest. Police used tear gas, rubber bullets and water cannon when "yellow vest" anti-government protesters in 2018 attacked the Arc de Triomphe, and ransacked shops.


However, with stores and historic cinemas closing along the avenue due to rising rents and falling sales, locals have gradually abandoned the Champs-Elysees over concerns that it is too noisy, dirty and expensive.

With Paris' other famous symbol the Eiffel Tower looming just across the River Seine, the name is the French for Elysian Fields, the paradise for dead heroes in Greek mythology.

At the other end, the Place de la Concorde, the largest square in Paris, will be the scene of the official parade for ticket holders, in addition to the protocol and artistic sequences.

The square has a bloody past: then known as "Place de la Revolution" it was a place of execution and heads rolled (literally) there during the French Revolution.

King Louis XVI and his wife Marie-Antoinette were famously guillotined there in 1793 during the Reign of Terror that followed the 1789 Revolution.

It was renamed Concorde after the July Revolution of 1830.

Today the elegant paved square by the Seine is defined by its huge obelisk, one of a pair originally erected by Ramses II outside the temple in Luxor in Egypt in the 13th century BC. It was gifted to Paris in 1830.
"""

lang ="English"


# Print the values
print(content)
print(lang)



# Define your desired data structure.
# Define the PostResponse model using Pydantic for structured output
class PostResponse(BaseModel):
    title: str = Field(description="This is the title of the post")
    summary: str = Field(description="This is the summary of the post")
    keywords: List[str] = Field(description="This is the 5 keywords of the post")
    categorie: str = Field(description="This is the categorie of the post")

# Define the Posts model, which contains a list of PostResponse objects
class Posts(BaseModel):
    post: List[PostResponse]


parser = JsonOutputParser(pydantic_object=PostResponse)


prompt = PromptTemplate(
    template="""
system:
Tu es un expert SEO qui ne répond que en {lang}.
Etant donné le texte saisi par l'utilisateur, génère les éléments suivants:

1: Un titre concis, engageant et riche en mots clés qui représente fidèlement le contenu. Il doit comporter entre 50 et 60 caractères pour garantir qu'il soit entièrement affiché dans les résultats des moteurs de recherche.
2: Un bref résumé de 2 à 3 phrases des principaux points ou points à retenir du texte. Cela devrait également inclure un ou deux des principaux mots-clés. Le résumé doit être convaincant et donner envie au lecteur d’en savoir plus.
3: Les cinq mots-clés les plus importants et les plus pertinents extraits du texte. Il doit s'agir exlusivement de cinq mots-clés que les lecteurs potentiels pourraient utiliser pour rechercher ce type de contenu.
4: La catégorie ou le sujet principal auquel appartient le texte. Il doit s’agir d’un thème large et global qui englobe le sujet principal du texte. Cette catégorie doit être dans la langue du texte {lang} et doit appartenir aux vocabulaires IPTC NewsCodes Concept.

question:
{content}

format_instructions:
{format_instructions}

""",
    input_variables=["content", "lang"],
    partial_variables={"format_instructions": parser.get_format_instructions()},

)

# And a query intended to prompt a language model to populate the data structure.
chain = prompt | model | parser
print("-------------------------------------- output\n")
output = chain.invoke({"content": content, "lang": lang})
print("\n")



# template = """You are a gift recommender. Given a person's age,\n
#  it is your job to suggest an appropriate gift for them. If age is under 10,\n
#  the gift should cost no more than {budget} otherwise it should cost atleast 10 times {budget}.

# Person Age:
# {output}
# Suggest gift:"""
# prompt_template = PromptTemplate(input_variables=["output", "budget"], template=template)
# chain_two = LLMChain(llm=llm, prompt=prompt_template)






