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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_video_editing_faiss_compare_keywords/ia_faiss

# launch the file in streamlit
streamlit run 018_ia_blip_generate_caption_face_recognition_streamlit_error.py


"""


import os
import streamlit as st
from PIL import Image
import face_recognition
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load BLIP model and processor
@st.cache_resource
def load_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
    return processor, model

processor, model = load_model()

def detect_faces(image):
    face_locations = face_recognition.face_locations(image)
    return len(face_locations)

def generate_description(image):
    try:
        # Process the image
        inputs = processor(images=image, return_tensors="pt")
        
        # Generate caption
        output = model.generate(**inputs, max_new_tokens=20)
        caption = processor.decode(output[0], skip_special_tokens=True)
        
        # Detect faces
        num_faces = detect_faces(face_recognition.load_image_file(image))
        
        # Add face detection information to the caption
        if num_faces > 0:
            face_info = f" with {num_faces} {'face' if num_faces == 1 else 'faces'} detected"
            caption += face_info
        
        # Convert caption to search query format
        query = f"Description: {caption.lower().rstrip('.')}"
        return query
    except Exception as e:
        return f"Error processing image: {str(e)}"

st.title("Image Description Generator")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")
    st.write("Generating description...")
    description = generate_description(image)
    st.write(description)
    

    
