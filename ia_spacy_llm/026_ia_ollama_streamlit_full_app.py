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
streamlit run 026_ia_ollama_streamlit_full_app.py

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

"""

import ollama
from datetime import datetime
import os
import streamlit as st

# Define a title with an icon
st.set_page_config(page_title="My App", page_icon=":guardsman:", layout="wide")



def get_llm_response(title_model, keywords_model, content_source):
    prompt = f"""
    Make 10 proposals for a similar title based on this title_model, 10 keywords based on on the keywords_model and this content_source.

    - title_model
    ```text
    {title_model}
    ```

    - keywords_model
    ```text
    {keywords_model}
    ```

    ```text
    {content_source}
    ```

    Just return the "Title Proposals" in a python object named title_proposals = [] without number and the "Keywords" in a python object named keywords_combinations = [] without number but with each keyword between quotes.
    """

    # response = ollama.generate(prompt)
    response = ollama.chat(model='mistral:latest', messages=[{
                'role': 'user',
                'content': prompt,
                },
      ])
    return response

def main():
    # title
    st.title("LLM Prompt Generator")


    # Create three tabs
    tab1, tab2, tab3 = st.tabs(["Send to LLM", "Similarity score", "Explanations"])


    # Tab 1: Send to LLM
    with tab1:
                title_model = st.text_input("Enter the title model", placeholder="Enter a title model for a post")
                st.caption("Enter a title model e.g \"German opposition demands confidence vote next week as Scholz's coalition crumbles\" ")

                keywords_model = st.text_input("Enter the keywords model", placeholder="Enter keywords model for a post")
                st.caption('Enter keywords model e.g "Germany", "Olaf Scholz", "CDU", "Ukraine"')

                content_source = st.text_area("Enter the content source", placeholder="Enter a content source model for a post")
                st.caption("Enter a content source e.g \"Germany's Christian Democratic Union (CDU) opposition party has called on Chancellor Olaf Scholz to seek a vote of confidence next week after the ruling coalition fell apart Wednesday night with Scholz's shock dismissal of his finance minister. Scholz had promised to put his government to a confidence vote by January 15, 2025.\"")

                if st.button("Send to LLM", type="primary"):
                    response = get_llm_response(title_model, keywords_model, content_source)

                    # Get the current date and time
                    now = datetime.now()

                    # Format the date and time as a string
                    datetime_str = now.strftime("%Y-%m-%d_%H-%M-%S")

                    # Create the filename
                    filename = f"ia_ollama_{datetime_str}.py"

                    # Create the directory if it doesn't exist
                    os.makedirs("ollama_output", exist_ok=True)

                    # Write the response to the file in the directory
                    with open(os.path.join("ollama_output", filename), "w") as f:
                        f.write(response['message']['content'])

                    st.success(f"See the result in the python file {filename} in the directory ollama_output.", icon="✅")

    # Tab 2: Similarity score
    with tab2:
        st.code("Similarity score")

    # Tab 3: Explanations
    with tab3:
        st.code("Explanations")


if __name__ == "__main__":
    main()

