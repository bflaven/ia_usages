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
import face_recognition
from PIL import Image
import torch
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

class FaceRecognizer:
    def __init__(self, known_faces_dir):
        self.known_faces = self.load_known_faces(known_faces_dir)

    def load_known_faces(self, directory):
        """Load and encode known faces from a directory."""
        known_faces = {}
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                path = os.path.join(directory, filename)
                image = face_recognition.load_image_file(path)
                encoding = face_recognition.face_encodings(image)
                if encoding:
                    known_faces[os.path.splitext(filename)[0]] = encoding[0]
        return known_faces

    def recognize_faces(self, image_path):
        """Recognize faces in an image."""
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        recognized_faces = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(list(self.known_faces.values()), face_encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = list(self.known_faces.keys())[first_match_index]
            recognized_faces.append(name)
        
        return recognized_faces

class ImageCaptioner:
    def __init__(self):
        self.model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        
        # Set the pad token to the eos token
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model.config.pad_token_id = self.model.config.eos_token_id

    def generate_caption(self, image_path):
        """Generate a caption for an image."""
        image = Image.open(image_path)
        if image.mode != "RGB":
            image = image.convert(mode="RGB")

        pixel_values = self.feature_extractor(images=[image], return_tensors="pt").pixel_values
        attention_mask = torch.ones(pixel_values.shape[0], pixel_values.shape[2], dtype=torch.long)
        
        with torch.no_grad():
            output_ids = self.model.generate(
                pixel_values,
                attention_mask=attention_mask,
                max_length=50,
                num_beams=4,
                early_stopping=True
            )
        
        caption = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return caption

def load_images(use_directory, image_paths=None):
    """Load images from a directory or a list of paths."""
    if use_directory:
        directory = "pictures"
        return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    else:
        return image_paths

def main(use_directory, image_paths=None):
    # Initialize FaceRecognizer and ImageCaptioner
    face_recognizer = FaceRecognizer("known_faces")
    image_captioner = ImageCaptioner()
    
    # Load images
    images = load_images(use_directory, image_paths)
    
    for image_path in images:
        # Recognize faces
        recognized_faces = face_recognizer.recognize_faces(image_path)
        
        # Generate caption
        caption = image_captioner.generate_caption(image_path)
        
        # Combine results
        if recognized_faces:
            recognized_faces_str = ", ".join([face for face in recognized_faces if face != "Unknown"])
            if recognized_faces_str:
                caption += f" Recognized faces: {recognized_faces_str}."
        
        print(f"Image: {image_path}")
        print(f"Description: {caption}")
        print()

if __name__ == "__main__":
    # Set to True to use the "pictures" directory instead of image_paths
    # use_directory = False  
    use_directory = True  

    image_paths = [
        "pictures/kamala_en_20250107_142604_142726_cs.jpg",
        "pictures/syria_prisoner_img_9135.jpg",
        "pictures/edmundo_gonzalez_ap25006631909879.jpg"
    ]
    main(use_directory, image_paths)



    



    




    
