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
streamlit run 019_ia_blip_generate_caption_face_recognition_streamlit.py

"""


import os
import streamlit as st
from PIL import Image
import face_recognition
import torch
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

# Load pre-trained model and tokenizer
@st.cache_resource
def load_model():
    model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    return model, feature_extractor, tokenizer, device

model, feature_extractor, tokenizer, device = load_model()

# Load known faces
@st.cache_resource
def load_known_faces():
    known_face_encodings = []
    known_face_names = ["Trump", "Harris", "Lula", "Modi", "Putin", "Obama", "Macron", "Gonzalez", "Subianto", "Vance", "Musk"]

    for name in known_face_names:
        image = face_recognition.load_image_file(f"known_faces/{name.lower()}.jpg")
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)

    return known_face_encodings, known_face_names

known_face_encodings, known_face_names = load_known_faces()

# Face recognition function
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

# Generate description function
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

        # Add face recognition information to the caption
        if recognized_faces:
            face_info = f" - featuring {', '.join(recognized_faces)}"
            caption += face_info

        return f"Description: {caption.lower().rstrip('.')}"
    except Exception as e:
        return f"Error processing {os.path.basename(image_path)}: {str(e)}"

# Streamlit app
st.title("Image Captioning and Face Recognition App")

# Upload images
uploaded_files = st.file_uploader("Upload Images", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Save uploaded file temporarily
        temp_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Display the image
        st.image(temp_path, caption=uploaded_file.name, use_column_width=True)

        # Generate and display description
        description = generate_description(temp_path)
        st.write(f"**{uploaded_file.name}:** {description}")

        # Remove temporary file
        os.remove(temp_path)



    
