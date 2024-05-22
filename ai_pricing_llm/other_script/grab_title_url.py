#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name grab_title_url python=3.9.13
conda info --envs
source activate grab_title_url
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n grab_title_url


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

pip install beautifulsoup4
pip install requests

python -m pip install beautifulsoup4
python -m pip install requests

# [path]
cd /Users/brunoflaven/Documents/02_copy/fmm_USECASES/pricing_mistral_chatgpt/

# LAUNCH the file
python grab_title_url.py

"""

import requests
from bs4 import BeautifulSoup

# List of URLs
urls = [
    "https://levelup.gitconnected.com/reduce-your-openai-api-costs-by-70-a9f123ce55a6",
"https://openai.com/api/pricing",
"https://mistral.ai/fr/technology/#models",
"https://github.com/FareedKhan-dev/basiclingua-LLM-Based-NLP",
"https://cookbook.openai.com/examples/entity_extraction_for_long_documents",
"https://levelup.gitconnected.com/reduce-your-openai-api-costs-by-70-a9f123ce55a6",
"https://github.com/FareedKhan-dev/basiclingua-LLM-Based-NLP",
"https://blog.wordbot.io/ai-artificial-intelligence/understanding-gpt3-cost-in-depth-using-a-real-example/",
"https://www.tokencounter.io/",
"https://azure.microsoft.com/en-us/free/ai-services/",
"https://techcommunity.microsoft.com/t5/ai-machine-learning-blog/mistral-large-mistral-ai-s-flagship-llm-debuts-on-azure-ai/ba-p/4066996",
"https://github.com/openai/tiktoken",
"https://github.com/Promptly-Technologies-LLC/llm_cost_estimation",
"https://github.com/microsoft/LLMLingua",
"https://github.com/magdalenakuhn17/awesome-cheap-llms",
"https://github.com/AnthusAI/LLM-Price-Comparison",
"https://medium.com/@fbanespo/build-a-token-counter-and-cost-estimator-with-streamlit-and-openai-2181e603f7cb",
"https://www.newtuple.com/post/the-ultimate-pricing-cheat-sheet-for-large-language-models",
"https://medium.com/artefact-engineering-and-data-science/llms-deployment-a-practical-cost-analysis-e0c1b8eb08ca",
"https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/how-to-evaluate-llms-a-complete-metric-framework/",
"https://llm-cost-estimator.readthedocs.io/en/latest/index.html",
"https://github.com/egordm/RougLLy",
"https://simmering.dev/blog/llm-price-performance/",
"https://www.tensorops.ai/post/understanding-the-cost-of-large-language-models-llms",
"https://www.tensorops.ai/post/prompt-engineering-techniques-practical-guide",
"https://github.com/TensorOpsAI/LLMStudio",
"https://www.tokencounter.io/",
"https://www.llmcalc.com/",
"https://llmpricecheck.com/",
"https://llmpricecheck.com/calculator",
"https://pypi.org/project/llm_cost_estimation/",
"https://llm-price.com/",
"https://github.com/g-simmons/llm-cost-estimator",
"https://github.com/AgentOps-AI/tokencost",
"https://vinlam.com/posts/local-llm-options/",
"https://github.com/VidhyaVarshanyJS/EnsembleX",
"https://platform.openai.com/tokenizer",
"https://francemm.atlassian.net/browse/IA-98",
"https://mistral.ai/fr/technology/",
"https://platform.openai.com/docs/guides/rate-limits/usage-tiers",
"https://mistral.ai/fr/technology/",
"https://azure.microsoft.com/en-us/pricing/purchase-options/pay-as-you-go",
"https://techcommunity.microsoft.com/t5/ai-machine-learning-blog/mistral-large-mistral-ai-s-flagship-llm-debuts-on-azure-ai/ba-p/4066996",
"https://docs.mistral.ai/deployment/cloud/azure/"
    # Add more URLs as needed
]

# Store the HTML code
html_code = ""

# Iterate through each URL
for url in urls:
    try:
        # Fetch the HTML content of the URL
        response = requests.get(url)
        html_content = response.text

        # Parse HTML using Beautiful Soup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the title tag
        title_tag = soup.title

        # Extract text from the title tag
        title_text = title_tag.text if title_tag else "Title Not Found"

        # Print the URL and the title text
        print(f"<li>{title_text}<br><a href=\"{url}\" target=\"_blank\" rel=\"noopener\">{url}</a></li>")

        # Append to the HTML code
        html_code += f"<li>{title_text}<br><a href=\"{url}\" target=\"_blank\" rel=\"noopener\">{url}</a></li>"

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")

# Print the full HTML code
print("\n--- Full HTML Code")
print("\n\n")
print(html_code)
print("\n\n")