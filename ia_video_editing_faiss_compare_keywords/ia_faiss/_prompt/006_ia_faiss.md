
# 006_ia_faiss.md

## PROMPT_1
As python expert, rewrite the script below with the following change:
- Replace "image_path" by "image_paths"
- Use Faiss to create Faiss index with the variable "query" so I can run the query against all the images inside "image_paths".

```python
query = "A snake in a tree"
```


```python
# Sample image paths (replace with your own images)
image_paths = [
"animal_badger.jpg",
"animal_bear.jpg",
"animal_bird.jpg",
"animal_camel.jpg",
"animal_dog.png",
"animal_elephants.jpg",
"animal_fawn_deer.jpg",
"animal_fish_blobfish.jpg",
"animal_hyena.jpg",
"animal_nature_bird_flying_red.jpg",
"animal_pangolin.jpg",
"animal_red_panda.jpg",
"animal_reptile_chamaeleo.jpg",
"animal_rhino.jpg",
"animal_snake.jpg",
"animal_squirrel.jpg",
"animal_tapir_malaisie.jpg",
"animal_tiger.jpg",
"animal_zebra.jpg",
"source_meta_image_89b37ba_636575492-2021-10-o-touron-lithium-hd-014.jpg"
]
```


```python

import open_clip
import torch
from PIL import Image

print('\n--- open_clip ')
print(open_clip.__version__)
print()


# Initialize the model and tokenizer
model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
model.eval()  # model in train mode by default, impacts some models with BatchNorm or stochastic depth active
tokenizer = open_clip.get_tokenizer('ViT-B-32')

# Load and preprocess the image
# image_path = "path/to/your/image.jpg"
image_path = "CLIP.png"
image = Image.open(image_path).convert("RGB")
image_input = preprocess(image).unsqueeze(0)

# Define some text prompts
# text_prompts = ["a photograph", "a painting", "a digital art", "a sketch"]
text_prompts = ["a diagram", "a dog", "a cat"]

text_tokens = tokenizer(text_prompts)

# Determine the device (CUDA if available, otherwise CPU)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = model.to(device)
image_input = image_input.to(device)
text_tokens = text_tokens.to(device)

# Encode image and text
try:
    with torch.no_grad(), torch.amp.autocast(device):
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(text_tokens)

        # Normalize features
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)

        # Calculate similarity
        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
except RuntimeError:
    # Fallback to CPU execution without autocast if CUDA is not available
    with torch.no_grad():
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(text_tokens)

        # Normalize features
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)

        # Calculate similarity
        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)

# Print results
for i, prompt in enumerate(text_prompts):
    print(f"Similarity to '{prompt}': {similarity[0][i].item():.2f}%")
```

## PERPLEXITY_1

Here's the rewritten script that incorporates the changes you requested, using Faiss to create an index for the images and run a query against all images in `image_paths`:

```python
import open_clip
import torch
from PIL import Image
import faiss
import numpy as np

print('\n--- open_clip ')
print(open_clip.__version__)
print()

# Initialize the model and tokenizer
model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
model.eval()
tokenizer = open_clip.get_tokenizer('ViT-B-32')

# Sample image paths (replace with your own images)
image_paths = [
    "animal_badger.jpg", "animal_bear.jpg", "animal_bird.jpg", "animal_camel.jpg",
    "animal_dog.png", "animal_elephants.jpg", "animal_fawn_deer.jpg",
    "animal_fish_blobfish.jpg", "animal_hyena.jpg", "animal_nature_bird_flying_red.jpg",
    "animal_pangolin.jpg", "animal_red_panda.jpg", "animal_reptile_chamaeleo.jpg",
    "animal_rhino.jpg", "animal_snake.jpg", "animal_squirrel.jpg",
    "animal_tapir_malaisie.jpg", "animal_tiger.jpg", "animal_zebra.jpg",
    "source_meta_image_89b37ba_636575492-2021-10-o-touron-lithium-hd-014.jpg"
]

# Determine the device (CUDA if available, otherwise CPU)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = model.to(device)

# Function to encode images
def encode_images(image_paths):
    image_features = []
    for path in image_paths:
        image = Image.open(path).convert("RGB")
        image_input = preprocess(image).unsqueeze(0).to(device)
        with torch.no_grad(), torch.amp.autocast(device):
            features = model.encode_image(image_input)
            features /= features.norm(dim=-1, keepdim=True)
        image_features.append(features.cpu().numpy())
    return np.concatenate(image_features)

# Encode all images
image_features = encode_images(image_paths)

# Create Faiss index
dimension = image_features.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(image_features)

# Define the query
query = "A snake in a tree"

# Encode the query
with torch.no_grad(), torch.amp.autocast(device):
    text_features = model.encode_text(tokenizer([query]).to(device))
    text_features /= text_features.norm(dim=-1, keepdim=True)

# Search the index
k = 5  # Number of top results to retrieve
D, I = index.search(text_features.cpu().numpy(), k)

# Print results
print(f"Top {k} images for query '{query}':")
for i in range(k):
    print(f"{i+1}. {image_paths[I[0][i]]} (similarity: {D[0][i]:.4f})")
```

This script does the following:

1. It uses the list of `image_paths` you provided.
2. It defines a function `encode_images` to encode all images in the list.
3. It creates a Faiss index using the encoded image features.
4. It encodes the query text "A snake in a tree".
5. It searches the Faiss index for the top 5 most similar images to the query.
6. Finally, it prints the top 5 matching images along with their similarity scores.

Note: Make sure you have the `faiss-cpu` or `faiss-gpu` package installed (`pip install faiss-cpu` or `pip install faiss-gpu`). Also, ensure that all the image paths in `image_paths` are correct and the images are accessible.
