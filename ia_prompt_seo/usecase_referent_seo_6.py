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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_prompt_seo/

# launch the file
python usecase_referent_seo_5.py


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

def openai_chat(user_prompt):

    # Create a chat completion using the OpenAI client
    response = client.chat.completions.create(
        # Set the model to "gpt-3.5-turbo-0125"
        model=model_selected, 
        messages=[{"role": "user", "content": user_prompt}]
    )

    # Response from the chat completion
    answer = response.choices[0].message.content

    # Assuming response and model_selected are defined and have valid values
    if model_selected == "gpt-3.5-turbo":
        input_price = response.usage.prompt_tokens * (0.46 / 1e6)
        output_price = response.usage.completion_tokens * (1.38 / 1e6)
    else:
        if model_selected == "gpt-4-turbo":
            input_price = response.usage.prompt_tokens * (9.18 / 1e6)
            output_price = response.usage.completion_tokens * (27.55 / 1e6)
        else:
            print("Invalid model selected. Please choose between 'gpt-3.5-turbo' and 'gpt-4-turbo'.")

     

    
    # calculate the total price
    total_price = input_price + output_price

    # Return the answer, input price, output price, total price
    # return {
    #     "answer": answer,
    #     "input_price": f"$ {input_price}",
    #     "output_price": f"$ {output_price}",
    #     "total_price": f"$ {total_price}"
    # }

    return {
        "answer": answer,
        "input_price": f"€ {input_price}",
        "output_price": f"€ {output_price}",
        "total_price": f"€ {total_price}"
    }
    
# prompt = """
# Who is Friedrich Nietzsche?
# """


user_input_language = """
French
"""

# user_input_language = """
# Spanish
# """


user_input = """
<p>Un bus a pris feu et une trentaine de personnes ont été légèrement blessés samedi 25 mai lors d'affrontements entre supporters de l'OL et du <a target="_self" href="https://www.france24.com/fr/tag/psg/" class="gtm-add-suggested-tag">PSG</a> à un péage d'autoroute près d'Arras, juste avant la finale de la <a target="_self" href="https://www.france24.com/fr/tag/coupe-de-france/" class="gtm-add-suggested-tag">Coupe de France</a> à Lille, des faits condamnés "avec la plus grande fermeté" par le président <a target="_self" href="https://www.france24.com/fr/tag/emmanuel-macron/" class="gtm-add-suggested-tag">Emmanuel Macron</a>.</p><p>Selon la préfecture du Pas-de-Calais, cette rixe a opposé des supporters des deux équipes qui se rendaient au stade Pierre-Mauroy de Villeneuve d'Ascq aux environs de 18H00 sur l'Autoroute A1, au niveau du péage de Fresnes-lès-Montauban (Pas-de-Calais), à une soixantaine de kilomètres de Lille.</p><p>"Une centaine d'individus sont impliqués et un bus a pris feu", a-t-elle précisé, ajoutant que "18 bus de supporters parisiens ont repris la route vers Lille". "Les supporters lyonnais ont également été écartés", a-t-elle poursuivi.</p><p>"Ce sont des rendez-vous sportifs où il faut avant tout être dans la joie et le sport. Je condamne avec la plus grande fermeté toutes les violences", a déclaré le chef de l'État lors d'une déambulation publique à Tourcoing. "J'espère que les choses se dérouleront le plus normalement possible ce soir", a-t-il ajouté, confirmant qu'il irait au stade.</p><h2>Aucune interpellation                </h2><p>Selon une source policière, les heurts "ont opposé environ une centaine de supporters lyonnais à près de 200 supporters parisiens" et "la barrière de péage (a été) partiellement incendiée".</p><p>Cette source fait également état de six policiers légèrement blessés, un bilan non confirmé par la préfecture du Pas-de-Calais. Aucune personne n'a été interpellée, selon la source policière.</p><p>D'après une source à la gendarmerie, ces violences font suite à "une rencontre inopportune entre des supporters lyonnais et parisiens".</p><p>"Le dispositif de sécurité important mis en place pour le match et notamment les escortes policières pour encadrer les ultras a permis de mettre fin rapidement, malgré des bus dégradés, aux affrontements", a écrit la préfecture du Nord sur X.</p><p>L'autoroute A1 reste coupée dans les deux sens, selon la préfecture du Pas-de-Calais.</p><p>Au Stade Pierre-Mauroy, la finale de la Coupe Gambardella entre Marseille et Nancy, qui se joue en lever de rideau de celle de la Coupe de France, a été interrompue une dizaine de minutes après le jet d'un projectile par des supporters parisiens, déjà présents dans le stade, en direction du gardien de l'OM.</p><p>Les fans de l'OL et du PSG se sont invectivés pendant cette rencontre, a constaté un journaliste de l'AFP.</p><h2>Alcool interdit</h2><p>Durant la journée, les supporters parisiens, mais surtout lyonnais, ont animé les rues du centre-ville de Lille dans une ambiance bon enfant, a constaté un journaliste de l'AFP. Un impressionnant dispositif policier est déployé dans la ville.</p><p>Selon la préfecture du Pas-de-Calais, 1 000 policiers et gendarmes ont été mobilisés pour sécuriser la rencontre et 1 000 autres pour gérer la sécurité dans le stade.</p><p>Appelant à "la responsabilité collective et individuelle des supporters", la préfecture du Nord avait mis en place plusieurs mesures administratives dans le cadre de cette rencontre classée à très haut risque.</p><p>Les supporters de l'OL et du PSG ont ainsi l'interdiction de se déplacer "en dehors des espaces qui leur sont réservés" et ne peuvent se croiser près de l'enceinte.</p><p>La préfecture avait également demandé aux supporters de chaque équipe d'utiliser chacun une ligne de métro différente, avec des arrêts de métro distincts, pour se rendre au stade et d'éviter au maximum les risques de débordements. </p><p>Autre interdiction : la consommation sur la voie publique et les terrasses de Lezennes, Lille et Villeneuve d'Ascq d'alcool "dans un contenant en verre ou en métal" jusqu'à dimanche 4 H.</p><p><em>Avec Reuters et AFP</em></p>
"""

