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
streamlit run streamlit_app_mistral_cost_estimation_1.py

"""

import streamlit as st
from llm_cost_estimation import count_tokens

######### VALUES #########
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

# Model configurations with corresponding input/output prices
models = {
    "mistral-small": {"input_price": 1.85, "output_price": 5.55},
    "mistral-medium": {"input_price": 2.5, "output_price": 7.5},
    "mistral-large": {"input_price": 7.3, "output_price": 22},
    "open-mistral-7b": {"input_price": 0.2, "output_price": 0.2},
    "open-mixtral-8x7b": {"input_price": 0.65, "output_price": 0.65},
    "open-mixtral-8x22b": {"input_price": 1.9, "output_price": 5.6},
}

# Define dropdown options
words_per_article_options = [500, 1000, 1500, 2000]
volume_items_options = [1000, 50000, 100000]
multiplier_low = 1.33
multiplier_high = 1.5

# Streamlit Interface
st.title("Cost Estimation for LLM")

st.markdown('**Exemple de texte en Français**')
st.code (TEXT_SAMPLE_SUMMARY_LLM_FR_VROUX)

st.markdown('**Exemple de texte en Anglais**')
st.code (TEXT_SAMPLE_SUMMARY_LLM_EN_VROUX)


# Display the original text
st.write("### Original Text:")
st.write(TEXT_SAMPLE_SUMMARY_LLM_FR_VROUX)

# Display the word count
word_count = count_words(TEXT_SAMPLE_SUMMARY_LLM_FR_VROUX)
st.write(f"Word Count: {word_count}")

# Display the token count
token_count = count_text_tokens(TEXT_SAMPLE_SUMMARY_LLM_FR_VROUX)
st.write(f"Token Count: {token_count}")

# Display the token count for the prompt
prompt_token_count = count_prompt_tokens(TEXT_SAMPLE_SUMMARY_LLM_FR_VROUX)
st.write(f"Prompt Token Count: {prompt_token_count}")

# Display the estimated token count for the completion
completion_token_count = count_completion_tokens(TEXT_SAMPLE_SUMMARY_LLM_FR_VROUX)
st.write(f"Estimated Completion Token Count: {completion_token_count}")


st.subheader('2. Sélectionner les éléments')


st.info("Veuillez sélectionner les élements pour le calcul", icon="⚠️")


# Model selection dropdown
model_name = st.selectbox("Sélectionner un modèle", list(models.keys()))

# Variable configuration
nb_words_item = st.selectbox("Nombre de mots par contenu", words_per_article_options)
volume_items = st.selectbox("Volume (Nombre de contenus)", volume_items_options)

# Get model pricing
model_prices = models[model_name]
price_input = model_prices["input_price"]
price_output = model_prices["output_price"]

# Calculate token counts and costs
tokens_low = nb_words_item * multiplier_low
tokens_high = nb_words_item * multiplier_high


st.markdown('### Mistral Input')
st.write("**model_name**:", model_name)
st.write("**price_input**:", price_input)


st.write("**tokens_low**:", tokens_low)
st.write("**tokens_high**:", tokens_high)



st.write("**volume tokens LOW**:", tokens_low*volume_items)
st.write("**volume tokens HIGH**:", tokens_high*volume_items)


cost_low = (tokens_low * price_input * volume_items) / 1_000_000
cost_high = (tokens_high * price_input * volume_items) / 1_000_000

st.write("**cost_low in euros**:", cost_low)
st.write("**cost_high in euros**:", cost_high)

# Calculate costs (input and output)
# cost_low = (tokens_low * price_input * volume_items) / 1_000_000
# cost_high = (tokens_high * price_output * volume_items) / 1_000_000

# # Display results
# st.write("**Model Name**:", model_name)
# st.write("**Number of Tokens per content (Low)**:", round(tokens_low, 2))
# st.write("**Number of Tokens per content (High)**:", round(tokens_high, 2))
# st.write("**Cost Estimation (Low) in EUROS**: ", round(cost_low, 2))
# st.write("**Cost Estimation (High) in EUROS**: ", round(cost_high, 2))
