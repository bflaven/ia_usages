
# 003_ia_faiss.md

## PROMPT_1
As python expert can script with Faiss and "sentence-transformers/all-MiniLM-L6-v2" the 3 titles among the variable "title_proposals" that are the best in comparison with the value inside "best_title".


```python
# Define the best title and the title proposals
best_title = "German opposition demands confidence vote next week as Scholz's coalition crumbles"

title_proposals = [
"CDU Calls for Confidence Vote in Germany Amid Coalition Crisis Following Finance Minister's Dismissal",
"Olaf Scholz Faces Confidence Vote as German Coalition Collapses After Finance Minister's Exit",
"German Government Crisis: CDU Demands Confidence Vote after Finance Minister Dismissal",
"Coalition Crumbles: Scholz Faces Confidence Vote as Germany's CDU Opposition Calls for Action",
"Scholz's Coalition on Brink of Collapse: Germany's CDU Opposition Seeks Confidence Vote",
"Germany's Political Crisis: Scholz Faces Confidence Vote after Finance Minister Dismissal",
"CDU Opposition Demands Confidence Vote in Germany as Coalition Crumbles Following Finance Minister's Departure",
"Scholz's Government on the Brink: CDU Seeks Confidence Vote Amid German Coalition Crisis",
"German Political Crisis: Scholz to Face Confidence Vote after Coalition Partner's Dismissal",
"Coalition Collapse: Germany's Scholz Faces Confidence Vote as CDU Calls for Action Following Finance Minister's Departure"
]
```

## PERPLEXITY_1
Here's a Python script using Faiss and the "sentence-transformers/all-MiniLM-L6-v2" model to find the 3 titles among the `title_proposals` that are most similar to the `best_title`:

```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load the pre-trained model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Define the best title and the title proposals
best_title = "German opposition demands confidence vote next week as Scholz's coalition crumbles"

title_proposals = [
    "CDU Calls for Confidence Vote in Germany Amid Coalition Crisis Following Finance Minister's Dismissal",
    "Olaf Scholz Faces Confidence Vote as German Coalition Collapses After Finance Minister's Exit",
    "German Government Crisis: CDU Demands Confidence Vote after Finance Minister Dismissal",
    "Coalition Crumbles: Scholz Faces Confidence Vote as Germany's CDU Opposition Calls for Action",
    "Scholz's Coalition on Brink of Collapse: Germany's CDU Opposition Seeks Confidence Vote",
    "Germany's Political Crisis: Scholz Faces Confidence Vote after Finance Minister Dismissal",
    "CDU Opposition Demands Confidence Vote in Germany as Coalition Crumbles Following Finance Minister's Departure",
    "Scholz's Government on the Brink: CDU Seeks Confidence Vote Amid German Coalition Crisis",
    "German Political Crisis: Scholz to Face Confidence Vote after Coalition Partner's Dismissal",
    "Coalition Collapse: Germany's Scholz Faces Confidence Vote as CDU Calls for Action Following Finance Minister's Departure"
]

# Generate embeddings for the best title and title proposals
best_title_embedding = model.encode([best_title])[0]
proposal_embeddings = model.encode(title_proposals)

# Create a Faiss index
d = best_title_embedding.shape[0]  # Dimensionality of the embeddings
index = faiss.IndexFlatL2(d)

# Add the proposal embeddings to the index
index.add(proposal_embeddings)

# Perform the search
k = 3  # Number of nearest neighbors to retrieve
D, I = index.search(best_title_embedding.reshape(1, -1), k)

# Get the top 3 most similar titles
top_3_titles = [title_proposals[i] for i in I[0]]

print("Top 3 most similar titles:")
for i, title in enumerate(top_3_titles, 1):
    print(f"{i}. {title}")
```

This script does the following:

1. It loads the "sentence-transformers/all-MiniLM-L6-v2" model[1][4].
2. It generates embeddings for the `best_title` and all `title_proposals` using the loaded model[1].
3. It creates a Faiss index and adds the embeddings of the title proposals to it[1][5].
4. It performs a similarity search using the embedding of the `best_title` to find the 3 most similar titles from the proposals[1][3].
5. Finally, it prints the top 3 most similar titles.

