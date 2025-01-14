
# 006_ia_cms.md

## PROMPT_1

As python expert can you write a script that compare the semantic similarity between the two lists "ia_generated_kw" and "cms_existing_kw" and provide a new list of keywords extracted from "cms_existing_kw" that are the most similar with the keywords provided in "ia_generated_kw". You must use the package "Faiss" to make the comparison to speed up the indexing and selecting process and use the package the "SentenceTransformer" from the model "all-MiniLM-L6-v2" to make the semantic similarity.

For your information, the general purpose of all this is to provide to an editor in a CMS, an accurate list of existing keywords in the taxonomy keywords based a bunch of keywords provided by a LLM.

```python

ia_generated_kw = ['Milagre económico', 'Ásia-Pacífico', 'Ásia-Pacífico', 'persona non grata".', 'Ébola', 'Áudio', 'óleo de palma', 'Áustria']

cms_existing_kw = ['Milagre económico', 'agentes do estrangeiro', '1° de Maio', 'persona non grata".', 'phygital', '#Metoopolitico', 'óleo de palma', 'ABBA']


```

## PERPLEXITY_1
Here's a Python script that compares the semantic similarity between the two lists "ia_generated_kw" and "cms_existing_kw" using FAISS for efficient indexing and SentenceTransformer for semantic similarity:

```python
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define the input lists
ia_generated_kw = ['Milagre económico', 'Ásia-Pacífico', 'Ásia-Pacífico', 'persona non grata".', 'Ébola', 'Áudio', 'óleo de palma', 'Áustria']
cms_existing_kw = ['Milagre económico', 'agentes do estrangeiro', '1° de Maio', 'persona non grata".', 'phygital', '#Metoopolitico', 'óleo de palma', 'ABBA']

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
k = 1  # Number of nearest neighbors to retrieve
distances, indices = index.search(ia_embeddings, k)

# Create a list to store the most similar keywords
most_similar_keywords = []

# Threshold for similarity (adjust as needed)
similarity_threshold = 0.7

for i, idx in enumerate(indices):
    if distances[i][0] > similarity_threshold:
        most_similar_keywords.append(cms_existing_kw[idx[0]])

# Remove duplicates while preserving order
most_similar_keywords = list(dict.fromkeys(most_similar_keywords))

print("Most similar keywords from cms_existing_kw:")
print(most_similar_keywords)
```

This script does the following:

1. It imports the necessary libraries: FAISS for efficient similarity search and SentenceTransformer for generating semantic embeddings[1][2].

2. It initializes the SentenceTransformer model using the 'all-MiniLM-L6-v2' model as specified[2].

3. The input lists `ia_generated_kw` and `cms_existing_kw` are defined.

4. The script encodes both lists of keywords into embeddings using the SentenceTransformer model[2].

5. The embeddings are normalized to ensure cosine similarity can be computed using dot product[7].

6. A FAISS index is created and the `cms_embeddings` are added to it[3][7].

7. The script performs a similarity search for each keyword in `ia_generated_kw` against the FAISS index of `cms_existing_kw`[5].

8. It applies a similarity threshold (0.7 in this case, which you can adjust) to filter out less similar matches[9].

9. The script creates a list of the most similar keywords from `cms_existing_kw`, removing duplicates while preserving the order.

10. Finally, it prints the list of most similar keywords.

This approach uses FAISS for efficient indexing and searching, which is particularly useful for larger datasets[5][7]. The SentenceTransformer model provides high-quality semantic embeddings, allowing for meaningful similarity comparisons[2][4].

By adjusting the similarity threshold, you can control how strict the matching is. A higher threshold will result in fewer but more closely related matches, while a lower threshold will include more potential matches but with potentially lower similarity[9].

This script provides an efficient way for editors in a CMS to get an accurate list of existing keywords from the taxonomy based on keywords provided by an LLM, as per your specified use case.

Citations:
[1] https://python.plainenglish.io/understanding-semantic-search-and-faiss-for-efficient-similarity-search-with-python-374dc7f2be84?gi=1815f4381604
[2] https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html
[3] https://huggingface.co/learn/nlp-course/chapter5/6?fw=tf
[4] https://www.sbert.net/examples/applications/semantic-search/README.html
[5] https://myscale.com/blog/mastering-semantic-search-faiss-langchain-step-by-step-guide/
[6] https://www.vennify.ai/semantic-similarity-sentence-transformers/
[7] https://github.com/facebookresearch/faiss?files=1
[8] https://sbert.net/examples/training/sts/README.html
[9] https://qxf2.com/blog/build-semantic-search-faiss/
[10] https://towardsdatascience.com/billion-scale-semantic-similarity-search-with-faiss-sbert-c845614962e2?gi=ae5b8d316f33

