#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_spacy_llm python=3.9.13
conda info --envs
source activate ia_spacy_llm
conda deactivate


# BURN AFTER READING
source activate ia_spacy_llm

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_spacy_llm

# BURN AFTER READING
conda env remove -n ia_spacy_llm


# other libraries
python -m pip install spacy 
python -m pip install spacy-llm 
python -m pip install scikit-learn
python -m pip install python-dotenv
python -m pip install langchain-openai



# spacy
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
python -m spacy validate

# other
python -m pip install -U sentence-transformers

# ollama
https://pypi.org/project/ollama/
python -m pip install ollama

# streamlit
python -m pip install streamlit


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_spacy_llm/


# launch the file
streamlit run 024_ia_ollama_streamlit.py

# source
https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
https://medium.com/@rahultiwari065/unlocking-the-power-of-sentence-embeddings-with-all-minilm-l6-v2-7d6589a5f0aa


https://docs.streamlit.io/develop/api-reference



# EXAMPLES

# EXAMPLE_1
title: Kylian Mbappé left out of France squad for Israel and Italy games
keywords: France, Kylian Mbappé, football, Real Madrid, UEFA Nations League
content: Struggling to make an impact at Real Madrid, star striker Kylian Mbappé has been left out of the France squad for their upcoming matches against Israel and Italy for the UEFA Nations League.


# EXAMPLE_2
title: Ukrainian defences in Donbas risk getting steamrolled by Russian advance
keywords: Ukraine war analysis, Ukraine, Russia, Donbas, Donetsk
content: As Russian troops chart a steady advance in east Ukraine, worn-down Ukrainian forces are struggling to plug holes in their front-line defences. At stake is the "fortress" town of Pokrovsk, a transport and logistics hub that could give Russia a clear pathway to advance in the Donetsk region and beyond.



# EXAMPLE_3
title: Iran arrests female student who stripped to protest dress code
keywords: Iran, women, women's rights, Mahsa Amini, Afghanistan, Middle East, protest
content: Iranian authorities on Saturday arrested a female student who staged a solo protest by stripping to her underwear in public. Reports indicate the action aimed to highlight the oppressive enforcement of Iran's dress code, which mandates women wear a headscarf and loose-fitting clothing in public.

# EXAMPLE_4 (french for sanitize)
title: 
"Les garde-fous ont disparu" : l'UE se prépare face à l'hypothèse d'une victoire de Trump

keywords: 
Union européenne, Pour aller plus loin, États-Unis, Présidentielle américaine, USA 2024, Donald Trump, Décryptage, l'été dernier

content:
Lors de son mandat à la Maison Blanche, Donald Trump avait retiré les États-Unis de plusieurs accords internationaux et agences de l'ONU, menaçant même de quitter l'Otan. À l'époque, des hauts fonctionnaires de son équipe agissaient comme "garde-fous" et l'Europe n'était pas en proie à un conflit sur son territoire. Aujourd'hui, face à la possibilité d'un retour au pouvoir du milliardaire, l'Europe se prépare activement à se protéger d'une nouvelle présidence du républicain.

# EXAMPLE_5 (portuguese, sanitize)

title:
Associação de Escritores Moçambicanos apela à criação de um governo de inclusão

keywords: 
Eleições gerais Moçambique 2024, Daniel Chapo, Venâncio Mondlane

content:
A Associação dos Escritores Moçambicanos (AEMO) propõe a criação de um governo de inclusão para acabar com a violência pós-eleitoral em Moçambique. Para o efeito, a agremiação defende a realização de um encontro urgente entre Daniel Chapo e Venâncio Mondlane, os dois candidatos mais votados nas eleições gerais de 09 de Outubro, segundo os resultados anunciados pela Comissão Nacional de Eleições.

# EXAMPLE_6 (russian, sanitize)

title:
В соборе Парижской Богоматери установят три новых колокола

keywords: 
Франция,Культура, Париж, Нотр-Дам де Пари

content:
В четверг, 8 ноября, в соборе Парижской Богоматери будут установлены три новых колокола, в том числе колокол, в который на Парижской олимпиаде 2024 спортсмены звонили после победы. Через месяц колокола на кафедральном соборое французской столицы начнут звонить ежедневно, по нескольку раз в день.


# EXAMPLE_6 (spanish, sanitize)
title:
Valencia manifiesta su hartazgo contra la gestión política del diluvio mortal


keywords: 
España, Catástrofes naturales, catástrofes, Ecología, Pedro Sánchez

content:
Varios miles de personas se manifiestan en Valencia y otras ciudades españolas contra la gestión política del diluvio del 29 de octubre y sus catastróficas consecuencias, con más de 200 muertos. Bajo el lema "Mazón, dimisión", las manifestaciones han exigido la renuncia de Carlos Mazón, presidente del Gobierno regional, aunque el enfado también afecta al presidente Sánchez por inacción.

# EXAMPLE_7 (romanian, sanitize)
title:
Elena Lasconi, solicitări pentru SRI şi ANCOM, pentru a clarifica dacă alegerile sunt amenințate de „tacticile ruseşti”

keywords: 
Elena Lasconi, Politică

