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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_spacy_llm


# LAUNCH the file
python grab_title_url.py

"""

import requests
from bs4 import BeautifulSoup

# List of URLs
urls = [

# library pysentence-similarity 
"https://pypi.org/project/pysentence-similarity/",
# library spacy-llm
"https://github.com/explosion/spacy-llm?tab=readme-ov-file",
"https://medium.com/@pankaj_pandey/spacy-llm-integrating-llms-into-structured-nlp-pipelines-7134dd05ebc2",
"https://github.com/patmejia/spacy-llm",
"https://github.com/wjbmattingly/tap-2024-spacy-llms/tree/main",
# guide
"https://ai.plainenglish.io/ensuring-accuracy-a-guide-to-validating-large-language-model-outputs-b24ea780aff7",
# guardrails
"https://github.com/guardrails-ai/guardrails?tab=readme-ov-file",
# diverse 
"https://github.com/agiga-quanta/Translation-is-fun/tree/main/Examples/Sentence%20similarity%20pairs",
"https://www.analyticsvidhya.com/blog/2024/11/all-minilm-l6-v2/",
"https://medium.com/@rahultiwari065/unlocking-the-power-of-sentence-embeddings-with-all-minilm-l6-v2-7d6589a5f0aa",
"https://github.com/agiga-quanta/Translation-is-fun/tree/main/Examples/Sentence%20similarity%20pairs",
"https://github.com/agiga-quanta/Translation-is-fun/tree/main/Examples/Sentence%20similarity%20ranked",
"https://github.com/agiga-quanta/Translation-is-fun/tree/main/Examples/Zero%20shot%20classification"
]

"""
# ecology
"https://www.newsweek.com/will-ai-another-unsustainable-environmental-disaster-opinion-1928737",
"https://www.unep.org/news-and-stories/story/ai-has-environmental-problem-heres-what-world-can-do-about",
"https://hbr.org/2024/07/the-uneven-distribution-of-ais-environmental-impacts",
"https://www.technologyreview.com/2024/05/23/1092777/ai-is-an-energy-hog-this-is-what-it-means-for-climate-change/",
"https://earth.org/the-green-dilemma-can-ai-fulfil-its-potential-without-harming-the-environment/",
"https://www.nature.com/articles/d41586-024-00478-x",
"https://www.nature.com/articles/s41599-024-03520-5"

# capitalism
"https://www.forbes.com/sites/laurasmythe/2023/02/03/forbes-daily-will-ai-break-capitalism/",
"https://www.imf.org/en/Publications/Staff-Discussion-Notes/Issues/2024/01/14/Gen-AI-Artificial-Intelligence-and-the-Future-of-Work-542379",
"https://www.imf.org/en/Blogs/Articles/2024/01/14/ai-will-transform-the-global-economy-lets-make-sure-it-benefits-humanity",
"https://www.sciencedirect.com/science/article/pii/S0160791X21002074"


# library pysentence-similarity 
"https://pypi.org/project/pysentence-similarity/",
# library spacy-llm
"https://github.com/explosion/spacy-llm?tab=readme-ov-file",
"https://medium.com/@pankaj_pandey/spacy-llm-integrating-llms-into-structured-nlp-pipelines-7134dd05ebc2",
"https://github.com/patmejia/spacy-llm",
"https://github.com/wjbmattingly/tap-2024-spacy-llms/tree/main",
# guide
"https://ai.plainenglish.io/ensuring-accuracy-a-guide-to-validating-large-language-model-outputs-b24ea780aff7",
# guardrails
"https://github.com/guardrails-ai/guardrails?tab=readme-ov-file",
# diverse 
"https://github.com/agiga-quanta/Translation-is-fun/tree/main/Examples/Sentence%20similarity%20pairs",
"https://www.analyticsvidhya.com/blog/2024/11/all-minilm-l6-v2/",
"https://medium.com/@rahultiwari065/unlocking-the-power-of-sentence-embeddings-with-all-minilm-l6-v2-7d6589a5f0aa",
"https://github.com/agiga-quanta/Translation-is-fun/tree/main/Examples/Sentence%20similarity%20pairs",
"https://github.com/agiga-quanta/Translation-is-fun/tree/main/Examples/Sentence%20similarity%20ranked",
"https://github.com/agiga-quanta/Translation-is-fun/tree/main/Examples/Zero%20shot%20classification"


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
