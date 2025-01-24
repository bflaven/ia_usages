#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_using_faiss python=3.9.13
conda info --envs
source activate ia_using_faiss
conda deactivate


# BURN AFTER READING
source activate ia_using_faiss

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_using_faiss

# BURN AFTER READING
conda env remove -n ia_using_faiss


# install packages with conda
conda install -c conda-forge sentence-transformers
conda install -c pytorch faiss-cpu

# install packages with pip
python -m pip install sentence-transformers
python -m pip install pytorch faiss-cpu
python -m pip install numpy

python -m pip install huggingface_hub==0.25.2


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_video_editing_faiss_compare_keywords/ia_cms

# launch the file in streamlit
streamlit run 006_ia_cms_streamlit.py



"""

import streamlit as st
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

# Set page to full screen
st.set_page_config(layout="wide", page_title="Semantic Keyword Matcher")

# Display package versions
st.info(f"""
Package versions:
- faiss: {faiss.__version__}
- numpy: {np.__version__}
- sentence_transformers: {SentenceTransformer.__version__}
""")

st.title("Semantic Keyword Matcher")

class KeywordMatcher:
    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path
        self.cms_existing_kw = self.load_keywords_from_json()
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def load_keywords_from_json(self) -> List[str]:
        with open(self.json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return [keyword['label'].strip('"') for keyword in data['keywords'] if keyword['label'].strip('"')]

    def get_similar_keywords(self, ia_generated_kw: List[str]) -> List[Tuple[str, float, str]]:
        ia_embeddings = self.model.encode(ia_generated_kw)
        cms_embeddings = self.model.encode(self.cms_existing_kw)

        faiss.normalize_L2(ia_embeddings)
        faiss.normalize_L2(cms_embeddings)

        dimension = ia_embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(cms_embeddings)

        k = len(self.cms_existing_kw)
        distances, indices = index.search(ia_embeddings, k)

        similar_keywords = []
        for i, (dist_row, idx_row) in enumerate(zip(distances, indices)):
            for j, (dist, idx) in enumerate(zip(dist_row, idx_row)):
                similar_keywords.append((self.cms_existing_kw[idx], float(dist), ia_generated_kw[i]))

        seen = {}
        unique_similar_keywords = []
        for kw, sim, orig in similar_keywords:
            if kw not in seen or sim > seen[kw][0]:
                seen[kw] = (sim, orig)
        
        for kw, (sim, orig) in seen.items():
            unique_similar_keywords.append((kw, sim, orig))

        unique_similar_keywords.sort(key=lambda x: x[1], reverse=True)
        return unique_similar_keywords

def main():
    matcher = KeywordMatcher('pt_tags_thema_list_4.json')

    tab1, tab2 = st.tabs(["Search", "Archives"])

    with tab1:
        st.subheader("Enter IA Generated Keywords")
        ia_generated_kw = st.text_area("Enter keywords (one per line)", height=200)
        
        st.markdown("**Example keywords:**")
        example_keywords = [
            "Hélio Almeida", "ministro das Finanças", "Presidente da República",
            "Carlos Vila Nova", "primeiro-ministro", "Patrice Trovoada", "ADI",
            "eleições 2022", "eleições antecipadas", "Tribunal Constitucional",
            "Hélio Vaz de Almeida", "economia", "Universidade Independente de Lisboa",
            "ministro do Plano e Finanças", "MLSTP", "Gabriel Costa", "Banco Central",
            "Jorge Bom Jesus", "Agência Fiduciária de Administração de Projetos", "AFAP"
        ]
        st.code("\n".join(example_keywords))

        if st.button("Find Similar Keywords", type="primary"):
            if ia_generated_kw:
                keywords = [kw.strip() for kw in ia_generated_kw.split("\n") if kw.strip()]
                similar_keywords = matcher.get_similar_keywords(keywords)
                
                st.subheader("Results")
                results_df = pd.DataFrame(similar_keywords, columns=["Keyword", "Similarity", "Original"])
                st.dataframe(results_df)

                reduced_keywords = [kw for kw, sim, _ in similar_keywords if sim >= 0.8]
                st.subheader("Reduced list of most similar keywords (Similarity >= 0.8)")
                st.write(reduced_keywords)
            else:
                st.warning("Please enter some keywords.")

        if st.button("Reset"):
            st.experimental_rerun()

    with tab2:
        st.write("Archive content goes here.")

if __name__ == "__main__":
    main()







    
