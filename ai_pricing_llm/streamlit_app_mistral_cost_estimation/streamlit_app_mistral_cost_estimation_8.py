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
streamlit run streamlit_app_mistral_cost_estimation_8.py


005_api_key_pricing


# source
https://platform.openai.com/tokenizer

1 token ~= 4 chars in English
1 token ~= ¾ words
100 tokens ~= 75 words

1-2 sentence ~= 30 tokens
1 paragraph ~= 100 tokens
1,500 words ~= 2048 tokens



"""

# Input : every time you send text to the API, an additional 7 tokens are automatically added. 
# https://levelup.gitconnected.com/reduce-your-openai-api-costs-by-70-a9f123ce55a6



import streamlit as st
import pandas as pd

# Part 1: Select a model
model_options = ["mistral-small", "mistral-medium", "mistral-large", "open-mistral-7b", "open-mixtral-8x7b", "open-mixtral-8x22b", "gpt-4-turbo-2024-04-09", "gpt-3.5-turbo-0125"]
selected_model = st.selectbox("Models", model_options)

# Part 2: Price for one token for input and output
# Define prices per 1 Million tokens for each model
# For mistral https://mistral.ai/fr/technology/
# For openai https://openai.com/api/pricing/

# GPT-4 Turbo
# Model gpt-4-turbo-2024-04-09
# Input 10,00 US$ / 1M tokens = 9,29 Euros / 1M tokens
# Output 30,00 US$ / 1M tokens  = 27,86 Euros / 1M tokens
# https://wise.com/fr/currency-converter/usd-to-eur-rate?amount=10

# GPT-3.5 Turbo
# Model gpt-3.5-turbo-0125
# Input 0,50 US$ / 1M tokens = 0,46 Euros / 1M tokens 
# Output 1,50 US$ / 1M tokens = 1,39 Euros / 1M tokens 
# https://wise.com/fr/currency-converter/usd-to-eur-rate?amount=10
# 
prices = {
    "mistral-small": {"input": 0.9, "output": 2.8},
    "mistral-medium": {"input": 2.5, "output": 7.5},
    "mistral-large": {"input": 3.8, "output": 11.3},
    "open-mistral-7b": {"input": 0.2, "output": 0.2},
    "open-mixtral-8x7b": {"input": 0.65, "output": 0.65},
    "open-mixtral-8x22b": {"input": 1.9, "output": 5.6},
    "gpt-4-turbo-2024-04-09": {"input": 9.29, "output": 27.86},
    "gpt-3.5-turbo-0125": {"input": 0.46, "output": 1.39}

}
# Get the selected model's prices
# input_price = prices[selected_model]["input"] / 1000000
# output_price = prices[selected_model]["output"] / 1000000

input_price = (prices[selected_model]["input"] / 1e6)
output_price = (prices[selected_model]["output"] / 1e6)


st.write(input_price)
st.write(output_price)

# # Calculate the price for input tokens
# one_token_input_price = (0.9 / 1e6)

# # Calculate the price for input tokens
# one_token_output_price = (2.8 / 1e6)



# Part 3: Total of tokens regarding the volume
# Define character counts per content and volume of content
character_counts = [500, 1000, 1500, 2000]
content_volumes = [500, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 50000]

# Calculate number of tokens for input and output for each combination
token_estimations = []
for characters in character_counts:
    for volume in content_volumes:
        # input_tokens = characters * volume
        input_tokens = (4*characters) * volume
        # example
        # total_tokens = (4*char_count) * volume
        output_tokens = input_tokens # Assuming 1:1 input-output ratio
        token_estimations.append({
            "Characters": characters, 
            "Volume": volume, 
            "Input/Output Tokens": input_tokens}) 
            # "Output Tokens": output_tokens})

# Part 4: Global estimation costs
# Create a DataFrame for all combinations
df = pd.DataFrame(token_estimations)
# Calculate costs for input and output for each combination
df["Input Cost (€)"] = df["Input/Output Tokens"] * input_price
df["Output Cost (€)"] = df["Input/Output Tokens"] * output_price

# Show the DataFrame
st.dataframe(df)

# Save DataFrame to Excel with multiple sheets
with pd.ExcelWriter("output/"+selected_model+"_estimation_costs.xlsx") as writer:
    for characters in character_counts:
        sheet_name = f"{selected_model}_{characters}"
        df_filtered = df[df["Characters"] == characters]
        df_filtered.to_excel(writer, sheet_name=sheet_name, index=False)

st.info(f"{selected_model}""_estimation_costs.xlsx")