This approach uses semantic similarity to find the best matching titles, which should provide more accurate results than simple string matching[3].

Citations:
[1] https://www.stephendiehl.com/posts/faiss/
[2] https://discuss.huggingface.co/t/different-embeddings-when-using-sentence-transformers-and-transformers-js/73345
[3] https://www.sbert.net/examples/applications/semantic-search/README.html
[4] https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
[5] https://python.langchain.com/v0.1/docs/integrations/vectorstores/faiss/
[6] https://www.linkedin.com/posts/koushikkhan_sentence-transformersall-minilm-l6-v2-activity-7259924959190220800-sRIu


## PROMPT_2
Can you change the script in order to add an index to measure the similarity

## PERPLEXITY_2
Certainly! I'll modify the script to include a similarity score for each of the top 3 titles. We'll use cosine similarity as our metric, which is a common choice for measuring the similarity between embeddings. Here's the updated script:

```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load the pre-trained model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Define the best title and the title proposals
best_title = "German opposition demands confidence vote next week as Scholz's coalition crumbles"

title_proposals = [
    "CDU Calls for Confidence Vote in Germany Amid Coalition Crisis Following Finance Minister's Dismissal",
    "Olaf Scholz Faces Confidence Vote as German Coalition Collapses After Finance Minister's Exit",
    "German Government Crisis: CDU Demands Confidence Vote after Finance Minister Dismissal",
    "Coalition Crumbles: Scholz Faces Confidence Vote as Germany's CDU Opposition Calls for Action",
    "Scholz's Coalition on Brink of Collapse: Germany's CDU Opposition Seeks Confidence Vote",
    "Germany's Political Crisis: Scholz Faces Confidence Vote after Finance Minister Dismissal",
    "CDU Opposition Demands Confidence Vote in Germany as Coalition Crumbles Following Finance Minister's Departure",
    "Scholz's Government on the Brink: CDU Seeks Confidence Vote Amid German Coalition Crisis",
    "German Political Crisis: Scholz to Face Confidence Vote after Coalition Partner's Dismissal",
    "Coalition Collapse: Germany's Scholz Faces Confidence Vote as CDU Calls for Action Following Finance Minister's Departure"
]

# Generate embeddings for the best title and title proposals
best_title_embedding = model.encode([best_title])[0]
proposal_embeddings = model.encode(title_proposals)

# Create a Faiss index
d = best_title_embedding.shape[0]  # Dimensionality of the embeddings
index = faiss.IndexFlatL2(d)

# Add the proposal embeddings to the index
index.add(proposal_embeddings)

# Perform the search
k = 3  # Number of nearest neighbors to retrieve
D, I = index.search(best_title_embedding.reshape(1, -1), k)

# Calculate cosine similarity for the top 3 titles
similarities = cosine_similarity(best_title_embedding.reshape(1, -1), proposal_embeddings[I[0]])

# Get the top 3 most similar titles with their similarity scores
top_3_titles = [(title_proposals[i], similarities[0][j]) for j, i in enumerate(I[0])]

print("Top 3 most similar titles with similarity scores:")
for i, (title, score) in enumerate(top_3_titles, 1):
    print(f"{i}. {title}")
    print(f"   Similarity score: {score:.4f}")
    print()
```

This updated script includes the following changes:

1. We import `cosine_similarity` from `sklearn.metrics.pairwise` to calculate the similarity scores.

2. After finding the top 3 most similar titles using Faiss, we calculate the cosine similarity between the `best_title_embedding` and the embeddings of the top 3 titles.

3. We create a list of tuples `top_3_titles` that contains both the title and its corresponding similarity score.

4. In the output, we print each title along with its similarity score, rounded to 4 decimal places.

This modification allows you to see not only which titles are most similar but also how similar they are quantitatively. The cosine similarity scores range from -1 to 1, where 1 indicates perfect similarity, 0 indicates no similarity, and -1 indicates perfect dissimilarity (though negative values are rare with text embeddings).