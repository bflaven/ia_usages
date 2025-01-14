
# 007_ia_cms.md

## PROMPT_1

As python expert can you merge the two scripts the one that loads a json that should populated the data inside into "cms_existing_kw" and the semantic similarity between the two lists "ia_generated_kw" and "cms_existing_kw" using FAISS for efficient indexing and SentenceTransformer for semantic similarity.


## PERPLEXITY_1


Certainly! I'll merge the two scripts into a single, comprehensive script that loads the JSON file, populates the `cms_existing_kw` list, and then performs the semantic similarity comparison using FAISS and SentenceTransformer. Here's the combined script:

```python
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

def load_keywords_from_json(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return [
        keyword['libelle'].strip('"')
        for keyword in data['keywords']
        if keyword['libelle'].strip('"')  # This condition excludes empty strings
    ]

def get_similar_keywords(ia_generated_kw: List[str], cms_existing_kw: List[str]) -> List[Tuple[str, float, str]]:
    # Initialize the SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Encode the keywords
    ia_embeddings = model.encode(ia_generated_kw)
    cms_embeddings = model.encode(cms_existing_kw)

    # Normalize the vectors
    faiss.normalize_L2(ia_embeddings)
    faiss.normalize_L2(cms_embeddings)

    # Create a FAISS index
    dimension = ia_embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(cms_embeddings)

    # Perform the search
    k = len(cms_existing_kw)  # Search for all possible matches
    distances, indices = index.search(ia_embeddings, k)

    # Create a list to store the keywords with their similarities
    similar_keywords = []

    for i, (dist_row, idx_row) in enumerate(zip(distances, indices)):
        for j, (dist, idx) in enumerate(zip(dist_row, idx_row)):
            similar_keywords.append((cms_existing_kw[idx], float(dist), ia_generated_kw[i]))

    # Remove duplicates while preserving the highest similarity
    seen = {}
    unique_similar_keywords = []
    for kw, sim, orig in similar_keywords:
        if kw not in seen or sim > seen[kw][0]:
            seen[kw] = (sim, orig)
    
    for kw, (sim, orig) in seen.items():
        unique_similar_keywords.append((kw, sim, orig))

    # Sort by similarity (highest to lowest)
    unique_similar_keywords.sort(key=lambda x: x[1], reverse=True)

    return unique_similar_keywords

# Load keywords from JSON file
json_file_path = 'pt_tags_thema_list_2.json'
cms_existing_kw = load_keywords_from_json(json_file_path)

# Define the IA generated keywords
ia_generated_kw = ['Milagre económico', 'Ásia-Pacífico', 'Ásia-Pacífico', 'persona non grata".', 'Ébola', 'Áudio', 'óleo de palma', 'Áustria']

# Get the sorted list of similar keywords with similarities
similar_keywords = get_similar_keywords(ia_generated_kw, cms_existing_kw)

# Print the results
print("Sorted list of keywords from cms_existing_kw with similarities:")
for kw, sim, orig in similar_keywords:
    print(f"'{kw}' (Similarity: {sim:.4f}) - Original: '{orig}'")

# If you need just the keywords in a list, you can do:
most_similar_keywords = [kw for kw, _, _ in similar_keywords]
print("\nOrdered list of most similar keywords:")
print(most_similar_keywords)
```

This combined script does the following:

1. It defines a function `load_keywords_from_json` that reads the JSON file and extracts the non-empty keywords.

2. The `get_similar_keywords` function remains the same as in the previous script, handling the semantic similarity comparison using FAISS and SentenceTransformer.

3. The script first loads the keywords from the JSON file into `cms_existing_kw`.

4. It then defines the `ia_generated_kw` list.

5. The script performs the similarity comparison and prints the results, showing each CMS keyword, its similarity score, and the original IA-generated keyword it matched with.

6. Finally, it also provides just the list of keywords if needed.

This combined script provides a complete workflow:
- Loading existing keywords from a JSON file
- Comparing them with IA-generated keywords using semantic similarity
- Presenting the results in a sorted, detailed manner

You can easily adjust the output or add a similarity threshold if you want to filter the results further. This comprehensive approach provides more information to the editor in the CMS, allowing for more informed decisions when selecting keywords.