###### EXTRACT FROM 003_prompts_seo_bestof.md ######

# seo_manage_title

# PERSONAL
# prompt_template = f'''
# As an {user_input_language} SEO expert, can you generate 10 compelling headline ideas for the post about {user_input} in {user_input_language}?
# '''

# OPENAI
# prompt_template = f'''
# As an SEO expert proficient in {user_input_language}, could you create 10 compelling headline ideas for a post about {user_input} in {user_input_language}?
# '''

# MISTRAL
# prompt_template = f'''
# Utilizing your expertise in {user_input_language} SEO, could you please generate 10 engaging and SEO-friendly headline suggestions for a blog post centered around the topic of {user_input}?
# '''

# seo_manage_url

# PERSONAL
# prompt_template = f'''
# As an {user_input_language} SEO expert, can you generate 10 compelling url ideas for the post about {user_input} in {user_input_language}?
# '''

# OPENAI
prompt_template = f'''
As an SEO expert proficient in {user_input_language}, could you create 10 compelling URL ideas for a post about {user_input} in {user_input_language}?
'''


# MISTRAL
# prompt_template = f'''
# Using your knowledge of {user_input_language} SEO best practices, can you please generate 10 concise and descriptive URL ideas for a post on a topic of {user_input}?
# '''

# seo_manage_meta_description

# PERSONAL
# prompt_template = f'''
# As an {user_input_language} SEO expert, write a meta description of 150-160 characters for a post about {user_input} in {user_input_language}?
# '''

# OPENAI
# prompt_template = f'''
# As an SEO expert proficient in {user_input_language}, please write a meta description of 150-160 characters for a post about {user_input} in {user_input_language}.
# '''

# MISTRAL
# prompt_template = f'''
# Using your expertise in {user_input_language} SEO, please craft a compelling and informative meta description of 150-160 characters for a blog post on the topic of {user_input}. The meta description should accurately summarize the post's content and entice users to click through to the post.
# '''


# seo_manage_backlink_internal_links
# No prompt available for PERSONAL, OPENAI, MISTRAL

# seo_manage_label_internal_link

# PERSONAL
# prompt_template = f'''
# As a {user_input_language} SEO expert, generate 10 semantic editorial proposals for link labels based on the post about {user_input} in {user_input_language}?
# '''

# OPENAI
# prompt_template = f'''
# As a {user_input_language} SEO expert, please generate 10 semantic editorial proposals for link labels based on a post about {user_input} in {user_input_language}.
# '''


# MISTRAL
# prompt_template = f'''
# Utilizing your expertise in {user_input_language} SEO, please generate 10 semantically relevant and engaging editorial proposals for link labels that could be used within a blog post on the topic of {user_input}. These link labels should accurately reflect the content of the linked-to page and provide value to the reader.
# '''


# seo_manage_ner_tags

# PERSONAL
# prompt_template = f'''
# Given the input in {user_input_language} text:user input: {user_input} perform NER detection on it. NER TAGS: FAC;  CARDINAL;  NUMBER;  DEMONYM;  QUANTITY;  TITLE;  PHONE_NUMBER;  NATIONAL;  JOB;  PERSON;  LOC;  NORP;  TIME;  CITY;  EMAIL;  GPE;  LANGUAGE;  PRODUCT;  ZIP_CODE;  ADDRESS;  MONEY;  ORDINAL;  DATE;  EVENT;  CRIMINAL_CHARGE;  STATE_OR_PROVINCE;  RELIGION;  DURATION;  URL;  WORK_OF_ART;  PERCENT;  CAUSE_OF_DEATH;  COUNTRY;  ORG;  LAW;  NAME;  COUNTRY;  RELIGION;  TIME answer must be in the format tag:value
# '''

