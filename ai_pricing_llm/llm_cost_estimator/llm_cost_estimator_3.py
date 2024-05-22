"""
[env]
# Conda Environment
conda create --name llm_integration_api_costs python=3.9.13
conda create --name fmm_fastapi_poc python=3.9.13
conda info --envs
source activate llm_integration_api_costs
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n llm_integration_api_costs



# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manuel install
pip install mistralai
pip install langchain-mistralai
pip install python-dotenv
pip install streamlit-authenticator
pip install aiohttp
pip install ydata-profiling
pip install streamlit_pandas_profiling
pip install tiktoken
python -m pip install tiktoken
python -m pip install llm_cost_estimation
python -m pip install pandas
python -m pip install Jinja2




# [path]
cd /Users/brunoflaven/Documents/02_copy/fmm_USECASES/pricing_mistral_chatgpt/

# LAUNCH the file
python llm_cost_estimator_3.py


# source
https://github.com/Promptly-Technologies-LLC/llm_cost_estimation
https://llm-cost-estimator.readthedocs.io/en/latest/index.html


"""
import pandas as pd
from llm_cost_estimation import models, count_tokens, estimate_cost


### EXAMPLE_1 ###
# text = "Hello, how are you?"
# model = "gpt-4"

# Count tokens in the text
# prompt_tokens, estimated_completion_tokens = count_tokens(text, model)

# print(f"Number of tokens in the prompt: {prompt_tokens}")
# print(f"Estimated number of tokens in the completion: {estimated_completion_tokens}")

### EXAMPLE_2 ###
# prompt = "Hello, how are you?"
# model = "gpt-4"

# prompt = """[INST] En français, vous êtes un gestionnaire de communauté intelligent et futé. Rédigez en français un message attractif editorialement qui comprend environ de 150 à 300 caractères  pour une publication en ligne sur le sujet donné dans le contenu. Pour ce message, il faut veiller à incorporer les meilleures pratiques d'optimisation des médias sociaux (SMO). Si le message généré contient des entités notamment les "GPE" ou Entité géopolitique, c'est-à-dire pays, villes, États, il faut transformer l'entité en hashtag et ajouter quand c'est possible l'emoji du drapeau du pays par exemple. Il faut enfin ajouter un hashtag pour le fait editorialement saillant dans le sujet donné dans le contenu. Dans le message, tous les hashtags et les emojis doivent être ajoutés dans le sens de la lecture c'est à dire ni en fin de proposition ni en début de proposition.
# Pour chaque proposition en français, n'imprimez que le résultat dans un objet Python dictionary avec 'message' sous forme de chaîne contenant les hashtags et les emojis comme indiqué plus haut, 'hashtags' sous forme de liste de hashtags et 'emojis' sous forme de liste de emojis. Dans la liste des hashtags, pour chaque hashtag, n'oubliez pas d'ajouter le signe "#" devant celui-ci, par exemple "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"]. Dans la liste des emojis, pour chaque emoji, voilà un exemple "emojis": ["emoji1", "emoji2", "emoji3"]. Incluez tous les résultats dans un objet Python list comme défini ci-dessous.
#     \n
#     Format de Sortie:\n
#     [
#     {{"message": "La valeur du message avec les hashtags et les emojis", "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"], "emojis": ["emoji1", "emoji2", "emoji3"]}},
#     ]
#     \n
#     Contenu: {content}
# \n
#     \n[/INST]"""
# model = "gpt-4"




# Estimate the cost for the completion
# estimated_cost = estimate_cost(prompt, model)
# print(f"Estimated cost of this completion: {estimated_cost}")

### EXAMPLE_3 ###

chat_history = [{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"}]
model = "gpt-4"

# Estimate the cost for the completion
estimated_cost = estimate_cost(chat_history, model)
