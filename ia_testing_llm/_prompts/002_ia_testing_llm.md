
# 001_ia_testing_llm.md


## PROMPT_1


As a Python, AI and Spacy expert, can you describe the steps and code for each of these steps for the following objective: compare "list_ia" a first list of the main keywords extracted from a text using an LLM with "list_human" a second list of keywords from the keyword taxonomy of a CMS for example entered by a human. The most important thing in this comparison is to understand the meaning of the words in order to bring them closer together, that is to say for example measure the semantic similarity, possibly indicate other techniques to bring the meaning of the words together in order to only propose the words from the list "list_human" that are semantically closest to "list_ia".



```python

# list_ia
list_ia = ["vaste remaniement ministériel", "Kaïs Saïed", "Affaires étrangères", "Défense", "secrétaires d'État"]

# list_human
list_human = ["Tunisie", "Kaïs Saïed", "Remaniement ministériel"]


```


## MISTRAL_1
To compare the two lists of keywords and measure their semantic similarity, you can follow these steps:

1. **Install Required Libraries**: Ensure you have the necessary libraries installed. You will need `spaCy` for NLP tasks and `transformers` for using pre-trained language models.

2. **Load Pre-trained Models**: Load a pre-trained language model that can compute sentence embeddings.

3. **Compute Embeddings**: Convert the keywords into embeddings using the pre-trained model.

4. **Calculate Similarity**: Compute the cosine similarity between the embeddings of the keywords from both lists.

5. **Filter and Rank**: Filter and rank the keywords from `list_human` based on their similarity to the keywords in `list_ia`.

Here is the code to achieve this:

```python
# Step 1: Install Required Libraries
# !pip install spacy transformers

# Step 2: Import Libraries
import spacy
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Step 3: Load Pre-trained Models
# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load transformers model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Function to compute embeddings
def compute_embeddings(texts):
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings

# Step 4: Compute Embeddings for Both Lists
list_ia = ["vaste remaniement ministériel", "Kaïs Saïed", "Affaires étrangères", "Défense", "secrétaires d'État"]
list_human = ["Tunisie", "Kaïs Saïed", "Remaniement ministériel"]

embeddings_ia = compute_embeddings(list_ia)
embeddings_human = compute_embeddings(list_human)

# Step 5: Calculate Cosine Similarity
similarity_matrix = cosine_similarity(embeddings_ia.numpy(), embeddings_human.numpy())

# Step 6: Filter and Rank
similarity_dict = {}
for i, keyword_ia in enumerate(list_ia):
    for j, keyword_human in enumerate(list_human):
        similarity_dict[(keyword_ia, keyword_human)] = similarity_matrix[i, j]

# Sort the similarity dictionary by values
sorted_similarity = sorted(similarity_dict.items(), key=lambda item: item[1], reverse=True)

# Print the sorted similarity
for (keyword_ia, keyword_human), similarity in sorted_similarity:
    print(f"{keyword_ia} <-> {keyword_human}: {similarity:.4f}")

# Step 7: Extract the most similar keywords from list_human
most_similar_keywords = set()
for (keyword_ia, keyword_human), similarity in sorted_similarity:
    if keyword_human not in most_similar_keywords:
        most_similar_keywords.add(keyword_human)
    if len(most_similar_keywords) >= len(list_human):
        break

print("Most similar keywords from list_human:", most_similar_keywords)
```

### Explanation:

1. **Install Required Libraries**: The code assumes you have `spaCy` and `transformers` installed. If not, you can install them using `pip`.

2. **Import Libraries**: Import the necessary libraries for NLP tasks and transformers.

3. **Load Pre-trained Models**: Load a pre-trained spaCy model and a transformers model for computing sentence embeddings.

4. **Compute Embeddings**: Define a function to compute embeddings for a list of texts using the transformers model.

5. **Calculate Cosine Similarity**: Compute the cosine similarity between the embeddings of the keywords from both lists.

6. **Filter and Rank**: Create a dictionary to store the similarity scores between each pair of keywords. Sort the dictionary by similarity scores in descending order.

7. **Extract the Most Similar Keywords**: Extract and print the most similar keywords from `list_human` based on their similarity to the keywords in `list_ia`.

This approach ensures that you can measure the semantic similarity between the keywords and propose the most relevant keywords from `list_human`.

