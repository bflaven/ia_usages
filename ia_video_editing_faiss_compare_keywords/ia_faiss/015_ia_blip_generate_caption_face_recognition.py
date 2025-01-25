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
python 015_ia_blip_generate_caption_face_recognition.py


"""
import os
from PIL import Image
import face_recognition
from transformers import BlipProcessor, BlipForConditionalGeneration

# Sample image paths (replace with your own images)
image_paths = [
    # "pictures/animal_badger.jpg", 
    # "pictures/animal_bear.jpg", 
    # "pictures/animal_bird.jpg", 
    # "pictures/animal_camel.jpg",
    # "pictures/animal_dog.png", 
    # "pictures/animal_elephants.jpg", 
    # "pictures/animal_fawn_deer.jpg",
    # "pictures/animal_fish_blobfish.jpg", 
    # "pictures/animal_hyena.jpg", 
    # "pictures/animal_nature_bird_flying_red.jpg",
    # "pictures/animal_pangolin.jpg", 
    # "pictures/animal_red_panda.jpg", 
    # "pictures/animal_reptile_chamaeleo.jpg",
    # "pictures/animal_rhino.jpg", 
    # "pictures/animal_snake.jpg", 
    # "pictures/animal_squirrel.jpg",
    # "pictures/animal_tapir_malaisie.jpg", 
    # "pictures/animal_tiger.jpg", 
    # "pictures/animal_zebra.jpg",
    "pictures/source_meta_image_89b37ba_636575492-2021-10-o-touron-lithium-hd-014.jpg",
    "pictures/brazil_indonesia_presidents.png",
    "pictures/Prime-Minister-Narendra-Modi_1687153732144_1687153732409.jpg",
    "pictures/putin_obama_78882139_179597572-1587096938.jpg",
    "pictures/trump-handshake-1.jpg",
    "pictures/kamala_en_20250107_142604_142726_cs.jpg",
    "pictures/syria_prisoner_img_9135.jpg",
    "pictures/edmundo_gonzalez_ap25006631909879.jpg",
]

# Load BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def detect_faces(image_path):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    return len(face_locations)

def generate_description(image_path):
    try:
        # Load and process the image
        image = Image.open(image_path).convert('RGB')
        inputs = processor(images=image, return_tensors="pt")
        
        # Generate caption
        output = model.generate(**inputs, max_new_tokens=20)
        caption = processor.decode(output[0], skip_special_tokens=True)
        
        # Detect faces
        num_faces = detect_faces(image_path)
        
        # Add face detection information to the caption
        if num_faces > 0:
            face_info = f" with {num_faces} {'face' if num_faces == 1 else 'faces'} detected"
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





    
