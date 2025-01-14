
# 010_ia_faiss.md

## PROMPT_1

As a python expert, rewrite the script below. It does not include the name entities in the description e.g "Putin", "Obama", "Trump", "Macron" and I have defined the directory "known_faces"

```text
known_faces/macron.jpg
known_faces/obama.jpg
known_faces/putin.jpg
known_faces/trump.jpg
```




```python
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


```
## PERPLEXITY_3

Here's a rewritten version of the script that incorporates named entities into the image descriptions:

```python
import os
from PIL import Image
import face_recognition
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer

# Sample image paths
image_paths = [
    "pictures/putin_obama_78882139_179597572-1587096938.jpg",
    "pictures/trump-handshake-1.jpg",
    # ... (other image paths)
]

# Load pre-trained model and tokenizer
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

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
        if True in matches:
            first_match_index = matches.index(True)
            recognized_names.append(known_face_names[first_match_index])

    return recognized_names

def generate_description(image_path):
    try:
        # Load and preprocess the image
        image = Image.open(image_path)
        pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values

        # Generate the caption
        output_ids = model.generate(pixel_values, max_length=50, num_beams=4, early_stopping=True)
        caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        # Recognize faces
        recognized_faces = recognize_faces(image_path)

        # Add face recognition information to the caption
        if recognized_faces:
            face_info = f" featuring {', '.join(recognized_faces)}"
            caption += face_info

        return f"Description: {caption.lower().rstrip('.')}"
    except Exception as e:
        return f"Error processing {os.path.basename(image_path)}: {str(e)}"

# Generate descriptions for each image
for path in image_paths:
    description = generate_description(path)
    print(f"{os.path.basename(path)}: {description}")
```

This script now uses the "nlpconnect/vit-gpt2-image-captioning" model for generating captions, which is more suitable for entity-aware captioning[2]. The `recognize_faces` function remains largely unchanged, but the `generate_description` function has been updated to use the new model and incorporate recognized faces into the caption. The script now should include named entities like "Putin", "Obama", "Trump", and "Macron" in the descriptions when they are recognized in the images[1][5].

Citations:
[1] https://arxiv.org/html/2403.12618v1
[2] https://codingmall.com/knowledge-base/25-global/1579-python-example-code-for-image-captioning
[3] https://bipinkrishnan.github.io/ml-recipe-book/image_captioning.html
[4] https://github.com/gnekt/Image-Captioning-with-Python
[5] https://www.youtube.com/watch?v=eSmBjyLODZ4
[6] https://github.com/alasdairtran/transform-and-tell
[7] https://www.researchgate.net/publication/373086116_Boosting_Entity-aware_Image_Captioning_with_Multi-modal_Knowledge_Graph
