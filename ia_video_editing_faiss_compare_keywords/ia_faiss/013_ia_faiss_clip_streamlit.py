#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_using_faiss python=3.9.13
conda info --envs
source activate ia_using_faiss
source activate clip_env
conda deactivate


# BURN AFTER READING
source activate ia_using_faiss

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_using_faiss
conda env remove -n ia_using_clip
conda env remove -n clip_env


# install packages with conda
conda install pytorch torchvision -c pytorch
pip install git+https://github.com/openai/CLIP.git
conda install ftfy regex tqdm


conda create -n clip_env python=3.8
conda activate clip_env
conda install pytorch torchvision -c pytorch
pip install git+https://github.com/openai/CLIP.git

conda install --yes -c pytorch pytorch=1.7.1 torchvision cudatoolkit=11.0
conda install --yes -c pytorch torchvision cudatoolkit
pip install ftfy regex tqdm
pip install git+https://github.com/openai/CLIP.git

pip install open_clip_torch
pip install torch torchvision torchaudio

conda install pytorch torchvision torchaudio cpuonly -c pytorch

# install good
python -m pip install open-clip-torch


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_video_editing_faiss_compare_keywords/ia_faiss


# launch the file in streamlit
streamlit run 013_ia_faiss_clip_streamlit.py

"""

import streamlit as st
import open_clip
import torch
from PIL import Image
import faiss
import numpy as np
import os

class ImageSearchApp:
    def __init__(self):
        st.set_page_config(page_title="VisualQuest", layout="wide", page_icon="🔍")
        st.title("VisualQuest: AI-Powered Image Search 🔍")
        # Add app icon
        # st.image("https://img.icons8.com/color/48/000000/search--v1.png", width=48)


        # Display package versions
        st.info(f"open_clip version: {open_clip.__version__}\nfaiss version: {faiss.__version__}")
        
        # Initialize model and tokenizer
        self.model, _, self.preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
        self.model.eval()
        self.tokenizer = open_clip.get_tokenizer('ViT-B-32')
        
        # Set device
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = self.model.to(self.device)
        
        # Initialize image paths and index
        self.image_paths = self.get_image_paths()
        self.index = None
        
        # Create tabs
        search_tab, archive_tab = st.tabs(["Search", "Search archives"])
        
        with search_tab:
            self.search_tab()
        
        with archive_tab:
            self.archive_tab()
        
    def get_image_paths(self):
        # Retrieve all .jpg and .png files from the 'pictures/' and 'known_faces/' directories
        image_paths = []
        for directory in ["pictures", "known_faces"]:
            image_paths.extend([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith((".jpg", ".png"))])
        return image_paths

    def encode_images(self):
        image_features = []
        for path in self.image_paths:
            try:
                image = Image.open(path).convert("RGB")
                image_input = self.preprocess(image).unsqueeze(0).to(self.device)
                with torch.no_grad():
                    features = self.model.encode_image(image_input)
                    features /= features.norm(dim=-1, keepdim=True)
                image_features.append(features.cpu().numpy())
            except Exception as e:
                st.error(f"Error processing {path}: {str(e)}")
        return np.concatenate(image_features)

    def create_index(self, image_features):
        dimension = image_features.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(image_features.astype(np.float32))
        return index

    def search_images(self, query, k=5):
        with torch.no_grad():
            text_features = self.model.encode_text(self.tokenizer([query]).to(self.device))
            text_features /= text_features.norm(dim=-1, keepdim=True)
        D, I = self.index.search(text_features.cpu().numpy(), k)
        return D[0], I[0]

    def search_tab(self):
        if self.index is None:
            with st.spinner("Encoding images..."):
                image_features = self.encode_images()
            with st.spinner("Creating Faiss index..."):
                self.index = self.create_index(image_features)
            st.success("Image encoding and indexing complete.")
            st.info("You can start using the search in natural language.")

        query = st.text_input("Enter your search query:")
        if st.button("Launch", type="primary"):
            if query:
                distances, indices = self.search_images(query)
                self.display_results(query, distances, indices)
            else:
                st.warning("Please enter a search query.")
        

    def archive_tab(self):
        archived_queries = [            
            "A badger in a field", # (EN)
            "Un tejón en un campo", # (ES)
            "Un blaireau dans un champs", # (FR)
            "Барсук в поле", # (RU)
            "Um texugo em um campo", # (BR)
            "A snake in a tree",
            "A man sits in a tent in the desert",
            "A zebra's muzzle with blue sky around it",
            "A chameleon on a broken branch",
            "Lula, the Brazil's President shaking hand to another person",
            "Prabowo Subianto, the Indonesia's President shaking hand to another person",
            "Putin shaking hand to another person",
            "Trump shaking hand to another person",
            "Modi shaking hand to another person",
            "Mike Johnson shaking hand to another person",
            "Vice President Kamala Harris shakes hands",
            "Mohamar Ouda ex-prisoner in Syria",
            "Edmundo González, venezuelan opposition leader",
            "2 elephants in the savannah",
            "Find me a picture for President Prabowo Subianto?",
            # foreign languages queries
            "Lula, le président du Brésil, serre la main d'une autre personne",
            "Лула, президент Бразилии",
            "Lula, o presidente do Brasil",
            "Lula, tổng thống Brazil",
            "لولا، رئیس جمهور برزیل",
            "Macron serre la main d'une autre personne",
            "Un serpent dans un arbre",
            "ancien prisonnier en Syrie",
            "Looking for J. D. Vance",
            "¿Dónde está el señor Musk?",
            "¿Dónde está el señor Trump?"
        ]


        selected_query = st.selectbox("Select an archived query:", archived_queries)
        if st.button("Search", type="primary"):
            distances, indices = self.search_images(selected_query)
            self.display_results(selected_query, distances, indices)
        
        

    def display_results(self, query, distances, indices):
        st.write(f"Top 5 images for query '{query}':")
        for i, (distance, index) in enumerate(zip(distances, indices)):
            st.write(f"{i+1}. {self.image_paths[index]} (similarity: {distance:.4f})")
            if i == 0:
                st.image(self.image_paths[index], caption=f"Best match: {self.image_paths[index]}")
        # add reload button
        if st.button("Reload", key="reload_archive"):
            # Update
            # `st.experimental_rerun` will be removed after 2024-04-01.
            # st.experimental_rerun()
            st.rerun

if __name__ == "__main__":
    # Suppress the TypedStorage deprecation warning
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="torch._utils")
    
    ImageSearchApp()






    
