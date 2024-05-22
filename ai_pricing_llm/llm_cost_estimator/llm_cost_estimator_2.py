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
python llm_cost_estimator_2.py


# source
https://github.com/Promptly-Technologies-LLC/llm_cost_estimation
https://llm-cost-estimator.readthedocs.io/en/latest/index.html


"""
import pandas as pd
from llm_cost_estimation import models

# Convert the list of dictionaries to a DataFrame
models_df = pd.DataFrame(models)

# Apply the desired style to the DataFrame
styled_df = models_df.style\
    .hide(axis="index")\
    .set_properties(**{'max-width': '80px'})\
    .set_properties(subset=['description'], **{'max-width': '280px'})\
    .set_table_styles([dict(selector="th", props=[('max-width', '85px'), ('word-break', 'break-all')])])

# Save the styled DataFrame to an HTML file
html_file_path = "styled_models.html"

# Get the HTML representation of the styled DataFrame
html_representation = styled_df.to_html()

# Write the HTML content to a file
with open(html_file_path, "w") as f:
    f.write(html_representation)

print(f"Styled DataFrame saved to {html_file_path}")






