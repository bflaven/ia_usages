#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name fmm_fastapi_poc python=3.9.13
conda info --envs
source activate fmm_fastapi_poc
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n fmm_fastapi_poc


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
cd /Users/brunoflaven/Documents/01_work/blog_articles/build_vue_js_on_fastapi

# LAUNCH the file
python grab_title_url.py

"""

import requests
from bs4 import BeautifulSoup

# List of URLs
"""
urls = [
"https://github.com/moking55/simple-vue-and-fastapi-face-recognizer", 
"https://github.com/kotaaaa/employees-app", 
"https://testdriven.io/blog/developing-a-single-page-app-with-fastapi-and-vuejs/", 
"https://www.haydenbarnett.dev/articles/integrating-fastapi-and-react", 
"https://github.com/krassykirov/FastAPI-Vue", 
"https://betterdatascience.com/deploy-a-machine-learning-model-with-fastapi/", 
"https://betterdatascience.com/deploy-a-machine-learning-model-with-fastapi/", 
"https://github.com/jfbriggs/nhl-award-vue-fastapi/tree/master", 
"https://github.com/krassykirov/FastAPI-Vue", 
"https://github.com/dwisulfahnur/blog-fastapi-vuejs", 
"https://github.com/serj2626/fapi-vue-interviews", 
"https://github.com/najeeb67/Hospital-Project-in-Python-and-Js", 
"https://github.com/joaovitoriasilva/endurain", 
"https://github.com/tiangolo/full-stack-fastapi-template", 
"https://github.com/wpcodevo/fastapi_sqlalchemy", 
"https://github.com/KenMwaura1/Fast-Api-Vue/tree/main", 
"https://github.com/martinrenner/RENBoard", 
"https://github.com/cofin/fastapi-vite", 
"https://github.com/SamuelEarl/svelte-fastapi-demo-app", 
"https://github.com/venkyPy-2019/FastAPI", 
"https://github.com/eno-conan/vite-fastapi_sqlalchemy/tree/main", 
"https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-12-react-js-frontend/", 
"https://testdriven.io/blog/fastapi-react/", 
"https://github.com/MehdiRtal/nuxt-fastapi-template/tree/main", 
"https://github.com/junkei-okinawa/hasura-postgres-fastapi-nuxtjs-vuetify", 
"https://github.com/Sakops/Nuxtjs-with-FastAPI", 
"https://github.com/rasheedjdh/vuejs-nuxtjs-fastapi", 
"https://github.com/it21024818/CafeGreenRestuarentManagementSystem", 
"https://github.com/TutorFx/nuxtjs-fastapi", 
"https://medium.com/codex/how-to-integrate-fastapi-with-vuejs-ef6734b308fd", 
"https://github.com/testdrivenio/fastapi-vue/tree/main/services", 
"https://dimmaski.com/serve-vue-fastapi/", 
"https://www.ichaoran.com/data-story/visualization/data-engineering/fastapi-vue-app/", 
"https://towardsdatascience.com/build-an-ai-based-autocomplete-in-the-browser-using-vue-js-fastapi-and-websockets-1eb7ae19bfd8", 
"https://www.the-analytics.club/deploy-machine-learning-models-using-fast-api/"
]
"""
urls = [
# "https://www.digitalocean.com/community/tutorials/vuejs-rest-api-axios",
# "https://dev.to/bugintheconsole/axios-vuejs-3-pinia-a-comfy-configuration-you-can-consider-for-an-api-rest-1i5c",
# "https://juliensalinas.com/fr/connecter-SPA-frontend-vuejs-axios-API-backend/",
# "https://medium.com/@techclaw/rendering-api-data-with-vue-js-and-axios-1e600c6f1031",
# "https://codesource.io/blog/building-an-e-commerce-app-with-vue-js-vuex-axios/"
"https://codesandbox.io/s/vue",
"https://www.bezkoder.com/vue-3-crud/",
"https://github.com/bezkoder/vue-3-crud",
"https://www.freecodecamp.org/news/the-vue-handbook-a-thorough-introduction-to-vue-js-1e86835d8446/",
"https://www.digitalocean.com/community/tutorials/how-to-use-vue-js-and-axios-to-display-data-from-an-api",
"https://www.sitepoint.com/fetching-data-third-party-api-vue-axios/",
"https://techclaw.org/rendering-api-data-with-vue-js-and-axios/",
"https://www.digitalocean.com/community/tutorials/vuejs-rest-api-axios",
"https://dev.to/bugintheconsole/axios-vuejs-3-pinia-a-comfy-configuration-you-can-consider-for-an-api-rest-1i5c",
"https://juliensalinas.com/fr/connecter-SPA-frontend-vuejs-axios-API-backend/",
"https://medium.com/@techclaw/rendering-api-data-with-vue-js-and-axios-1e600c6f1031",
"https://codevoweb.com/vue-query-and-axios-crud-app/",
"https://medium.com/@sangeeth123sj/how-to-create-a-web-app-using-fastapi-vuejs-and-mongodb-for-generating-and-showcasing-images-193ccdb20091",
"https://github.com/pelocho/VueFastAPILearning",
"https://github.com/calvin-giese/VueFastAPIExample",
"https://github.com/pelocho/VueFastAPILearning",
"https://github.com/huyunlei/VueFast",
"https://github.com/jitsejan/fastapi-sqlalchemy-tutorial",
"https://github.com/dwisulfahnur/blog-fastapi-vuejs",
"https://github.com/frodrig3ND/DailyDashV2"
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