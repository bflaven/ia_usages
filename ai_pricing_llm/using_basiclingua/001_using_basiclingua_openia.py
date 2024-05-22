"""
[env]
# Conda Environment
conda create --name llm_integration_api_costs python=3.9.13
conda create --name fmm_fastapi_poc python=3.9.13
conda info --envs
source activate llm_integration_api_costs
source activate fmm_fastapi_poc
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
python -m pip install python-dotenv
python -m pip install openai
pip install openai

conda install -c conda-forge openai
pip install emoji
python -m pip install emoji

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ai_pricing_llm/using_basiclingua/


# LAUNCH the file
python 001_using_basiclingua.py


# source
https://github.com/FareedKhan-dev/basiclingua-LLM-Based-NLP


"""
############## OPENAI LINGUA CLASS ##############
# for api key
import os
from dotenv import load_dotenv

# Import the OpenAI class from the openai module
from openai import OpenAI
# Import the class
from openia_basiclingua import OpenAILingua

### 1. GET API KEY ###
# Load environment variables from the .env file
load_dotenv()

# Access the API key using os.getenv
open_ai_key = os.getenv("OPENAI_API_KEY")
openai_model = OpenAILingua(api_key=open_ai_key)

# 1. Extract Patterns
# User Input containing important information
# user_input = """
# In the bustling metropolis of New Alexandria, Detective Miller was hot on the trail of a notorious hacker known only as "Cipher." A cryptic message intercepted by the cybercrime unit mentioned a meeting at "The Crimson Cafe, 3pm, table 7," and listed two aliases: "Silver Fox" and "Blackbird." Miller knew these were likely the hacker's accomplices. His informant, a nervous young man named Alex Turner, claimed Cipher frequented an online forum under the ShadowHunter1337 and often boasted about their exploits. Turner also provided a burner phone number, 555-987-2104, supposedly used by Cipher to contact their associates. Armed with this information, Miller headed to The Crimson Cafe. He arrived early, taking a seat across from table 7, his eyes scanning the room. At precisely 3pm, two individuals approached the table. One, a woman with silver hair and piercing blue eyes, exuded an air of confidence and cunning. The other, a man clad in black, remained silent and watchful. Miller approached them, flashing his badge. "Excuse me, I'm Detective Miller. I believe you might have information regarding an individual known as Cipher." The woman, her lips curling into a sly smile, replied, "Cipher? Never heard of them."""

# user_input = """
# On s’interrogera longtemps sur le choix, par les démocrates américains, de l’octogénaire Joe Biden face à Donald Trump, de quatre ans seulement son cadet, mais nettement plus pugnace. C’est d’ailleurs moins l’âge de l’actuel locataire de la Maison Blanche qui est en cause que ses dérapages aussi répétés qu’embarrassants. C’est ainsi que le président américain a, en avril, exhorté Benyamin Nétanyahou à ne pas attaquer… Haïfa. Il confondait le grand port du nord d’Israël avec Rafah, la ville du sud de la bande de Gaza, où plus de la moitié de la population de l’enclave palestinienne s’est réfugiée, à la frontière de l’Egypte.

# Peu importe de toute façon, puisque l’homme le plus puissant de la planète n’est même pas arrivé à empêcher l’opération en cours contre Rafah. Et si Joe Biden a attendu sept mois de carnage pour hausser vraiment le ton envers Benyamin Nétanyahou, c’est parce que sa fidélité à Israël est ancrée dans une expérience fondatrice, déjà vieille de plus d’un demi-siècle.

# Le président américain, né en 1942 en Pennsylvanie, a été élevé par ses deux parents catholiques dans un profond respect de l’Etat d’Israël. Elu à 30 ans sénateur démocrate du Delaware, il se rend en Egypte et en Israël, en août 1973, pour son premier voyage à l’étranger en tant que parlementaire. Déçu de n’avoir été reçu que par des officiels de second rang en Egypte, il considère au contraire sa rencontre avec la cheffe du gouvernement israélien, Golda Meir, comme « une des plus marquantes » de sa vie.

# Un « sioniste » fervent
# Joe Biden racontera souvent par la suite comment la première ministre lui avait révélé « l’arme secrète » d’Israël : « Nous n’avons aucun autre endroit où aller. » Golda Meir, parfaitement anglophone du fait de ses années de formation aux Etats-Unis, martelait à l’époque dans les médias américains que la « nation palestinienne » n’existe pas plus que le « peuple palestinien ». Mais la première ministre affirmait également ne pas « pouvoir pardonner aux Palestiniens de [les] forcer à tuer leurs enfants », une citation très reprise aujourd’hui en Israël.

# Le jeune sénateur Biden revient si enthousiasmé de ce séjour en Israël qu’il commence à se déclarer « sioniste », un fervent engagement qu’il a maintes fois réitéré en public, précisant à chaque fois qu’il « n’est pas nécessaire d’être juif pour être sioniste ». Il soutient en juin 1982 le gouvernement de Menahem Begin dans son invasion du Liban, en dépit des très nombreuses victimes civiles. Ce soutien est si exalté que le premier ministre israélien doit lui-même tempérer Joe Biden, en rappelant que tout belligérant est tenu d’épargner les femmes et les enfants. Quatre années plus tard, Joe Biden défend ardemment au Congrès l’aide militaire colossale à Israël : « C’est le meilleur investissement de 3 milliards que nous ayons jamais fait. S’il n’y avait pas d’Israël, les Etats-Unis devraient inventer un Israël pour protéger leurs intérêts dans la région. »"""
# patterns = "phone_numbers, person_names, location_names, time_expressions, aliases, usernames, physical_descriptions"
# openai_entities = openai_model.extract_patterns(user_input, patterns=patterns)
# print("OpenAI Entities:", openai_entities)

