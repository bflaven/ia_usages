"""
[env]
# Conda Environment
conda create --name llm_integration_api_costs python=3.9.13
conda create --name fmm_fastapi_poc python=3.9.13
conda info --envs
source activate llm_integration_api_costs
source activate fmm_fastapi_poc
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n llm_integration_api_costs
conda env remove -n fmm_fastapi_poc



# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manuel install
pip install streamlit
pip install llm_cost_estimation



# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ai_pricing_llm/streamlit_app_mistral_cost_estimation/

# LAUNCH the file
streamlit run streamlit_app_mistral_cost_estimation_2.py



"""

import streamlit as st
from llm_cost_estimation import count_tokens, models
import pandas as pd

######### VALUES #########


models_mistral = [
    {
        'name': 'mistral-small',
        'description': 'Description for mistral-small',
        'max_tokens': 'Max tokens for mistral-small',
        'prompt_cost_per_token': 'Prompt cost for mistral-small',
        'completion_cost_per_token': 'Completion cost for mistral-small'
    },
    {
        'name': 'mistral-medium',
        'description': 'Description for mistral-medium',
        'max_tokens': 'Max tokens for mistral-medium',
        'prompt_cost_per_token': 'Prompt cost for mistral-medium',
        'completion_cost_per_token': 'Completion cost for mistral-medium'
    },
    {
        'name': 'mistral-large',
        'description': 'Description for mistral-large',
        'max_tokens': 'Max tokens for mistral-large',
        'prompt_cost_per_token': 'Prompt cost for mistral-large',
        'completion_cost_per_token': 'Completion cost for mistral-large'
    },
    {
        'name': 'open-mistral-7b',
        'description': 'Description for open-mistral-7b',
        'max_tokens': 'Max tokens for open-mistral-7b',
        'prompt_cost_per_token': 'Prompt cost for open-mistral-7b',
        'completion_cost_per_token': 'Completion cost for open-mistral-7b'
    },
    {
        'name': 'open-mixtral-8x7b',
        'description': 'Description for open-mixtral-8x7b',
        'max_tokens': 'Max tokens for open-mixtral-8x7b',
        'prompt_cost_per_token': 'Prompt cost for open-mixtral-8x7b',
        'completion_cost_per_token': 'Completion cost for open-mixtral-8x7b'
    },
    {
        'name': 'open-mixtral-8x22b',
        'description': 'Description for open-mixtral-8x22b',
        'max_tokens': 'Max tokens for open-mixtral-8x22b',
        'prompt_cost_per_token': 'Prompt cost for open-mixtral-8x22b',
        'completion_cost_per_token': 'Completion cost for open-mixtral-8x22b'
    }
]


# all estiamtions for tokens comme from https://www.tokencounter.io/

# for gpt-3.5-turbo
# Number of Characters 1372
# Number of Tokens 391
# Estimated Cost $0.000586

# for gpt-4
# Number of Characters 1372
# Number of Tokens 391
# Estimated Cost $0.011730
# 
# Example_1 FR (vroux)
TEXT_SAMPLE_SUMMARY_LLM_FR_VROUX = "Dans les écoles, sur les terrains de basket, comme à la Maison Blanche, chaque année en février, les États-Unis fêtent le Black History Month, le mois de l'histoire des noirs. Cela fait bientôt 100 ans de ce rendez-vous historique existe, mais d'où vient cette célébration ? C'est Carter Cotwin Woodson qui a eu cette idée. Ce fils de deux esclaves affranchis est considéré comme le père de l'histoire afro-américaine. Il est seulement le deuxième homme noir à avoir obtenu un diplôme de l'université de Harvard. Et 50 ans après l'abolition de l'esclavage, il lance l'idée d'une Negro History Week dans la première édition à lieu en 1926. Woodson veut encourager les afro-américains à s'intéresser davantage à leur histoire et surtout, il veut que celle-ci soit enseignée dans les écoles. Il choisit la deuxième semaine de février pour cette célébration car c'est à l'église les deux grandes figures de l'abolitionnisme aux États-Unis. Peu à peu, le rendez-vous s'impose dans les États et les villes les plus progressistes. Woodson meurt en 1950, mais son idée lui survit. En 1976, pour le bicentenaire des États-Unis, le président Gerald Ford en fait une célébration officielle et la semaine devient un mois de l'histoire des noirs. En 2016, Barack Obama en fait le 40e anniversaire par ses mots depuis nos origines, l'histoire des noirs, c'est l'histoire des États-Unis."

