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

# manual install
To complete

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_prompt_seo/

# launch the file
python aso_prompts_1.py

"""

# for api key
import os
from dotenv import load_dotenv

# Import the OpenAI class from the openai module
from openai import OpenAI

### 1. GET API KEY ###
# Load environment variables from the .env file
load_dotenv()

# Access the API key using os.getenv
api_key = os.getenv("OPENAI_API_KEY")

# Get the model
model_selected = "gpt-3.5-turbo"
# model_selected = "gpt-4-turbo"


### 2. GET STUFF FROM CHATGPOT ###
# Create an instance of the OpenAI class with the provided API key
client = OpenAI(api_key=api_key)

def openai_chat(prompt_key, user_input):
    # Create the user prompt from the dictionary
    user_prompt = aso_prompts[prompt_key].format(user_input=user_input)

    # Create a chat completion using the OpenAI client
    response = client.chat.completions.create(
        model=model_selected, 
        messages=[{"role": "user", "content": user_prompt}]
    )

    # Response from the chat completion
    answer = response.choices[0].message.content

    # Assuming response and model_selected are defined and have valid values
    if model_selected == "gpt-3.5-turbo":
        input_price = response.usage.prompt_tokens * (0.46 / 1e6)
        output_price = response.usage.completion_tokens * (1.38 / 1e6)
    elif model_selected == "gpt-4-turbo":
        input_price = response.usage.prompt_tokens * (9.18 / 1e6)
        output_price = response.usage.completion_tokens * (27.55 / 1e6)
    else:
        raise ValueError("Invalid model selected. Please choose between 'gpt-3.5-turbo' and 'gpt-4-turbo'.")

    # Calculate the total price
    total_price = input_price + output_price

    # Return the answer, input price, output price, total price
    return {
        "answer": answer,
        "input_price": f"€ {input_price}",
        "output_price": f"€ {output_price}",
        "total_price": f"€ {total_price}"
    }


 
user_input = """
"""

###### All prompts ######

aso_prompts={

### 1. Title Optimization:

# "aso_title_optimization" : """ 
# As an ASO (App Store Optimization) expert proficient, could you create 10 compelling application titles in {aso_app_main_language} for an {aso_app_main_os} mobile application ? Please do follow these guidelines: 1. Keep the title within the 30-character limit to ensure it displays correctly across all devices. 2 Incorporate primary keywords that users are likely to search for "{aso_app_primary_keywords}"" 3. Ensure your brand name "{aso_app_brand_name}"
# """

# "aso_title_optimization" : """ 
# As an ASO (App Store Optimization) expert proficient, could you create 10 compelling application titles in French for an IOS mobile application ? Please do follow these guidelines: 1. Keep the title within the 30-character limit to ensure it displays correctly across all devices. 2. Incorporate primary keywords that users are likely to search for "{user_input}" 3. Ensure your brand name "FRANCE 24"
# """,

### 2. Subtitle Optimization:
"aso_subtitle_optimization" : """ 
As a seasoned ASO (App Store Optimization) specialist, can you generate 10 captivating application subtitles for an iOS mobile app, using "{user_input}". The subtitles should include synonyms or variations of the keyword to ensure diversity. Please adhere to the strict 30-character limit for subtitles to maintain compatibility with the App Store guidelines.
""",

### 3. Add Keywords
"aso_add_keywords" : """ 
As an ASO (App Store Optimization) expert proficient, could you create a list of compelling application keywords for an IOS mobile application ? Please do follow these guidelines: 1. Incorporate primary keywords that users are likely to search for "{user_input}" 3. Ensure your brand name "FRANCE 24"
""",

### 4. Engaging App Descriptions
"aso_engaging_app_descriptions" : """ 
As an ASO (App Store Optimization) expert proficient, could you write a compelling application description in French for an IOS mobile application, using the following examples as a source of inspiration? Incorporate relevant keywords and ensure your brand name is "FRANCE 24".

Here are the examples:

{user_input}

Please make sure to write a unique and engaging description that highlights the features and benefits of your app, while also incorporating the best practices and strategies from the examples provided.
""",

### 5. Create Keywords and Descriptions Clusters
"aso_keywords_descriptions_clusters" : """
As an advanced SEO and ASO expert, I would like you to analyze the following page from the Apple App Store and extract some key information for me.

Page URL: {user_input}

Category: Actualités

Please provide me with the following:
1. A list of the 50 most commonly used keywords in this category.
2. The top 3 app descriptions in this category, based on their keyword usage, readability, and overall effectiveness.

Your analysis and insights will be very helpful in optimizing our own app's presence in the App Store.
"""


}

### 1. Title Optimization:

# prompt_key = "aso_title_optimization"
# user_input = "actualité en direct, application France 24, contenus exclusifs, journalistes de France 24, articles, reportages, émissions, vidéos, français, anglais, espagnol, arabe, naviguer facilement, multimédias, partage sur les réseaux sociaux, info en continu, 24h/24 et 7j/7, faits-divers, grands événements internationaux, actualités françaises et internationales, rubriques spécialisées, Afrique, Moyen-Orient, Eco-Tech, Découvertes, replay vidéo, journaux sous-titrés, magazines de la rédaction, réseaux sociaux, Facebook, Twitter, Instagram, TikTok, YouTube, Telegram, Soundcloud, donnez-nous une note, laissez-nous un commentaire, France Médias Monde, Radio France Internationale, Monte Carlo Doualiya"

### 2. Subtitle Optimization:

# prompt_key = "aso_subtitle_optimization"
# user_input = "FRANCE 24 - Info et actualités. Suivez l'actualité en direct et en continu en téléchargeant gratuitement l’application France 24."


### 3. Add Keywords
# prompt_key = "aso_add_keywords"
# user_input = "News, Actualités, Information, Journal, Presse, Breaking, Live, Articles, Reportage, Politics, International, Economy, Finance, Culture, Sports, Weather, Local, Global, Headlines, Updates, Stories, Events, World, Media, Daily, Analysis, Insights, Highlights, Coverage, Alerts, Trending, Online, Mobile, Network, Bulletin, Update, Current, TV, Radio, Video, Stream, Reports, Digital, Read, Real-time, Data, Interactive, Subscription, In-depth, Highlights"

### 4. Engaging App Descriptions

# prompt_key = "aso_engaging_app_descriptions"
# user_input = """
# 1. TF1 INFO - LCI: Actualités La Chaine Info
# Découvrez toute l'actualité en direct avec TF1 INFO - LCI. Suivez les dernières nouvelles en France et à l'international, les reportages exclusifs, les analyses et les vidéos. Recevez des alertes pour rester informé en temps réel. L'info en continu, à portée de main.

# 2. Google Actualités
# Google Actualités vous propose une couverture complète et personnalisée des actualités qui vous intéressent. Explorez les articles des plus grandes publications et recevez des alertes sur les sujets de votre choix. Restez informé grâce à des mises à jour en temps réel et à une sélection de sources fiables.

# 3. Le Monde, Live, Actu en direct
# Retrouvez toute l'actualité avec Le Monde. Accédez à des articles en profondeur, des analyses, des vidéos et des photos. Suivez les événements en direct et recevez des notifications sur les sujets qui vous intéressent. Une couverture complète de l'actualité française et internationale, 24h/24.
# """


### 5. Create Keywords and Descriptions Clusters
# prompt_key = "aso_keywords_descriptions_clusters"
# user_input = """
# https://apps.apple.com/fr/charts/iphone/actualit%C3%A9s-apps/6009
# """


# Calling the function with the prompt key and user input
response = openai_chat(prompt_key, user_input)

# Print the response
print(response)

