
# 008_ia_faiss.md

## PROMPT_1
In this script, can you generate caption in different language than English e.g. Spanish, French, Russian... etc





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

Certainly! We can modify the script to generate captions in different languages. We'll use the MarianMT translation model from Hugging Face to translate the English captions into various languages. Here's the updated script that generates captions in English, Spanish, French, and Russian:

```python
import os
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration, MarianMTModel, MarianTokenizer

# Sample image paths (replace with your own images)
image_paths = [
    "pictures/animal_badger.jpg", 
    "pictures/animal_bear.jpg", 
    "pictures/animal_bird.jpg", 
    # ... (other image paths)
]

# Load BLIP model and processor
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

# Load translation models
translation_models = {
    "Spanish": ("Helsinki-NLP/opus-mt-en-es", "es"),
    "French": ("Helsinki-NLP/opus-mt-en-fr", "fr"),
    "Russian": ("Helsinki-NLP/opus-mt-en-ru", "ru")
}

translation_models_cache = {}

def load_translation_model(language):
    if language not in translation_models_cache:
        model_name, _ = translation_models[language]
        model = MarianMTModel.from_pretrained(model_name)
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        translation_models_cache[language] = (model, tokenizer)
    return translation_models_cache[language]

def translate_text(text, target_language):
    model, tokenizer = load_translation_model(target_language)
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

def generate_description(image_path, languages):
    try:
        # Load and process the image
        image = Image.open(image_path).convert('RGB')
        inputs = blip_processor(images=image, return_tensors="pt")
        
        # Generate caption in English
        output = blip_model.generate(**inputs, max_new_tokens=20)
        caption_en = blip_processor.decode(output[0], skip_special_tokens=True)
        
        # Prepare descriptions in different languages
        descriptions = {"English": f"image of {caption_en.lower().rstrip('.')}"}
        
        for lang in languages:
            if lang != "English":
                translated_caption = translate_text(caption_en, lang)
                descriptions[lang] = f"imagen de {translated_caption.lower().rstrip('.')}" if lang == "Spanish" else \
                                     f"image de {translated_caption.lower().rstrip('.')}" if lang == "French" else \
                                     f"изображение {translated_caption.lower().rstrip('.')}" if lang == "Russian" else \
                                     f"image of {translated_caption.lower().rstrip('.')}"
        
        return descriptions
    except Exception as e:
        return {lang: f"Error processing {os.path.basename(image_path)}: {str(e)}" for lang in languages}

# Languages to generate descriptions in
languages = ["English", "Spanish", "French", "Russian"]

# Generate descriptions for each image
for path in image_paths:
    descriptions = generate_description(path, languages)
    print(f"\n{os.path.basename(path)}:")
    for lang, desc in descriptions.items():
        print(f"  {lang}: {desc}")
```

This updated script does the following:

1. We import the necessary additional libraries for translation (MarianMTModel and MarianTokenizer).

2. We define translation models for Spanish, French, and Russian.

3. We create a `load_translation_model` function to load and cache translation models for efficiency.

4. We add a `translate_text` function to translate the English caption to the target language.

5. We modify the `generate_description` function to:
   - Generate the caption in English using BLIP.
   - Translate the caption to the specified languages.
   - Format the descriptions appropriately for each language.

6. We define a list of languages we want to generate descriptions in.

7. We iterate through each image path, generate descriptions in all specified languages, and print the results.

To use this script, you'll need to install the additional required libraries:

```bash
pip install pillow torch transformers sentencepiece
```

This script will now generate descriptions that resemble human-typed search queries in English, Spanish, French, and Russian for each image in the `image_paths` list. The output will show the filename followed by the descriptions in each language.

Note that the quality of translations may vary, and for best results in a production environment, you might want to consider using more specialized translation services or fine-tuned models for specific domains.



