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
cd /Users/brunoflaven/Documents/01_work/blog_articles/_using_mlflow/controlling-large-language-model-output-with-pydantic/

# launch the file
python 010a_controlling-large-language-model-output-with-pydantic.py


# source
https://github.com/debianmaster/opensource-llm-experiments


"""

from langchain_community.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List
from typing import Optional


from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama

model = Ollama(
    model="mistral:latest", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)

# model = OpenAI(model_name="text-davinci-003", temperature=0.0)


content = """
En Tunisie, le président Kaïs Saïed procède à un vaste remaniement ministériel
Après avoir changé de Premier ministre au début du mois d'août, le président tunisien Kaïs Saïed a remplacé dimanche 19 ministres dont ceux des Affaires étrangères et de la Défense, ainsi que trois secrétaires d'État.

Le président de Tunisie Kaïs Saïed a procédé dimanche 25 août à un vaste remaniement ministériel sans donner d'explications, à un peu plus d'un mois de l'élection présidentielle. 

Ce remaniement inattendu comprend le remplacement de 19 ministres, dont ceux des Affaires étrangères et de la Défense, et de trois secrétaires d'État, après le limogeage début août du Premier ministre, qui n'a pas été remplacé depuis.

Mohamed Ali Nafti, ancien diplomate ayant exercé dans plusieurs ambassades tunisiennes, notamment en Grèce, en Espagne et en Corée du Sud, est le nouveau chef de la diplomatie. Il occupait le poste de secrétaire d'État auprès du ministre des Affaires étrangères lorsque Kaïs Saïed l'avait démis de ses fonctions en 2021. 

Khaled Shili, également ex-diplomate et ancien responsable au ministère des Affaires étrangères, est désigné ministre de la Défense. Il a notamment été ambassadeur en Jordanie. 

Dérive autoritaire

Selon la présidence, les trois nouveaux secrétaires d'État assisteront le ministre des Affaires étrangères, le ministre de l'Agriculture et des ressources hydrauliques et celui de l'Emploi.

Le président Kaïs Saïed, 66 ans, démocratiquement élu en 2019, s'est accaparé tous les pouvoirs lors d'un coup de force le 25 juillet 2021, et est depuis accusé de dérive autoritaire par l'opposition et ses détracteurs. Il brigue aujourd'hui un second mandat présidentiel dans le cadre de ce qu'il a qualifié de "guerre de libération et d'autodétermination" visant à "établir une nouvelle république".

Face à lui lors de cette présidentielle prévue le 6 octobre, les deux autres candidats sont Zouhair Maghzaoui, un ex-député de la gauche panarabe, et un industriel quadragénaire, Ayachi Zammel, chef d'un parti libéral.

"Empêchés de se présenter"
Mardi, l'ONG Human Rights Watch (HRW) avait affirmé qu'"au moins huit candidats potentiels ont été poursuivis en justice, condamnés ou emprisonnés" et, de facto, "empêchés de se présenter". Il s'agit notamment des dirigeants de l'opposition Issam Chebbi et Ghazi Chaouachi, et de la cheffe du Parti destourien libre Abir Moussi, une figure de l'opposition nostalgique des anciens régimes de Habib Bourguiba et Zine El Abidine Ben Ali.

"Après avoir emprisonné des dizaines d'opposants et de militants de renom, les autorités ont écarté presque tous les concurrents sérieux de la course à la présidence, réduisant cette élection à une simple formalité", a déclaré Bassam Khawaja, directeur adjoint de la division Moyen-Orient/Afrique du Nord pour HRW.

Plusieurs candidats s'étaient notamment plaints d'avoir été entravés sur le plan administratif pour obtenir les formulaires de parrainages ainsi qu'un extrait de casier judiciaire.

Le 8 août, les services du président avaient annoncé le limogeage du Premier ministre Ahmed Hachani, sans donner d'explications officielles.

Après s'être octroyé les pleins pouvoirs, Kaïs Saïed a révisé la Constitution pour substituer au régime parlementaire en vigueur, un système ultraprésidentialiste où le Parlement n'a pratiquement plus de pouvoirs. Il a, en outre, selon ses opposants, démantelé la plupart des institutions de contrepoids instaurées depuis l'avènement de la démocratie et la chute de la dictature de Ben Ali en 2011, dans le sillage du Printemps arabe.
"""
lang ="Français"

# Print the values
print(content)
print(lang)



# Define your desired data structure.




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

prefix:
Voici votre réponse en {lang} :
[{{ "1": "...",
   "2": "...",
   "3": [
    "...",
    "...",
    "...",
    "...",
    "..."
  ],
    "4": "..." }}]
""",
    input_variables=["content", "lang"],
)

# And a query intended to prompt a language model to populate the data structure.
chain = prompt | model
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
