content:
Elena Lasconi, candidata USR la alegerile prezidenţiale, a solicitat, sâmbătă, instituţiilor statului, în special SRI şi ANCOM, să clarifice dacă există dovezi că alegerile din acest an sunt ameninţate de reţelele de manipulare şi dezinformare, potrivit News.ro. Ea a cerut să fie dezvăluite și motivele pentru care George Simion i-a fost interzis accesul în Republica Moldova şi Ucraina.

# EXAMPLE_8 (persian, sanitize)
title:
آغاز خاموشی‌های برنامه‌ریزی شده در سراسر ایران به دلیل کمبود سوخت نیروگاه‌ها برای تولید برق

keywords: 
ایران, سوخت, برق, انرژی, گاز, مسعود پزشکیان


content:
رسانه‌های رسمی ایران گزارش دادند که با توجه به کمبود سوخت برای تولید برق نیروگاه‌ها در این کشور و اطلاعیه شورای اطلاع‌رسانی دولت مبنی بر اعمال خاموشی منظم به‌جای مازوت‌سوزی و آلودگی هوا، از روز یکشنبه ۲۰ آبان، «خاموشی‌های برنامه‌ریزی‌ شده» در سراسر ایران اعمال خواهد شد.


# EXAMPLE_9 (vietnamese, sanitize)
title:
Chiến lược của Zelensky để thuyết phục Trump không bỏ rơi Ukraina

content:
Trong suốt quá trình vận động tranh cử tổng thống Mỹ, ông Donald Trump nhắc đi nhắc lại là sẽ chấm dứt chiến tranh Ukraina « trong vòng 24 giờ » để Mỹ ngừng viện trợ quân sự cho Kiev. Chính quyền tổng thống Volodymyr Zelensky chưa hẳn đã thất vọng khi thấy tổng thống thứ 47 của Mỹ là người chủ trương « Nước Mỹ trên hết », mà dường như ngay từ tháng 09/2024, Kiev đã chuẩn bị chiến lược thuyết phục ông Trump không bỏ rơi Ukraina.

keywords: 
Phân tích, Ukraina, Hoa Kỳ, Volodymyr Zelensky, Donald Trump, Nga, Chiến tranh, Viện trợ



"""

import ollama
from datetime import datetime
import os
import streamlit as st

def get_llm_response(language, title_model, keywords_model, content_source):
    prompt = f"""
Given the title model, keywords model, and content source, your task is to generate 10 similar title proposals in {language} and 5 unique keyword combinations in {language}. The output must be in the language specified: {language}.

Title Model: {title_model}

Keywords Model: {keywords_model}

Content Source: {content_source}

Please return the output in the following format but with values in {language}:

title_proposals = [
    "Proposal 1",
    "Proposal 2",
    ...
    "Proposal 10"
]

keywords_combinations = [
    ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    ...
    ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
]

Ensure that each keyword in the keyword combinations is unique and enclosed in quotes.
"""


    # response = ollama.generate(prompt)
    response = ollama.chat(model='mistral:latest', messages=[{
                'role': 'user',
                'content': prompt,
                },
      ])
    return response

# Define a title with an icon
st.set_page_config(page_title="LLM Prompt Generator", page_icon=":guardsman:", layout="wide")



def main():
    st.title("LLM Prompt Generator")

    language = st.text_input("Enter the destination language", placeholder="Enter a destination language for the IAG")
    st.caption("Enter a language written in english e.g \"English\" or \"Spanish\" or \"Russian\" or \"Portuguese\" or \"French\"... etc ")

    title_model = st.text_input("Enter the title model", placeholder="Enter a title model for a post")
    st.caption("Enter a title model e.g \"German opposition demands confidence vote next week as Scholz's coalition crumbles\" ")

    keywords_model = st.text_input("Enter the keywords model", placeholder="Enter keywords model for a post")
    st.caption('Enter keywords model e.g "Germany", "Olaf Scholz", "CDU", "Ukraine"')

    content_source = st.text_area("Enter the content source", placeholder="Enter a content source model for a post")
    st.caption("Enter a content source e.g \"Germany's Christian Democratic Union (CDU) opposition party has called on Chancellor Olaf Scholz to seek a vote of confidence next week after the ruling coalition fell apart Wednesday night with Scholz's shock dismissal of his finance minister. Scholz had promised to put his government to a confidence vote by January 15, 2025.\"")

    if st.button("Send to LLM", type="primary"):
        response = get_llm_response(language, title_model, keywords_model, content_source)

        # Get the current date and time
        now = datetime.now()

        # Format the date and time as a string
        datetime_str = now.strftime("%Y_%m_%d_%H_%M_%S")

        # Create the filename
        filename = f"ia_ollama_{language}_{datetime_str}.py"

        # Create the directory if it doesn't exist
        os.makedirs("ollama_output", exist_ok=True)

        # Write the response to the file in the directory
        with open(os.path.join("ollama_output", filename), "w") as f:
            f.write(response['message']['content'])

        st.success(f"See the result in the python file {filename} in the directory ollama_output.", icon="✅")

if __name__ == "__main__":
    main()

