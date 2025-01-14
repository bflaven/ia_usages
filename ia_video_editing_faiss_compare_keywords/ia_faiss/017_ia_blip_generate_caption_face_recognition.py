#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name ia_using_faiss python=3.9.13
conda info --envs
source activate ia_using_faiss
conda deactivate



# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_using_faiss

# install good
python -m pip install pillow torch transformers
python -m pip install pillow torch transformers sentencepiece
python -m pip install sentencepiece 

# to insert face_recognition
python -m pip install face_recognition



# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_video_editing_faiss_compare_keywords/ia_faiss


# launch the file
python 017_ia_blip_generate_caption_face_recognition.py


"""


import os
from PIL import Image
import face_recognition
import torch
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

# Sample image paths
image_paths = [
    "pictures/brazil_indonesia_presidents.png",
    "pictures/Prime-Minister-Narendra-Modi_1687153732144_1687153732409.jpg",
    "pictures/putin_obama_78882139_179597572-1587096938.jpg",
    "pictures/trump-handshake-1.jpg",
    "pictures/kamala_en_20250107_142604_142726_cs.jpg",
    "pictures/syria_prisoner_img_9135.jpg",
    "pictures/edmundo_gonzalez_ap25006631909879.jpg",
    "pictures/elon-musk-donald-trump-jd-vance.jpg",
    # ... (other image paths)
]

# Load pre-trained model and tokenizer
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

# Set the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Load known faces
known_face_encodings = []

# known_face_names = ["Harris", "Lula", "Modi", "Putin", "Obama", "Macron", "Gonzalez", "Subianto"]

# known_face_names = ["Trump", "Harris", "Lula", "Modi", "Putin", "Obama", "Macron", "Gonzalez", "Subianto"]

known_face_names = ["Trump", "Harris", "Lula", "Modi", "Putin", "Obama", "Macron", "Gonzalez", "Subianto", "Vance", "Musk"]


for name in known_face_names:
    image = face_recognition.load_image_file(f"known_faces/{name.lower()}.jpg")
    encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(encoding)

def recognize_faces(image_path):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    recognized_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        if True in matches:
            first_match_index = matches.index(True)
            recognized_names.append(known_face_names[first_match_index])

    return recognized_names


def generate_description(image_path):
    try:
        # Load and preprocess the image
        image = Image.open(image_path)
        inputs = feature_extractor(images=image, return_tensors="pt").to(device)
        
        # Generate the caption
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=50, num_beams=4, early_stopping=True)
        
        caption = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Recognize faces
        recognized_faces = recognize_faces(image_path)

        # Print out recognized_faces
        # print('\n--- recognized_faces ')
        # print(f"{recognized_faces}")

        # Add face recognition information to the caption
        if recognized_faces:
            face_info = f" - featuring {', '.join(recognized_faces)}"
            caption += face_info

        return f"Description: {caption.lower().rstrip('.')}"
    except Exception as e:
        return f"Error processing {os.path.basename(image_path)}: {str(e)}"

# Generate descriptions for each image
for path in image_paths:
    description = generate_description(path)
    print(f"{os.path.basename(path)}: {description}")



    
