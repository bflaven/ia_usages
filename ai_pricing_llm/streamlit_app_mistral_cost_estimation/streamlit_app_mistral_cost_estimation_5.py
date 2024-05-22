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
streamlit run streamlit_app_mistral_cost_estimation_5.py


# source
https://platform.openai.com/tokenizer

1 token ~= 4 chars in English
1 token ~= ¾ words
100 tokens ~= 75 words

1-2 sentence ~= 30 tokens
1 paragraph ~= 100 tokens
1,500 words ~= 2048 tokens



"""

import streamlit as st
import pandas as pd

# Input : every time you send text to the API, an additional 7 tokens are automatically added. 
# https://levelup.gitconnected.com/reduce-your-openai-api-costs-by-70-a9f123ce55a6


# Part_1: Select a model
model_options = ["mistral-small"]
selected_model = st.selectbox("Models", model_options)

# Part_2: Price for one token for input and output
input_price_per_million_tokens = 0.9  # €1.85 per 1 Million tokens
output_price_per_million_tokens = 2.8  # €5.55 per 1 Million tokens

# Estimation for one token input and output price
# Calculate the price for input tokens
one_token_input_price = (0.9 / 1e6)

# Calculate the price for input tokens
one_token_output_price = (2.8 / 1e6)

# st.write(one_token_input_price)
# st.write(one_token_output_price)



# Part_3: Total of tokens regarding the volume
characters_per_content = [500, 1000, 1500, 2000]
volume_of_content = [500, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 50000]

# Estimation for the number of Tokens both for Input and Output
token_estimations = []
for char_count in characters_per_content:
    for content_count in volume_of_content:
        tokens_input = char_count * (content_count)
        tokens_output = tokens_input  # Assuming 1:1 input-output ratio
        
        estimated_input_total_cost = (tokens_input*one_token_input_price)
        estimated_output_total_cost = (tokens_output*one_token_output_price)

        token_estimations.append({
            "Characters Per Content": char_count,
            "Volume of Content": content_count,
            # "Tokens Input": tokens_input,
            # "Tokens Output": tokens_output,
            "Input : Estimated Total Cost": estimated_input_total_cost,
            "Output : Estimated Total Cost": estimated_output_total_cost
        })

# Part_4: Global estimation costs
df = pd.DataFrame(token_estimations)

# Displaying the results
# st.write("Estimation for one token input price: €", round(one_token_input_price, 5))
# st.write("Estimation for one token output price: €", round(one_token_output_price, 5))



st.write("Estimation for the number of Tokens for Input and Output:")
st.write(df)



