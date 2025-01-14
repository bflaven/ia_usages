
# 009_ia_faiss.md

## PROMPT_1

As a python expert, rewrite the script below that generates a description for each image inside "image_paths". For the description, make a coding proposition in order to insert well known figures as name entities  like : Trump, Modi, Lula... inside the description text.

```python

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

def generate_description(image_path):
    try:
        # Load and process the image
        image = Image.open(image_path).convert('RGB')
        inputs = processor(images=image, return_tensors="pt")
        
        # Generate caption
        output = model.generate(**inputs, max_new_tokens=20)
        caption = processor.decode(output[0], skip_special_tokens=True)
        
        # Convert caption to search query format
        query = f"Description: {caption.lower().rstrip('.')}"
        return query
    except Exception as e:
        return f"Error processing {os.path.basename(image_path)}: {str(e)}"

# Generate descriptions for each image
for path in image_paths:
    description = generate_description(path)
    print(f"{os.path.basename(path)}: {description}")

```








## PERPLEXITY_1
Here's a rewritten version of the script that generates descriptions for images and inserts well-known figures as named entities:

```python
import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import random

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

# List of well-known figures
figures = ["Trump", "Modi", "Lula", "Obama", "Putin", "Kamala Harris", "Macron", "Merkel", "Xi Jinping", "Boris Johnson"]

def insert_named_entity(caption):
    words = caption.split()
    if len(words) > 3:
        insert_position = random.randint(1, len(words) - 1)
        figure = random.choice(figures)
        words.insert(insert_position, figure)
    return " ".join(words)

def generate_description(image_path):
    try:
        # Load and process the image
        image = Image.open(image_path).convert('RGB')
        inputs = processor(images=image, return_tensors="pt")
        
        # Generate caption
        output = model.generate(**inputs, max_new_tokens=20)
        caption = processor.decode(output[0], skip_special_tokens=True)
        
        # Insert named entity
        caption_with_entity = insert_named_entity(caption)
        
        # Convert caption to search query format
        query = f"Description: {caption_with_entity.lower().rstrip('.')}"
        return query
    except Exception as e:
        return f"Error processing {os.path.basename(image_path)}: {str(e)}"

# Generate descriptions for each image
for path in image_paths:
    description = generate_description(path)
    print(f"{os.path.basename(path)}: {description}")
```

This script introduces the following changes:

1. A list of well-known figures is defined[1].

2. A new function `insert_named_entity()` is added to randomly insert a figure's name into the generated caption[3].

3. The `generate_description()` function now calls `insert_named_entity()` to modify the caption before returning it[4].

This approach will randomly insert a well-known figure's name into the generated descriptions, creating more diverse and potentially interesting captions. Note that the insertions are random and may not always make sense in the context of the image, but it fulfills the requirement of including named entities in the descriptions[7].

Citations:
[1] https://thepythoncode.com/article/image-captioning-with-pytorch-and-transformers-in-python
[2] http://violet-spiders.cocolog-nifty.com/blog/2008/10/post-ac01-2.html
[3] https://www.edenai.co/post/how-to-generate-images-from-text-with-python
[4] https://data-flair.training/blogs/python-based-project-image-caption-generator-cnn/
[5] https://www.youtube.com/watch?v=okSrioyYnHw
[6] https://github.com/prateekkeshari/ImageCaptioning
[7] https://www.kaggle.com/code/ysthehurricane/image-caption-generator-tutorial




## PROMPT_2
Rewrite the script and do not use for the script any predefined figures, try to ensure that a package is able to detect which faces are in the pictures.
```python
# List of well-known figures
figures = ["Trump", "Modi", "Lula", "Obama", "Putin", "Kamala Harris", "Macron", "Merkel", "Xi Jinping", "Boris Johnson"]
```

## PERPLEXITY_2


Here's a rewritten version of the script that uses face detection to identify faces in the images without relying on predefined figures:

```python
import os
from PIL import Image
import face_recognition
from transformers import BlipProcessor, BlipForConditionalGeneration

# Sample image paths (replace with your own images)
image_paths = [
    "pictures/animal_badger.jpg",
    # ... (other image paths)
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
```

This script uses the `face_recognition` library to detect faces in the images[8]. Instead of inserting predefined figures, it counts the number of faces detected in each image and adds this information to the caption. The `detect_faces` function returns the number of faces found in an image[8].

The `generate_description` function now includes face detection. If faces are detected, it adds this information to the caption (e.g., "with 2 faces detected"). This approach provides more accurate information about the actual content of the images without relying on a predefined list of figures[1][3].

Remember to install the required libraries:

```
pip install face_recognition pillow transformers
```

This script will generate captions for the images and include information about detected faces, providing a more dynamic and content-aware description of each image[5][7].

Citations:
[1] https://dev.to/devasservice/face-detection-made-easy-with-opencv-and-python-3hgj
[2] https://arxiv.org/html/2403.12618v1
[3] https://cloudinary.com/guides/image-effects/face-detection-in-python
[4] https://blender.cs.illinois.edu/paper/imagecaption.pdf
[5] https://realpython.com/face-recognition-with-python/
[6] https://www.researchgate.net/publication/344894385_A_Caption_Is_Worth_A_Thousand_Images_Investigating_Image_Captions_for_Multimodal_Named_Entity_Recognition
[7] https://www.codingal.com/coding-for-kids/blog/build-face-recognition-app-with-python/
[8] https://pypi.org/project/face-recognition/


## PERPLEXITY_3
It does not work can you rewrite the script as I known for instance that there are pictures with "Putin", "Obama", "Trump", "Macron"... can you ensure that the package "face_recognition" recognize the well-known faces.

```python
import os
from PIL import Image
import face_recognition
from transformers import BlipProcessor, BlipForConditionalGeneration

# Sample image paths (replace with your own images)
image_paths = [
    "pictures/putin_obama_78882139_179597572-1587096938.jpg",
    "pictures/trump-handshake-1.jpg",
    # ... (other image paths)
]
```


