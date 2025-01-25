
# 015_ia_faiss.md




## PROMPT_1

As a prompt expert, first, can you improve the logic of the prompt and see if the main objective is well understood. Second, to fully understand if the purpose has been understood, translate into French the improved prompt.

Write the improved prompt in english and in french into ```text ``` so I just have to cut and paste the text.

```text
As a python expert, write a script:
- load, browse and load images from a directory named "pictures", vectorize these images or load a certain number of images defined in an object named "image_paths". The user can define with a boolean whether he wants to parse the directory "pictures" or goes for the object "image_paths". 
- use the images in a directory "known_faces" to see if some of the faces that are in the "pictures" contains images with known faces.
- generate at the end a description for each image in "pictures" with a mention featuring the filename without the extension found in "known_faces" if several faces are recognized in pictures found "pictures"

The main objective of all this script is to generate a description that mixes facial recognition based on a list of known faces stored in a directory so the user can extend by adding images in the directory the ability to write relevant description for any image.
```




# MISTRAL_1


### Improved Prompt in English

```text
As a Python expert, write a script that performs the following tasks:

1. **Image Loading**:
   - Load and browse images from a directory named "pictures".
   - Alternatively, load a specified number of images defined in an object named "image_paths".
   - The user can specify via a boolean whether to parse the directory "pictures" or use the object "image_paths".

2. **Facial Recognition**:
   - Use the images in a directory named "known_faces" to check if any faces in the images from the "pictures" directory match known faces.

3. **Description Generation**:
   - Generate a description for each image in the "pictures" directory.
   - If multiple faces are recognized in an image, include the filenames (without extensions) of the corresponding known faces in the description.

The main objective of this script is to generate descriptions that incorporate facial recognition based on a list of known faces stored in a directory. This allows the user to extend the script's capabilities by adding more images to the "known_faces" directory, thereby enhancing the ability to write relevant descriptions for any image.
```

### Improved Prompt in French

```text
En tant qu'expert en Python, écrivez un script qui réalise les tâches suivantes :

1. **Chargement des Images** :
   - Chargez et parcourez les images d'un répertoire nommé "pictures".
   - Alternativement, chargez un nombre spécifié d'images définies dans un objet nommé "image_paths".
   - L'utilisateur peut spécifier via un booléen s'il faut parcourir le répertoire "pictures" ou utiliser l'objet "image_paths".

2. **Reconnaissance Faciale** :
   - Utilisez les images d'un répertoire nommé "known_faces" pour vérifier si certains des visages dans les images du répertoire "pictures" correspondent à des visages connus.

3. **Génération de Descriptions** :
   - Générez une description pour chaque image dans le répertoire "pictures".
   - Si plusieurs visages sont reconnus dans une image, incluez les noms de fichiers (sans extensions) des visages connus correspondants dans la description.

L'objectif principal de ce script est de générer des descriptions qui intègrent la reconnaissance faciale basée sur une liste de visages connus stockés dans un répertoire. Cela permet à l'utilisateur d'étendre les capacités du script en ajoutant plus d'images au répertoire "known_faces", améliorant ainsi la capacité à écrire des descriptions pertinentes pour n'importe quelle image.
```



## PROMPT_2

As a Python expert, write a script that performs the following tasks:

1. **Image Loading**:
   - Load and browse images from a directory named "pictures".
   - Alternatively, load a specified number of images defined in an object named "image_paths".
   - The user can specify via a boolean whether to parse the directory "pictures" or use the object "image_paths".

2. **Facial Recognition**:
   - Use the images in a directory named "known_faces" to check if any faces in the images from the "pictures" directory match known faces.

3. **Description Generation**:
   - Generate a description for each image in the "pictures" directory.
   - If multiple faces are recognized in an image, include the filenames (without extensions) of the corresponding known faces in the description.

The main objective of this script is to generate descriptions that incorporate facial recognition based on a list of known faces stored in a directory. This allows the user to extend the script's capabilities by adding more images to the "known_faces" directory, thereby enhancing the ability to write relevant descriptions for any image.

