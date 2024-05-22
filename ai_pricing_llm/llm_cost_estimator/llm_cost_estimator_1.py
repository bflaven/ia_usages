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


# [path]
cd /Users/brunoflaven/Documents/02_copy/fmm_USECASES/pricing_mistral_chatgpt/

# LAUNCH the file
python llm_cost_estimator_1.py


# source
https://github.com/Promptly-Technologies-LLC/llm_cost_estimation
https://llm-cost-estimator.readthedocs.io/en/latest/index.html


"""
from llm_cost_estimation import models
import pandas as pd


# EXAMPLE_1
for model in models:
    print(f'Model Name: {model["name"]}')
    print(f'Completion Cost Per Token: {model["completion_cost_per_token"]}')
    print(f'Prompt Cost Per Token: {model["prompt_cost_per_token"]}')
    print(f'Maximum Tokens: {model["max_tokens"]}')
    print(f'Description: {model["description"]}\n')


# EXAMPLE_2
# Convert the list of dictionaries to a DataFrame
models_df = pd.DataFrame(models)

# Display the DataFrame
print(models_df)




