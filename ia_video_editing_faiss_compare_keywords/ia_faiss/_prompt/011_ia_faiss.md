
# 011_ia_faiss.md

## PROMPT_1

As a python expert, rewrite the all script below in order to avoid this error when the script is executed. Write the all script so I can cut and paste it.



```text
The attention mask is not set and cannot be inferred from input because pad token is same as eos token. As a consequence, you may observe unexpected behavior. Please pass your input's `attention_mask` to obtain reliable results.
We strongly recommend passing in an `attention_mask` since your input_ids may be padded. See https://huggingface.co/docs/transformers/troubleshooting#incorrect-output-when-padding-tokens-arent-masked.
You may ignore this warning if your `pad_token_id` (50256) is identical to the `bos_token_id` (50256), `eos_token_id` (50256), or the `sep_token_id` (None), and your input is not padded.
```

```python
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
known_face_names = ["Harris", "Lula", "Modi", "Putin", "Obama", "Trump", "Macron", "Gonzalez", "Subianto"]

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



```


## CHATGPT_3

Here’s the revised script to avoid the warning about `attention_mask` not being set while generating captions. The script ensures the `attention_mask` is explicitly passed during generation. You can copy and paste the entire corrected script. 

```python
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
known_face_names = ["Harris", "Lula", "Modi", "Putin", "Obama", "Trump", "Macron", "Gonzalez", "Subianto"]

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
        inputs = feature_extractor(images=image, return_tensors="pt")
        inputs = {key: value.to(device) for key, value in inputs.items()}

        # Generate the caption
        with torch.no_grad():
            outputs = model.generate(
                input_ids=inputs["pixel_values"],
                attention_mask=torch.ones_like(inputs["pixel_values"]),
                max_length=50,
                num_beams=4,
                early_stopping=True
            )
        
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

# Generate descriptions for each image
for path in image_paths:
    description = generate_description(path)
    print(f"{os.path.basename(path)}: {description}")
```

### Key Changes:
1. **Attention Mask**: The `attention_mask` is explicitly passed to the `model.generate()` method as `torch.ones_like(inputs["pixel_values"])`.
2. **Inputs Device Mapping**: Ensured all input tensors are moved to the appropriate device.
3. **Code Consistency**: Minor cleanup for clarity and alignment.

This should prevent the warning and ensure the script executes reliably.