```python
image_paths = [
                # "pictures/animal_badger.jpg", 
                # "pictures/animal_bear.jpg", 
                # "pictures/animal_bird.jpg", 
                # "pictures/brazil_indonesia_presidents.png",
                # "pictures/Prime-Minister-Narendra-Modi_1687153732144_1687153732409.jpg",
                # "pictures/putin_obama_78882139_179597572-1587096938.jpg",
                # "pictures/trump-handshake-1.jpg",
                "pictures/kamala_en_20250107_142604_142726_cs.jpg",
                "pictures/syria_prisoner_img_9135.jpg",
                "pictures/edmundo_gonzalez_ap25006631909879.jpg"
            ]
```

# PERPLEXITY_1

Thank you for providing the additional context with the `image_paths` object. I'll modify the script to incorporate this information and ensure it meets all the requirements you've specified. Here's the updated Python script:

```python
import os
import face_recognition
from PIL import Image
import numpy as np
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch

def load_images(use_directory, image_paths=None):
    if use_directory:
        directory = "pictures"
        return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    else:
        return image_paths

def load_known_faces(directory):
    known_faces = {}
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(directory, filename)
            image = face_recognition.load_image_file(path)
            encoding = face_recognition.face_encodings(image)
            if encoding:
                known_faces[os.path.splitext(filename)[0]] = encoding[0]
    return known_faces

def recognize_faces(image_path, known_faces):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    recognized_faces = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(list(known_faces.values()), face_encoding)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = list(known_faces.keys())[first_match_index]
        recognized_faces.append(name)
    
    return recognized_faces

def generate_description(image_path, model, feature_extractor, tokenizer):
    image = Image.open(image_path)
    if image.mode != "RGB":
        image = image.convert(mode="RGB")

    pixel_values = feature_extractor(images=[image], return_tensors="pt").pixel_values
    
    with torch.no_grad():
        output_ids = model.generate(pixel_values, max_length=50)
    
    description = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]
    return description

def main(use_directory, image_paths=None):
    # Load images
    images = load_images(use_directory, image_paths)
    
    # Load known faces
    known_faces = load_known_faces("known_faces")
    
    # Load description generation model
    model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    
    for image_path in images:
        # Recognize faces
        recognized_faces = recognize_faces(image_path, known_faces)
        
        # Generate description
        description = generate_description(image_path, model, feature_extractor, tokenizer)
        
        # Combine results
        if recognized_faces:
            recognized_faces_str = ", ".join([face for face in recognized_faces if face != "Unknown"])
            if recognized_faces_str:
                description += f" Recognized faces: {recognized_faces_str}."
        
        print(f"Image: {image_path}")
        print(f"Description: {description}")
        print()

if __name__ == "__main__":
    use_directory = False  # Set to True to use the "pictures" directory instead of image_paths
    image_paths = [
        "pictures/kamala_en_20250107_142604_142726_cs.jpg",
        "pictures/syria_prisoner_img_9135.jpg",
        "pictures/edmundo_gonzalez_ap25006631909879.jpg"
    ]
    main(use_directory, image_paths)
```

This script fulfills all the requirements you specified:

1. **Image Loading**: 
   - The `load_images` function can load images from either the "pictures" directory or use the specified `image_paths` object, depending on the `use_directory` boolean.

2. **Facial Recognition**:
   - The `load_known_faces` function loads and encodes faces from the "known_faces" directory.
   - The `recognize_faces` function uses these known faces to identify faces in the input images.

3. **Description Generation**:
   - The `generate_description` function uses a pre-trained Vision Transformer (ViT) model to generate a description for each image.
   - If multiple faces are recognized, their names (filenames without extensions) are included in the final description.

The main function combines all these tasks. It loads the images, recognizes faces, generates descriptions, and then combines the results.

To use this script:

1. Install the required libraries: `face_recognition`, `pillow`, `numpy`, `transformers`, and `torch`.
2. Place your input images in a directory named "pictures".
3. Place images of known faces in a directory named "known_faces". The filenames (without extensions) will be used as the names for recognition.
4. Set the `use_directory` boolean to `True` if you want to use all images in the "pictures" directory, or `False` to use the specified `image_paths`.
5. Run the script.

You can extend the script's capabilities by adding more images to the "known_faces" directory, which will enhance its ability to recognize faces and write relevant descriptions for any image.

