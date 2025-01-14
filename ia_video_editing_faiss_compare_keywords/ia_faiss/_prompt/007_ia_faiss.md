
# 007_ia_faiss.md

## PROMPT_1
As python expert, write a script that generate a description for each image inside "image_paths". As a result, the description should look like a human type search query. It must use an analyze for each image content to create plausible descriptions.




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
```




## PERPLEXITY_1

Here's a Python script that generates descriptions for each image in the `image_paths` list, creating plausible descriptions that resemble human-typed search queries based on the image content:

```python
import os
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

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
        query = f"image of {caption.lower().rstrip('.')}"
        return query
    except Exception as e:
        return f"Error processing {os.path.basename(image_path)}: {str(e)}"

# Generate descriptions for each image
for path in image_paths:
    description = generate_description(path)
    print(f"{os.path.basename(path)}: {description}")
```

This script does the following:

1. We import the necessary libraries, including PIL for image processing and the Hugging Face Transformers library for the BLIP image captioning model[1][2].

2. We define a function `generate_description` that takes an image path as input:
   - It opens and processes the image using the BLIP processor.
   - Generates a caption using the BLIP model.
   - Converts the caption to a search query format by adding "image of" at the beginning and making it lowercase[3].

3. We iterate through each image path in the `image_paths` list:
   - Generate a description for each image.
   - Print the filename and the generated description.

This script uses the BLIP (Bootstrapping Language-Image Pre-training) model, which is state-of-the-art for image captioning tasks[4]. The generated descriptions will resemble human-typed search queries based on the content of each image.

To use this script, make sure to install the required libraries:

```bash
pip install pillow torch transformers
```

Then run the script, and it will output descriptions for each image in the `image_paths` list[5].

Citations:
[1] https://data-flair.training/blogs/python-based-project-image-caption-generator-cnn/
[2] https://guillermoch.com/exploring-embedding-spaces-with-my-photo-library-c53bf23f35b9?gi=1b3e90bd5165
[3] https://www.youtube.com/watch?v=CzO8VuaHfKM
[4] https://github.com/snap-research/MyVLM/blob/master/README.md
[5] https://github.com/cyberandy/image-captioning



