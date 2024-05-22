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

python -m pip install openpyxl

# [path]
cd /Users/brunoflaven/Documents/02_copy/fmm_USECASES/pricing_mistral_chatgpt/

# LAUNCH the file
python merge_cost_estimation_1.py

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



import os
import pandas as pd
from datetime import datetime

# Get current date in the required format
date_created = datetime.now().strftime("%Y-%m-%d")
output_folder = "output/"
output_all_filename = f"{date_created}_output_all.xlsx"

# Find all .xlsx files in the output folder
xlsx_files = [file for file in os.listdir(output_folder) if file.endswith(".xlsx")]

# Check if there are any .xlsx files in the folder
if not xlsx_files:
    print("No .xlsx files found in the directory.")
else:
    # Create an empty list to store DataFrames of all sheets
    all_sheets = []

    # Iterate through each .xlsx file
    for file in xlsx_files:
        file_path = os.path.join(output_folder, file)
        # Read all sheets from the Excel file
        sheets = pd.read_excel(file_path, sheet_name=None)
        
        # Iterate through each sheet
        for sheet_name, df in sheets.items():
            # Add a column with the original filename for reference
            df['Original_Filename'] = file
            # Append the DataFrame of the current sheet to the list
            all_sheets.append(df)

    # Concatenate all DataFrames into a single DataFrame
    combined_data = pd.concat(all_sheets, ignore_index=True)

    # Write the combined data to a new Excel file
    output_path = os.path.join(output_folder, output_all_filename)
    combined_data.to_excel(output_path, index=False)
    print(f"Combined data saved to {output_all_filename} in the output folder.")




