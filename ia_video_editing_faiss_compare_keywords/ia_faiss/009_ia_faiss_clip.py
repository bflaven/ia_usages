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
python 009_ia_faiss_clip.py

# source
https://github.com/bflaven/ia_usages/tree/921276b19f5098e990588a7061511ae80af7eb7a/ia_spacy_llm




"""

import open_clip
import torch
from PIL import Image

print('\n--- open_clip ')
print(open_clip.__version__)
print()



# Initialize the model and tokenizer
model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
model.eval()  # model in train mode by default, impacts some models with BatchNorm or stochastic depth active
tokenizer = open_clip.get_tokenizer('ViT-B-32')

# Load and preprocess the image
# image_path = "path/to/your/image.jpg"
image_path = "CLIP.png"
image = Image.open(image_path).convert("RGB")
image_input = preprocess(image).unsqueeze(0)

# Define some text prompts
# text_prompts = ["a photograph", "a painting", "a digital art", "a sketch"]
text_prompts = ["a diagram", "a dog", "a cat"]


text_tokens = tokenizer(text_prompts)

# Encode image and text
with torch.no_grad(), torch.cuda.amp.autocast():
    image_features = model.encode_image(image_input)
    text_features = model.encode_text(text_tokens)

    # Normalize features
    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    # Calculate similarity
    similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)

# Print results
for i, prompt in enumerate(text_prompts):
    print(f"Similarity to '{prompt}': {similarity[0][i].item():.2f}%")










    
