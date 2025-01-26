# prompt_edito_lazy_prompt_6.md

## prompt

As an editorial manager of a YouTube channel in English, follow these steps:

1. **Explain Scripts**:
   - Describe in plain English what each script does.
   - Create a concise, easy-to-understand text for each script that can be used as a YouTube video description.
   - Follow the Editorial Guidelines provided below.

2. **Generate Titles**:
   - From each text generated in the first step, propose 3 suitable titles for a YouTube video.

3. **Create General Proposal**:
   - Merge the texts from each script into a general proposal.
   - Summarize all the texts produced to create a comprehensive description for your YouTube channel.

4. **Generate General Titles**:
   - From the general proposal created in the third step, propose 3 suitable titles for a YouTube video.

**Editorial Guidelines**:
- Keep the texts straightforward and easy to understand.
- Avoid overly promotional language or hard selling.
- Use a neutral tone; avoid being too emphatic, catchy, vulgar, banal, or overly enthusiastic.
- Do not use name-dropping.
- Stay close to the logic of the code submitted.
- Include the names of packages and models to enhance semantic quality and improve search engine optimization (SEO) across various topics.

--- SCRIPT_1
```python

import streamlit as st
import open_clip
import torch
from PIL import Image
import faiss
import numpy as np
import os

class ImageSearchApp:
    def __init__(self):
        st.set_page_config(page_title="VisualQuest", layout="wide", page_icon="🔍")
        st.title("VisualQuest: AI-Powered Image Search 🔍")
        # Add app icon
        # st.image("https://img.icons8.com/color/48/000000/search--v1.png", width=48)


        # Display package versions
        st.info(f"open_clip version: {open_clip.__version__}\nfaiss version: {faiss.__version__}")
        
        # Initialize model and tokenizer
        self.model, _, self.preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
        self.model.eval()
        self.tokenizer = open_clip.get_tokenizer('ViT-B-32')
        
        # Set device
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = self.model.to(self.device)
        
        # Initialize image paths and index
        self.image_paths = self.get_image_paths()
        self.index = None
        
        # Create tabs
        search_tab, archive_tab = st.tabs(["Search", "Search archives"])
        
        with search_tab:
            self.search_tab()
        
        with archive_tab:
            self.archive_tab()
        
    def get_image_paths(self):
        # Retrieve all .jpg and .png files from the 'pictures/' and 'known_faces/' directories
        image_paths = []
        for directory in ["pictures", "known_faces"]:
            image_paths.extend([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith((".jpg", ".png"))])
        return image_paths

    def encode_images(self):
        image_features = []
        for path in self.image_paths:
            try:
                image = Image.open(path).convert("RGB")
                image_input = self.preprocess(image).unsqueeze(0).to(self.device)
                with torch.no_grad():
                    features = self.model.encode_image(image_input)
                    features /= features.norm(dim=-1, keepdim=True)
                image_features.append(features.cpu().numpy())
            except Exception as e:
                st.error(f"Error processing {path}: {str(e)}")
        return np.concatenate(image_features)

    def create_index(self, image_features):
        dimension = image_features.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(image_features.astype(np.float32))
        return index

    def search_images(self, query, k=5):
        with torch.no_grad():
            text_features = self.model.encode_text(self.tokenizer([query]).to(self.device))
            text_features /= text_features.norm(dim=-1, keepdim=True)
        D, I = self.index.search(text_features.cpu().numpy(), k)
        return D[0], I[0]

    def search_tab(self):
        if self.index is None:
            with st.spinner("Encoding images..."):
                image_features = self.encode_images()
            with st.spinner("Creating Faiss index..."):
                self.index = self.create_index(image_features)
            st.success("Image encoding and indexing complete.")
            st.info("You can start using the search in natural language.")

        query = st.text_input("Enter your search query:")
        if st.button("Launch", type="primary"):
            if query:
                distances, indices = self.search_images(query)
                self.display_results(query, distances, indices)
            else:
                st.warning("Please enter a search query.")
        

    def archive_tab(self):
        archived_queries = [            
            "A badger in a field", # (EN)
            "Un tejón en un campo", # (ES)
            "Un blaireau dans un champs", # (FR)
            "Барсук в поле", # (RU)
            "Um texugo em um campo", # (BR)
            "A snake in a tree",
            "A man sits in a tent in the desert",
            "A zebra's muzzle with blue sky around it",
            "A chameleon on a broken branch",
            "Lula, the Brazil's President shaking hand to another person",
            "Prabowo Subianto, the Indonesia's President shaking hand to another person",
            "Putin shaking hand to another person",
            "Trump shaking hand to another person",
            "Modi shaking hand to another person",
            "Mike Johnson shaking hand to another person",
            "Vice President Kamala Harris shakes hands",
            "Mohamar Ouda ex-prisoner in Syria",
            "Edmundo González, venezuelan opposition leader",
            "2 elephants in the savannah",
            "Find me a picture for President Prabowo Subianto?",
            # foreign languages queries
            "Lula, le président du Brésil, serre la main d'une autre personne",
            "Лула, президент Бразилии",
            "Lula, o presidente do Brasil",
            "Lula, tổng thống Brazil",
            "لولا، رئیس جمهور برزیل",
            "Macron serre la main d'une autre personne",
            "Un serpent dans un arbre",
            "ancien prisonnier en Syrie",
            "Looking for J. D. Vance",
            "¿Dónde está el señor Musk?",
            "¿Dónde está el señor Trump?"
        ]


        selected_query = st.selectbox("Select an archived query:", archived_queries)
        if st.button("Search", type="primary"):
            distances, indices = self.search_images(selected_query)
            self.display_results(selected_query, distances, indices)
        
        

    def display_results(self, query, distances, indices):
        st.write(f"Top 5 images for query '{query}':")
        for i, (distance, index) in enumerate(zip(distances, indices)):
            st.write(f"{i+1}. {self.image_paths[index]} (similarity: {distance:.4f})")
            if i == 0:
                st.image(self.image_paths[index], caption=f"Best match: {self.image_paths[index]}")
        # add reload button
        if st.button("Reload", key="reload_archive"):
            # Update
            # `st.experimental_rerun` will be removed after 2024-04-01.
            # st.experimental_rerun()
            st.rerun

if __name__ == "__main__":
    # Suppress the TypedStorage deprecation warning
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="torch._utils")
    
    ImageSearchApp()




```


