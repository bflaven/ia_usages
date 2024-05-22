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
streamlit run streamlit_app_mistral_cost_estimation_9.py


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
from datetime import datetime
import os.path

# Part 1: Select multiple models
model_options = ["mistral-small", "mistral-medium", "mistral-large", "open-mistral-7b", "open-mixtral-8x7b", "open-mixtral-8x22b", "gpt-4-turbo-2024-04-09", "gpt-3.5-turbo-0125"]
selected_models = st.multiselect("Models", model_options)

# Prices dictionary
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

creation_date = datetime.now().strftime("%Y-%m-%d")

# Part 3: Total of tokens regarding the volume
# Define character counts per content and volume of content
character_counts = [500, 1000, 1500, 2000]
content_volumes = [500, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 50000]

# Iterate over each selected model
for selected_model in selected_models:
    # Get the selected model's prices
    input_price = prices[selected_model]["input"] / 1000000
    output_price = prices[selected_model]["output"] / 1000000
    
    # Create a dictionary to store the results for this model
    results = {}
    
    # Iterate over each combination of character counts and content volumes
    for char_count in character_counts:
        for volume in content_volumes:
            # Calculate total tokens
            total_tokens = (4*char_count) * volume
            
            # Calculate estimation cost for input and output
            input_cost = total_tokens * input_price
            output_cost = total_tokens * output_price
            
            # Store the results
            key = f"Character Count: {char_count}, Content Volume: {volume}"
            results[key] = {"Input Cost": input_cost, "Output Cost": output_cost}
    
    # Create a DataFrame from the results
    df = pd.DataFrame(results).T

    # Define the file name
    file_name = f'{creation_date}_estimation_costs.xlsx'

    # Check if the file exists
    if not os.path.isfile(file_name):
        # If the file does not exist, create it with the DataFrame
        with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name=f'{selected_model} Estimation Costs')
    else:
        # If the file already exists, delete the existing sheet and write the new data
        with pd.ExcelWriter(file_name, mode='a', engine='openpyxl') as writer:
            # Open the existing workbook
            book = writer.book
            
            # Delete the sheet if it already exists
            try:
                del book[f'{selected_model} Estimation Costs']
            except KeyError:
                pass
            
            # Write the new data to the sheet
            df.to_excel(writer, sheet_name=f'{selected_model} Estimation Costs', index=False)
            st.warning(f"{selected_model} Estimation Costs has been added", icon="⚠️")


    st.info(f"{creation_date}_estimation_costs.xlsx has been created!", icon="ℹ️")


    


