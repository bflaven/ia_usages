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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_kpi_carbon_footprint_deepseek


# LAUNCH the file
python grab_title_url.py

"""

import requests
from bs4 import BeautifulSoup

"""

- DeepSeek
https://www.deepseek.com/


--- ollama commands
https://ollama.com/library/deepseek-r1
ollama run deepseek-r1:7b (nope)
ollama run deepseek-r1 (yep)


--- articles
https://medium.com/@pankaj_pandey/0497a4899cb2
https://ai.gopubby.com/integrating-deepseek-into-your-python-applications-118e9f5da50f
https://www.france24.com/fr/%C3%A9missions/info-%C3%A9co/20250128-deepseek-l-intelligence-artificielle-chinoise-qui-fait-trembler-la-tech-am%C3%A9ricaine
https://www.reuters.com/technology/artificial-intelligence/what-is-deepseek-why-is-it-disrupting-ai-sector-2025-01-27/


"https://www.deepseek.com/",
"https://ollama.com/library/deepseek-r1",
"https://medium.com/@pankaj_pandey/0497a4899cb2",
"https://ai.gopubby.com/integrating-deepseek-into-your-python-applications-118e9f5da50f",
"https://www.france24.com/fr/%C3%A9missions/info-%C3%A9co/20250128-deepseek-l-intelligence-artificielle-chinoise-qui-fait-trembler-la-tech-am%C3%A9ricaine",
"https://www.reuters.com/technology/artificial-intelligence/what-is-deepseek-why-is-it-disrupting-ai-sector-2025-01-27/"



+ A. KPI_CARBON_FOOTPRINT
--- Tools to test for kpi carbone


- 1. using codecarbon

! TESTING CODECARBON
check https://github.com/mlco2/codecarbon
https://github.com/mlco2/codecarbon/tree/master/examples

https://asciinema.org/a/667970

# OPEN-SOURCE
1. CodeCarbon (package Python)
https://codecarbon.io/
https://github.com/mlco2/codecarbon
https://pypi.org/project/codecarbon/



- 2. using Eco2AI

2. Eco2AI
https://github.com/sb-ai-lab/Eco2AI
014_carbon_footprint_eco2ai.py



- 3. carbontxt.org

https://carbontxt.org/quickstart
https://github.com/thegreenwebfoundation/carbon-txt-validator/

Using the Green Web Foundation carbon.txt validator

# command does not work
python -m pip install carbon-txt


https://developers.thegreenwebfoundation.org/

https://www.thegreenwebfoundation.org/news/introducing-our-new-work-on-carbon-txt-the-carbon-txt-validator-and-an-updated-spec/
https://github.com/thegreenwebfoundation/carbon-txt-validator

- 4. OTHER

check https://www.cloudcarbonfootprint.org/

CarbonAI 
https://capgemini-invent-france.github.io/CarbonAI/
https://github.com/Capgemini-Invent-France/CarbonAI?tab=readme-ov-file


! extended search with tags on github.
https://github.com/topics/co2-monitoring?l=python



# AZURE
1. Azure Sustainability Calculator
https://www.microsoft.com/en-us/sustainability/emissions-impact-dashboard

4. Cloud Carbon Footprint (open source) pour Azure
https://github.com/microsoft/azure-carbon-estimator

5. Azure Emissions Impact Dashboard (natif Azure)
https://www.microsoft.com/en-us/sustainability/emissions-impact-dashboard


6. CO2.JS (librairie JavaScript)
https://github.com/orgs/thegreenwebfoundation/repositories?q=lang%3Apython&type=all


# OTHER
https://www.cloudcarbonfootprint.org/
https://medium.com/intel-analytics-software/reduce-large-language-model-carbon-footprint-with-intel-neural-compressor-and-intel-extension-for-dfadec3af76a
https://medium.com/@thesab/unmasking-the-dirty-secret-of-large-language-models-their-carbon-footprint-9bac7ae2da5e
https://github.com/Jjing-Liang/LLMCarbon--
https://medium.com/codesphere-cloud/how-to-build-a-llm-powered-carbon-footprint-analysis-app-28ef85cf51ec
https://github.com/MohitRS/EcoLLM
https://medium.com/@made_tech/measuring-the-carbon-footprint-of-your-python-applications-43c0c279d4a0
https://github.com/topics/carbon-footprint
https://github.com/topics/carbon-footprint?l=python
https://github.com/mukesh1322/carbon_footprint


"""


# List of URLs
urls = [

'https://github.com/mlco2/codecarbon',
'https://github.com/mlco2/codecarbon/tree/master/examples',
'https://asciinema.org/a/667970',
'https://codecarbon.io/',
'https://github.com/mlco2/codecarbon',
'https://pypi.org/project/codecarbon/',
'https://github.com/sb-ai-lab/Eco2AI',
'https://developers.thegreenwebfoundation.org/',
'https://www.thegreenwebfoundation.org/news/introducing-our-new-work-on-carbon-txt-the-carbon-txt-validator-and-an-updated-spec/',
'https://github.com/thegreenwebfoundation/carbon-txt-validator',
'https://www.cloudcarbonfootprint.org/',
'https://capgemini-invent-france.github.io/CarbonAI/',
'https://github.com/Capgemini-Invent-France/CarbonAI?tab=readme-ov-file',
'https://github.com/topics/co2-monitoring?l=python',
'https://www.microsoft.com/en-us/sustainability/emissions-impact-dashboard',
'https://github.com/microsoft/azure-carbon-estimator',
'https://www.microsoft.com/en-us/sustainability/emissions-impact-dashboard',
'https://github.com/orgs/thegreenwebfoundation/repositories?q=lang%3Apython&type=all',
'https://www.cloudcarbonfootprint.org/',
'https://medium.com/intel-analytics-software/reduce-large-language-model-carbon-footprint-with-intel-neural-compressor-and-intel-extension-for-dfadec3af76a',
'https://medium.com/@thesab/unmasking-the-dirty-secret-of-large-language-models-their-carbon-footprint-9bac7ae2da5e',
'https://github.com/Jjing-Liang/LLMCarbon--',
'https://medium.com/codesphere-cloud/how-to-build-a-llm-powered-carbon-footprint-analysis-app-28ef85cf51ec',
'https://github.com/MohitRS/EcoLLM',
'https://medium.com/@made_tech/measuring-the-carbon-footprint-of-your-python-applications-43c0c279d4a0',
'https://github.com/topics/carbon-footprint',
'https://github.com/topics/carbon-footprint?l=python',
'https://github.com/mukesh1322/carbon_footprint',

]

"""


"""
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
        # print(f"<li>{title_text}<br><a href=\"{url}\" target=\"_blank\" rel=\"noopener\">{url}</a></li>")

        # Append to the HTML code
        html_code += f"<li>{title_text}<br><a href=\"{url}\" target=\"_blank\" rel=\"noopener\">{url}</a></li>"

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")

# Print the full HTML code
print("\n--- Full HTML Code")
print("\n\n")
print(html_code)
print("\n\n")