# OPENAI
# prompt_template = f'''
# Given the input in {user_input_language} text:user input: {user_input} perform NER detection on it. NER TAGS: FAC;  CARDINAL;  NUMBER;  DEMONYM;  QUANTITY;  TITLE;  PHONE_NUMBER;  NATIONAL;  JOB;  PERSON;  LOC;  NORP;  TIME;  CITY;  EMAIL;  GPE;  LANGUAGE;  PRODUCT;  ZIP_CODE;  ADDRESS;  MONEY;  ORDINAL;  DATE;  EVENT;  CRIMINAL_CHARGE;  STATE_OR_PROVINCE;  RELIGION;  DURATION;  URL;  WORK_OF_ART;  PERCENT;  CAUSE_OF_DEATH;  COUNTRY;  ORG;  LAW;  NAME;  COUNTRY;  RELIGION;  TIME answer must be in the format tag:value
# '''

# MISTRAL
# prompt_template = f'''
# Please perform Named Entity Recognition (NER) on the following {user_input_language} text: "{user_input}". Identify and label the entities in the text using the following NER tags: FAC, CARDINAL, NUMBER, DEMONYM, QUANTITY, TITLE, PHONE_NUMBER, NATIONAL, JOB, PERSON, LOC, NORP, TIME, CITY, EMAIL, GPE, LANGUAGE, PRODUCT, ZIP_CODE, ADDRESS, MONEY, ORDINAL, DATE, EVENT, CRIMINAL_CHARGE, STATE_OR_PROVINCE, RELIGION, DURATION, URL, WORK_OF_ART, PERCENT, CAUSE_OF_DEATH, COUNTRY, ORG, LAW, NAME.

# Please format your answer as a list of tuples, where each tuple contains the NER tag and the corresponding value from the text. For example: [("PERSON", "John Smith"), ("LOC", "New York City")].
# '''


# seo_manage_reverse_linking
# No prompt available for PERSONAL, OPENAI, MISTRAL

# seo_manage_html_subtitles

# PERSONAL
# prompt_template = f'''
# As a {user_input_language} SEO expert, can you generate an HTML code structure using `<H1>`, `<H2>`, and `<H3>` tags for the post content provided here: {user_input}. Please ensure that the code adheres to best SEO practices for optimal content structure, readability, and search engine optimization.
# '''

# OPENAI
# prompt_template = f'''
# As an SEO expert proficient in {user_input_language}, please generate an HTML code structure for the post content: "{user_input}". Use <H1>, <H2>, and <H3> tags to organize the content effectively. Ensure the structure follows best SEO practices for optimal readability and search engine optimization.
# '''


# MISTRAL
# prompt_template = f'''
# Utilizing your expertise in {user_input_language} SEO, please generate an HTML code structure for the following post content: "{user_input}". The code should include <H1>, <H2>, and <H3> tags to create a well-structured and easily-readable hierarchy of content.

# Please ensure that the code adheres to best SEO practices for optimal content structure, readability, and search engine optimization. This includes using descriptive and keyword-rich headings, limiting the use of <H1> tags to one per page, and ensuring that the content within each heading accurately reflects the information that follows.

# Additionally, please include any relevant <meta> tags, such as <meta name="description" content="">, to further optimize the post for search engines.
# '''


# seo_manage_image_optimization
# No prompt available for PERSONAL, OPENAI, MISTRAL


# seo_manage_image_alt_attribute

# PERSONAL
# prompt_template = f'''
# As a {user_input_language} SEO expert, can you generate 10 alt messages in {user_input_language} for potential images illustrating the main topic for the post: {user_input}. You can provide editorial proposals in {user_input_language} with synonyms or variations according to the main keyword of the post. Each alt message cannot exceed more than 125 characters.
# '''

# OPENAI
# prompt_template = f'''
# As an SEO expert proficient in {user_input_language}, please generate 10 alt text descriptions in {user_input_language} for images related to the main topic of the post: "{user_input}". Each alt text should incorporate synonyms or variations of the main keyword and must not exceed 125 characters.
# '''


# MISTRAL
# prompt_template = f'''
# Utilizing your expertise in {user_input_language} SEO, please generate 10 descriptive and keyword-rich alt messages in {user_input_language} for potential images that could be used to illustrate the main topic of the following post: "{user_input}".

# To provide a diverse set of options, please feel free to include synonyms or variations of the main keyword in your alt messages. However, please ensure that each alt message accurately and concisely describes the content of the corresponding image.

# Please also ensure that each alt message does not exceed 125 characters in length, as this is the maximum length that is typically displayed by search engines and screen readers.
# '''


# Calling our function with the prompt
openai_chat(prompt_template)

####### OUTPUT #######
print(openai_chat(prompt_template))


