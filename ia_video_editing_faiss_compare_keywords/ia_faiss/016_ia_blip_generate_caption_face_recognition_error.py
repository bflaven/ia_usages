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
/Users/brunoflaven/Documents/01_work/blog_articles/ia_video_editing_faiss_compare_keywords/ia_faiss


# launch the file
python 016_ia_blip_generate_caption_face_recognition.py


"""
import os
from PIL import Image
import face_recognition
from transformers import BlipProcessor, BlipForConditionalGeneration

# Sample image paths
image_paths = [
    "pictures/putin_obama_78882139_179597572-1587096938.jpg",
    "pictures/trump-handshake-1.jpg",
    # ... (other image paths)
]

# Load BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

# Load known faces
known_face_encodings = []
known_face_names = ["Putin", "Obama", "Trump", "Macron"]

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
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        recognized_names.append(name)

    return recognized_names

def generate_description(image_path):
    try:
        # Load and process the image
        image = Image.open(image_path).convert('RGB')
        inputs = processor(images=image, return_tensors="pt")
        
        # Generate caption
        output = model.generate(**inputs, max_new_tokens=20)
        caption = processor.decode(output[0], skip_special_tokens=True)
        
        # Recognize faces
        recognized_faces = recognize_faces(image_path)
        
        # Add face recognition information to the caption
        if recognized_faces:
            face_info = f" with {', '.join(recognized_faces)} recognized"
            caption += face_info
        
        # Convert caption to search query format
        query = f"Description: {caption.lower().rstrip('.')}"
        return query
    except Exception as e:
        return f"Error processing {os.path.basename(image_path)}: {str(e)}"

# Generate descriptions for each image
for path in image_paths:
    description = generate_description(path)
    print(f"{os.path.basename(path)}: {description}")



    
