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


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_video_editing_faiss_compare_keywords/ia_faiss/


# launch the file
python 013a_ia_blip_generate_caption_generate_english_known_faces.py


"""

import os
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import face_recognition
import numpy as np

class ImageProcessor:
    def __init__(self):
        # Initialize BLIP model for image captioning
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        
        # Load known faces
        self.known_faces, self.known_names = self.load_known_faces()

    def load_known_faces(self):
        """Load known faces from the 'known_faces' directory."""
        known_faces = []
        known_names = []
        known_faces_dir = "known_faces"
        
        for filename in os.listdir(known_faces_dir):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                name = os.path.splitext(filename)[0]
                image_path = os.path.join(known_faces_dir, filename)
                face_image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(face_image)
                if face_encodings:
                    known_faces.append(face_encodings[0])
                    known_names.append(name)
                else:
                    print(f"Warning: No face detected in {filename}")
        
        return known_faces, known_names

    def vectorize_images(self, directory):
        """Vectorize images in the given directory using BLIP model."""
        vectors = {}
        for filename in os.listdir(directory):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                image_path = os.path.join(directory, filename)
                image = Image.open(image_path)
                inputs = self.processor(images=image, return_tensors="pt")
                with torch.no_grad():
                    output = self.model.vision_model(**inputs)
                vector = output.last_hidden_state.mean(dim=1).squeeze().numpy()
                vectors[filename] = vector
        print("Vectorization complete.")
        return vectors

    def generate_description(self, image_path):
        """Generate description for the given image, including recognized faces."""
        # Load and process the image
        image = Image.open(image_path)
        inputs = self.processor(images=image, return_tensors="pt")
        
        # Generate caption
        with torch.no_grad():
            output = self.model.generate(**inputs, max_new_tokens=50)
        caption = self.processor.decode(output[0], skip_special_tokens=True)
        
        # Perform face recognition
        face_image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(face_image)
        face_encodings = face_recognition.face_encodings(face_image, face_locations)
        
        recognized_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_faces, face_encoding)
            if True in matches:
                match_index = matches.index(True)
                recognized_names.append(self.known_names[match_index])
        
        # Add recognized personalities to the caption
        if recognized_names:
            caption += f" Featuring: {', '.join(recognized_names)}"
        
        return caption

def main():
    processor = ImageProcessor()
    
    # Vectorize images in the "pictures" directory
    vectors = processor.vectorize_images("pictures")
    
    # Generate descriptions for each image
    for filename in os.listdir("pictures"):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join("pictures", filename)
            description = processor.generate_description(image_path)
            print(f"{filename}: {description}")

if __name__ == "__main__":
    main()

    




    
