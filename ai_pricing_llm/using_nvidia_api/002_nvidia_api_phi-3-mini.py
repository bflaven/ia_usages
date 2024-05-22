
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
python -m pip install openai



# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ai_pricing_llm/using_nvidia_api/

# LAUNCH the file
python 002_nvidia_api_phi-3-mini.py


# source
https://build.nvidia.com/explore/discover#phi-3-mini

# required
You need to register in nvidia.com and grab an API KEY


"""

# for api key
import os
from dotenv import load_dotenv
from openai import OpenAI

### 1. GET API KEY ###
# Load environment variables from the .env file
load_dotenv()

# Access the API key using os.getenv
api_key = os.getenv("NVIDIA_API_KEY")

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = api_key
)

# prompt="""
# Who is Barack Obama?
# """

prompt="""
Who is Elfriede Jelinek?
"""


completion = client.chat.completions.create(
  model="microsoft/phi-3-mini-128k-instruct",
  messages=[{"role":"user","content":prompt}],
  temperature=0.2,
  top_p=0.7,
  max_tokens=1024,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")

