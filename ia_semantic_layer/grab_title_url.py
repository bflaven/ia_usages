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
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_semantic_layer


# LAUNCH the file
python grab_title_url.py

"""

import requests
from bs4 import BeautifulSoup

"""


+ CS106A: Programming Methodology
https://web.stanford.edu/class/cs106a/




"""


# List of URLs
urls = [
# "https://medium.com/@sendoamoronta/minerva-and-the-evolution-of-semantic-layers-in-modern-data-platforms-95299432f739",
# "https://airbnb.io/projects/",
# "https://medium.com/airbnb-engineering/how-airbnb-achieved-metric-consistency-at-scale-f23cc53dea70",
# "https://github.com/semanticdatalayer",
# "https://motherduck.com/blog/semantic-layer-duckdb-tutorial/",
# "https://github.com/boringdata/boring-semantic-layer",
# "https://ibis-project.org/",
# "https://github.com/topics/semantic-layer",
# "https://github.com/aurelio-labs/semantic-router",
# "https://docs.getdbt.com/docs/get-started-dbt",
# "https://github.com/microsoft/semantipy",
# "https://github.com/Canner/wren-engine",
# "https://www.getwren.ai/post/powering-ai-driven-workflows-with-wren-engine-and-zapier-via-the-model-context-protocol-mcp?hss_channel=lcp-89794921",
"https://web.stanford.edu/class/cs106a/"

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