# for gpt-3.5-turbo
# Number of Characters 1261
# Number of Tokens 262
# Estimated Cost $0.000393

# for gpt-4
# Number of Characters 1261
# Number of Tokens 262
# Estimated Cost $0.007860

 
TEXT_SAMPLE_SUMMARY_LLM_EN_VROUX = "In schools, on basketball courts, as well as at the White House, every year in February, the United States celebrates Black History Month. It's almost 100 years since this historic meeting existed, but where does this celebration come from? It was Carter Cotwin Woodson who had this idea. This son of two freed slaves is considered the father of African-American history. He is only the second black man to graduate from Harvard University. And 50 years after the abolition of slavery, he launched the idea of a Negro History Week in the first edition held in 1926. Woodson wanted to encourage African-Americans to be more interested in their history and above all, he wants it to be taught in schools. He chose the second week of February for this celebration because the two great figures of abolitionism in the United States were in church. Little by little, the meeting is taking hold in the most progressive states and cities. Woodson died in 1950, but his idea lived on. In 1976, for the United States Bicentennial, President Gerald Ford made it an official celebration and the week became Black History Month. In 2016, President Barack Obama marked the 40th anniversary with his words since our origins, black history is the history of the United States."

######### FUNCTIONS #########
# Function to count the number of words in the text
def count_words(text):
    words = text.split()
    return len(words)

# Function to count the number of tokens in the text
def count_text_tokens(text):
    return count_tokens(text)

# Function to count the number of tokens in a prompt
def count_prompt_tokens(text):
    # The prompt might include extra context, adding some overhead
    prompt = f"Please summarize the following text: {text}"
    return count_tokens(prompt)

# Function to count the estimated number of tokens in a completion
def count_completion_tokens(text):
    # In completion, the response might have a similar length to the prompt
    # This is a rough estimation; adjust as needed for your use case
    completion_text = f"This is a summary of the text: {text}"
    return count_tokens(completion_text)

######### APP #########



# Streamlit Interface
st.title("Cost Estimation for LLM")

# st.markdown('**Exemple de texte en Français**')
# st.code (TEXT_SAMPLE_SUMMARY_LLM_FR_VROUX)

# st.markdown('**Exemple de texte en Anglais**')
# st.code (TEXT_SAMPLE_SUMMARY_LLM_EN_VROUX)

# st.code(f"models: {models}")   
st.code(f"models_mistral: {models_mistral}")   

# Title for the app
st.title("Model Information Viewer")

# Dropdown menu to select a model
model_names = [model['name'] for model in models]
selected_model_name = st.selectbox("Select a Model", model_names)

# Get the selected model details
selected_model = next(model for model in models if model['name'] == selected_model_name)

# Display information about the selected model
st.write(f"### Model Information for: {selected_model['name']}")
st.write(f"**Completion Cost Per Token**: {selected_model['completion_cost_per_token']}")
st.write(f"**Prompt Cost Per Token**: {selected_model['prompt_cost_per_token']}")
# st.write(f"**Maximum Tokens**: {selected_model['max_tokens']}")
# st.write(f"**Description**: {selected_model['description']}")

# Convert the list of dictionaries to a DataFrame and display it
# models_df = pd.DataFrame(models)

# st.write("### Overview of All Models")
# st.dataframe(models_df)  
# This displays the DataFrame in the Streamlit app
