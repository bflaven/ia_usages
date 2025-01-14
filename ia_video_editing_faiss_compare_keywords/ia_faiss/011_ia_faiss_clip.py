#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
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


# BURN AFTER READING
conda env remove -n ia_using_clip


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
python 011_ia_faiss_clip.py

# source
https://github.com/bflaven/ia_usages/tree/921276b19f5098e990588a7061511ae80af7eb7a/ia_spacy_llm



"""

import open_clip
import torch
from PIL import Image
import faiss
import numpy as np

print('\n--- open_clip ')
print(open_clip.__version__)
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
    "pictures/source_meta_image_89b37ba_636575492-2021-10-o-touron-lithium-hd-014.jpg"
]

# Determine the device (CUDA if available, otherwise CPU)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = model.to(device)

# Function to encode images
def encode_images(image_paths):
    image_features = []
    for path in image_paths:
        image = Image.open(path).convert("RGB")
        image_input = preprocess(image).unsqueeze(0).to(device)
        with torch.no_grad(), torch.amp.autocast(device):
            features = model.encode_image(image_input)
            features /= features.norm(dim=-1, keepdim=True)
        image_features.append(features.cpu().numpy())
    return np.concatenate(image_features)

# Encode all images
image_features = encode_images(image_paths)

# Create Faiss index
dimension = image_features.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(image_features)

# Define the query
query = "A snake in a tree"

# Encode the query
with torch.no_grad(), torch.amp.autocast(device):
    text_features = model.encode_text(tokenizer([query]).to(device))
    text_features /= text_features.norm(dim=-1, keepdim=True)

# Search the index
k = 5  # Number of top results to retrieve
D, I = index.search(text_features.cpu().numpy(), k)

# Print results
print(f"Top {k} images for query '{query}':")
for i in range(k):
    print(f"{i+1}. {image_paths[I[0][i]]} (similarity: {D[0][i]:.4f})")









    