# mistral


### Step 1: Explain Scripts

#### Script 1: ImageSearchApp

**Description**:
This script creates a Streamlit web application for AI-powered image search using natural language queries. It utilizes the `open_clip` model for encoding images and text, and `faiss` for efficient similarity search. The application allows users to search for images based on textual descriptions and view the top matching images.

**YouTube Video Description**:
This video demonstrates how to build an AI-powered image search application using Streamlit, open_clip, and faiss. The application allows users to search for images using natural language queries. It encodes images and text using the open_clip model and performs efficient similarity searches with faiss. The application features a user-friendly interface with tabs for real-time searches and archived queries, making it easy to find relevant images based on textual descriptions.

### Step 2: Generate Titles

#### Script 1: ImageSearchApp

1. "Building an AI-Powered Image Search App with Streamlit and open_clip"
2. "Efficient Image Search Using Natural Language Queries with faiss"
3. "Creating a User-Friendly Image Search Application with Streamlit"

### Step 3: Create General Proposal

**General Proposal**:
This video series explores the creation of an AI-powered image search application using Streamlit, open_clip, and faiss. The application enables users to search for images using natural language queries, leveraging the power of AI to find the most relevant images efficiently. The open_clip model is used for encoding images and text, while faiss handles the similarity search. The application features a user-friendly interface with tabs for real-time searches and archived queries, making it easy to find relevant images based on textual descriptions.

### Step 4: Generate General Titles

1. "Developing an AI-Powered Image Search Application with Streamlit and open_clip"
2. "Efficient Image Search Using Natural Language Queries and faiss"
3. "Creating a User-Friendly Image Search App with Streamlit and AI"
