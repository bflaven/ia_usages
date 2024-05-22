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
cd /Users/brunoflaven/Documents/02_copy/fmm_USECASES/pricing_mistral_chatgpt/

# LAUNCH the file
streamlit run streamlit_app_mistral_cost_estimation_6.py


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


import streamlit as st
import pandas as pd

# Part 1: Select a model
model_options = ["mistral-small", "mistral-medium", "mistral-large"]
selected_model = st.selectbox("Models", model_options)
# Here, we create a dropdown menu with model options and let the user select one.

# Part 2: Price for one token for input and output
# Define prices per 1 Million tokens for each model
prices = {
    "mistral-small": {"input": 0.9, "output": 2.8},
    "mistral-medium": {"input": 2.5, "output": 7.5},
    "mistral-large": {"input": 3.8, "output": 11.3}
}
# Get the selected model's prices
input_price = prices[selected_model]["input"] / 1000000
output_price = prices[selected_model]["output"] / 1000000
# Convert prices from per 1M tokens to per 1 token.

# Part 3: Total of tokens regarding the volume
# Define character counts per content and volume of content
character_counts = [500, 1000, 1500, 2000]
content_volumes = [500, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 50000]

# Calculate number of tokens for input and output for each combination
token_estimations = []
for characters in character_counts:
    for volume in content_volumes:
        input_tokens = characters * volume
        output_tokens = input_tokens # Assuming 1:1 input-output ratio
        token_estimations.append({
            "Characters": characters, 
            "Volume": volume, 
            "Input Tokens": input_tokens, 
            "Output Tokens": output_tokens})

# Part 4: Global estimation costs
# Create a DataFrame for all combinations
df = pd.DataFrame(token_estimations)
# Calculate costs for input and output for each combination
df["Input Cost (€)"] = df["Input Tokens"] * input_price
df["Output Cost (€)"] = df["Output Tokens"] * output_price

# Show the DataFrame
st.dataframe(df)
# Save DataFrame to CSV
df.to_csv("estimation_costs.csv", index=False)






