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
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_video_editing_faiss_compare_keywords/ia_faiss/


# launch the file
python 012_ia_faiss_clip.py


"""

import open_clip
import torch
from PIL import Image
import faiss
import numpy as np

print('\n--- open_clip version ')
print(open_clip.__version__)
print()
print('\n--- faiss version ')
print(faiss.__version__)
print()

# Initialize the model and tokenizer
model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
model.eval()
tokenizer = open_clip.get_tokenizer('ViT-B-32')

# Sample image paths (replace with your own images)
image_paths = [
    "pictures/animal_badger.jpg", 
    "pictures/animal_bear.jpg", 
    "pictures/animal_bird.jpg", 
    "pictures/animal_camel.jpg",
    "pictures/animal_dog.png", 
    "pictures/animal_elephants.jpg", 
    "pictures/animal_fawn_deer.jpg",
    "pictures/animal_fish_blobfish.jpg", 
    "pictures/animal_hyena.jpg", 
    "pictures/animal_nature_bird_flying_red.jpg",
    "pictures/animal_pangolin.jpg", 
    "pictures/animal_red_panda.jpg", 
    "pictures/animal_reptile_chamaeleo.jpg",
    "pictures/animal_rhino.jpg", 
    "pictures/animal_snake.jpg", 
    "pictures/animal_squirrel.jpg",
    "pictures/animal_tapir_malaisie.jpg", 
    "pictures/animal_tiger.jpg", 
    "pictures/animal_zebra.jpg",
    "pictures/source_meta_image_89b37ba_636575492-2021-10-o-touron-lithium-hd-014.jpg",
    "pictures/brazil_indonesia_presidents.png",
    "pictures/Prime-Minister-Narendra-Modi_1687153732144_1687153732409.jpg",
    "pictures/putin_obama_78882139_179597572-1587096938.jpg",
    "pictures/trump-handshake-1.jpg",
    "pictures/kamala_en_20250107_142604_142726_cs.jpg",
    "pictures/syria_prisoner_img_9135.jpg",
    "pictures/edmundo_gonzalez_ap25006631909879.jpg",
    "pictures/elon-musk-donald-trump-jd-vance.jpg",
    # known_faces
    "known_faces/gonzalez.jpg",
    "known_faces/harris.jpg",
    "known_faces/lula.jpg",
    "known_faces/macron.jpg",
    "known_faces/modi.jpg",
    "known_faces/musk.jpg",
    "known_faces/obama.jpg",
    "known_faces/putin.jpg",
    "known_faces/subianto.jpg",
    "known_faces/trump.jpg",
    "known_faces/vance.jpg",

]

# Determine the device (CUDA if available, otherwise CPU)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = model.to(device)

# Function to encode images
def encode_images(image_paths):
    image_features = []
    for path in image_paths:
        try:
            image = Image.open(path).convert("RGB")
            image_input = preprocess(image).unsqueeze(0).to(device)
            with torch.no_grad():
                features = model.encode_image(image_input)
                features /= features.norm(dim=-1, keepdim=True)
            image_features.append(features.cpu().float().numpy())
        except Exception as e:
            print(f"Error processing {path}: {str(e)}")
    return np.concatenate(image_features)

# Encode all images
print("Encoding images...")
image_features = encode_images(image_paths)

# Create Faiss index
print("Creating Faiss index...")
dimension = image_features.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(image_features.astype(np.float32))

# Define the query
# query = "A snake in a tree"
# query = "A man sits in a tent in the desert"
# query = "A zebra's muzzle with blue sky around it"
# query = "A chameleon on a broken branch"

# File photo of Brazil's President Luiz Inacio Lula da Silva (L) with Indonesia's President Prabowo Subianto in Rio de Janeiro, Brazil, on November 18, 2024. © Ricardo Stuckert, AFP

# query = "Lula, the Brazil's President shaking hand to another person"
# query = "Prabowo Subianto, the Indonesia's President shaking hand to another person"
# query = "Putin shaking hand to another person"
# query = "Trump shaking hand to another person"
# query = "Modi shaking hand to another person"
# query = "Mike Johnson shaking hand to another person"
# query = "Vice President Kamala Harris shakes hands"
# query = "Mohamar Ouda ex-prisoner in Syria"
# query = "Edmundo González, venezuelan opposition leader"

# query = "2 elephants in the savannah"
# 
# # other languages
# query = "Lula, le président du Brésil, serre la main d'une autre personne"
# query = "Лула, президент Бразилии"
# query = "Lula, o presidente do Brasil"
# query = "Lula, tổng thống Brazil"
# query = "لولا، رئیس جمهور برزیل"
# query = "Macron serre la main d'une autre personne"
# query = "Un serpent dans un arbre"
# query = "ancien prisonnier en Syrie"

# query = "Looking for J. D. Vance"
# query = "¿Dónde está el señor Musk?"
# query = "¿Dónde está el señor Trump?"
query = "Find me a picture for President Prabowo Subianto?"


# Vice President Kamala Harris shakes hands with House Speaker Mike Johnson, as a joint session of Congress convenes to certify President-elect Donald Trump's election victory on January 6, 2025, at the U.S. Capitol in Washington.
# kamala_en_20250107_142604_142726_cs.jpg

# Mohamar Ouda a été emprisonné et torturé durant sept ans. Yarmouk, le 4 janvier 2025.
# syria_prisoner_img_9135.jpg

# El líder opositor venezolano Edmundo González, en el centro, habla con periodistas en la Casa Blanca, el lunes 6 de enero de 2025, en Washington.
# edmundo_gonzalez_ap25006631909879.jpg

# Encode the query
print(f"Encoding query: '{query}'")
with torch.no_grad():
    text_features = model.encode_text(tokenizer([query]).to(device))
    text_features /= text_features.norm(dim=-1, keepdim=True)

# Search the index
k = 5  # Number of top results to retrieve
print(f"Searching for top {k} matches...")
D, I = index.search(text_features.cpu().float().numpy(), k)

# Print results
print(f"\nTop {k} images for query '{query}':")
for i in range(k):
    print(f"{i+1}. {image_paths[I[0][i]]} (similarity: {D[0][i]:.4f})")









    