# 2. Text Translate
user_input = """As the sunset painted the sky with shades of orange and pink, a gentle breeze rustled the leaves, creating a soothing symphony, while the aroma of freshly brewed coffee filled the cozy cafe."""
openai_translation = openai_model.text_translate(user_input, target_lang="german")
print("OpenAI Translation:", openai_translation)

# 3. Text Replace
# user_input = '''karachi is a very big city in pakistan but what about mumbai and delhi?'''
# replacement_rules = '''all city names with fareed'''
# openai_replacement = openai_model.text_replace(user_input, replacement_rules)
# print("OpenAI Replacement:", openai_replacement)

# 4. NER Detection
# user_input = '''i googled youtube.com'''
# openai_ner = openai_model.detect_ner(user_input)
# print("OpenAI NER:", openai_ner)

# 5. Text Summarization
# user_input = '''Fareed and asad are coming to my house at 5 pm. They are bringing a gift for me. I am very happy to see them. I am going to make a cake and tea for them. I hope they will like it. I am very excited to meet them. I have not seen them for a long time. I hope they will stay for a long time. I have a lot of things to talk to them about. I hope they will like my house. I have decorated it for them. I hope they will like it.'''
# summary_length = 3
# openai_summary = openai_model.text_summarize(user_input, summary_length=summary_length)
# print("OpenAI Summary:", openai_summary)

# 6. Question Answering
# user_input = '''Fareed and asad are coming to my house at 5 pm. They are bringing a gift for me. I am very happy to see them. I am going to make a cake and tea for them. I hope they will like it. I am very excited to meet them. I have not seen them for a long time. I hope they will stay for a long time. I have a lot of things to talk to them about. I hope they will like my house. I have decorated it for them. I hope they will like it.'''
# question = "Who is coming to my house at 5 pm?"
# openai_summary = openai_model.text_qna(user_input, question=question)
# print("OpenAI QNA:", openai_summary)


# 7. Intent Recognition
# user_input = '''Fareed and asad are coming to my house at 5 pm. They are bringing a gift for me. I am very happy to see them. I am going to make a cake and tea for them. I hope they will like it. I am very excited to meet them. I have not seen them for a long time. I hope they will stay for a long time. I have a lot of things to talk to them about. I hope they will like my house. I have decorated it for them. I hope they will like it.'''
# openai_intent = openai_model.text_intent(user_input)
# print("OpenAI Intent:", openai_intent)

# 8. Generate Embeddings
# user_input = '''Fareed'''
# openai_embedd = openai_model.text_embedd(user_input)
# print("OpenAI Embedd:", openai_embedd[:2])

# 9. Spam detection
# user_input = '''he congratulations you have won a lottery of 1000000 dollars. Please provide your bank details to claim the prize.'''
# openai_spam = openai_model.detect_spam(user_input)
# print("OpenAI Spam:", openai_spam)

# 10. Spelling Check
# user_input = '''we willl brange the pizze for u'''
# openai_spellcheck = openai_model.text_spellcheck(user_input)
# print("OpenAI Spellcheck:", openai_spellcheck)


# 11. Semantic Role Labeling
# user_input = '''The quick brown fox and lion jumps over the lazy dog.'''
# openai_srl = openai_model.text_srl(user_input)
# print("OpenAI SRL:", openai_srl)


# 12. Sentiment Analysis
# user_input = '''I like this pizza at all.'''
# openai_sentiment = openai_model.text_sentiment(user_input)
# print("OpenAI Sentiment:", openai_sentiment)

# 13. Topic Modeling
# user_input = '''Fareed and asad are coming to my house at 5 pm. They are bringing a gift for me. I am very happy to see them. I am going to make a cake and tea for them. I hope they will like it. I am very excited to meet them. I have not seen them for a long time. I hope they will stay for a long time. I have a lot of things to talk to them about. I hope they will like my house. I have decorated it for them. I hope they will like it.'''
# openai_sentiment = openai_model.text_topic(user_input)
# print("OpenAI Topic:", openai_sentiment)

# 14. POS Tagging
# user_input = '''Fareed and asad are coming to my house at 5 pm. They are bringing a gift for me. I am very happy to see them. I am going to make a cake and tea for them. I hope they will like it. I am very excited to meet them. I have not seen them for a long time. I hope they will stay for a long time. I have a lot of things to talk to them about. I hope they will like my house. I have decorated it for them. I hope they will like it.'''
# openai_pos = openai_model.detect_pos(user_input)
# print("OpenAI POS:", openai_pos)

# 15. Text Badness
# user_input = '''Fareed ia very bad guy'''
# openai_badwords = openai_model.text_badness(user_input)
# print("OpenAI Badness:", openai_badwords)


# 16. Text Emojis
# user_input = '''Fareed ia very bad guy 😡 but still i like him 😊'''
# openai_emoji = openai_model.text_emojis(user_input)
# print("OpenAI Emojis:", openai_emoji)

# 17. Text Idioms
# user_input = '''Fareed is a bad egg but still i like him because he is a good apple'''
# openai_idioms = openai_model.text_idioms(user_input)
# print("OpenAI Idioms:", openai_idioms)

# 18. Anomaly Detection
# user_input = '''Fareed is a bad egg but still i like him because he is a good apple'''
# openai_anomaly = openai_model.text_anomaly(user_input)
# print("OpenAI Anomaly:", openai_anomaly)

# 19. Text Coreference
# user_input = '''me and amjad are going to the market but he said he will not come'''
# openai_coref = openai_model.text_coreference(user_input)
# print("OpenAI Coreference:", openai_coref)

# 20. Chat with PDF
# 21. OCR