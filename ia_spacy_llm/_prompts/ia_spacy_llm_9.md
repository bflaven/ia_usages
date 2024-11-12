# ia_spacy_llm_9.md

As IA and Python expert, rewrite the script below using best practices and function and a class if needed. Just preserve the variables so it can be easily changed.


```python
from sentence_transformers import SentenceTransformer, util

# Load the model
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
# Define the best keywords and the keywords combinations
best_keywords = ["Germany", "Olaf Scholz", "CDU", "Ukraine"]

keywords_combinations = [
["Germany", "CDU", "Olaf Scholz", "confidence vote"],
["Germany", "coalition crisis", "Scholz", "confidence vote"],
["Olaf Scholz", "Germany", "CDU", "confidence vote"],
["CDU", "Germany", "Scholz", "confidence vote"],
["Germany", "coalition", "Scholz", "confidence vote"],
["CDU", "Germany", "Scholz", "confidence vote"],
["finance minister", "Germany", "Scholz", "confidence vote"],
["dismissal", "Germany", "Scholz", "confidence vote"],
["Germany", "political crisis", "Scholz", "confidence vote"],
["coalition partner's departure", "Germany", "Scholz", "confidence vote"]
]


#### TITLES
print('\n### TITLES')
# Compute the embeddings for the best title and the title proposals
best_title_embedding = model.encode(best_title, convert_to_tensor=True)
title_proposals_embeddings = model.encode(title_proposals, convert_to_tensor=True)

# Compute the cosine similarities between the best title and the title proposals
cosine_scores = util.cos_sim(best_title_embedding, title_proposals_embeddings)

# Sort the title proposals by the highest cosine similarity score with the best title
sorted_title_proposals = sorted(zip(title_proposals, cosine_scores[0]), key=lambda x: x[1], reverse=True)


print('\n--- result_1: sorted title proposals')
# Print the sorted title proposals
for title, score in sorted_title_proposals:
    print(f"Title: {title} | Score: {score:.4f}")

# Filter and print the sorted title proposals where the score is >= 0.5000
filtered_title_proposals = [(title, score) for title, score in sorted_title_proposals if score >= 0.5000]

print('\n--- result_2: sorted title proposals where score is >= 0.5000')
for title, score in filtered_title_proposals:
    print(f"Title: {title} | Score: {score:.4f}")


#### KEYWORDS 
print('\n### KEYWORDS')
# Compute the embeddings for the best keywords and the keywords combinations
best_keywords_embedding = model.encode(" ".join(best_keywords), convert_to_tensor=True)
keywords_combinations_embeddings = [model.encode(" ".join(combination), convert_to_tensor=True) for combination in keywords_combinations]

# Compute the cosine similarities between the best keywords and the keywords combinations
cosine_scores = [util.cos_sim(best_keywords_embedding, combination_embedding) for combination_embedding in keywords_combinations_embeddings]

# Sort the keywords combinations by the highest cosine similarity score with the best keywords
sorted_keywords_combinations = sorted(zip(keywords_combinations, cosine_scores), key=lambda x: x[1], reverse=True)

print('\n--- result_1: sorted keywords combinations')
# Print the sorted keywords combinations
for combination, score in sorted_keywords_combinations:
    print(f"Combination: {combination} | Score: {score.item():.4f}")

print('\n--- result_2: sorted keywords combinations where score is >= 0.5000')
# Filter and print the sorted keywords combinations where the score is >= 0.5000
filtered_keywords_combinations = [(combination, score) for combination, score in sorted_keywords_combinations if score.item() >= 0.5000]

for combination, score in filtered_keywords_combinations:
    print(f"Combination: {combination} | Score: {score.item():.4f}")


```

## MISTRAL

Here's a refactored version of the script that uses a class to encapsulate the functionality and makes it easier to change the variables.

```python
from sentence_transformers import SentenceTransformer, util

class TitleAndKeywordAnalyzer:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def analyze_titles(self, best_title, title_proposals, threshold=0.5000):
        print('\n### TITLES')
        best_title_embedding = self.model.encode(best_title, convert_to_tensor=True)
        title_proposals_embeddings = self.model.encode(title_proposals, convert_to_tensor=True)
        cosine_scores = util.cos_sim(best_title_embedding, title_proposals_embeddings)
        sorted_title_proposals = sorted(zip(title_proposals, cosine_scores[0]), key=lambda x: x[1], reverse=True)
        self._print_results(sorted_title_proposals, threshold)

    def analyze_keywords(self, best_keywords, keywords_combinations, threshold=0.5000):
        print('\n### KEYWORDS')
        best_keywords_embedding = self.model.encode(" ".join(best_keywords), convert_to_tensor=True)
        keywords_combinations_embeddings = [self.model.encode(" ".join(combination), convert_to_tensor=True) for combination in keywords_combinations]
        cosine_scores = [util.cos_sim(best_keywords_embedding, combination_embedding) for combination_embedding in keywords_combinations_embeddings]
        sorted_keywords_combinations = sorted(zip(keywords_combinations, cosine_scores), key=lambda x: x[1], reverse=True)
        self._print_results(sorted_keywords_combinations, threshold)

    def _print_results(self, sorted_items, threshold):
        print('\n--- result_1: sorted items')
        for item, score in sorted_items:
            print(f"Item: {item} | Score: {score.item():.4f}")

        print(f'\n--- result_2: sorted items where score is >= {threshold}')
        filtered_items = [(item, score) for item, score in sorted_items if score.item() >= threshold]
        for item, score in filtered_items:
            print(f"Item: {item} | Score: {score.item():.4f}")

# Define the variables
best_title = "German opposition demands confidence vote next week as Scholz's coalition crumbles"
title_proposals = [
    "CDU Calls for Confidence Vote in Germany Amid Coalition Crisis Following Finance Minister's Dismissal",
    # ... other titles ...
]
best_keywords = ["Germany", "Olaf Scholz", "CDU", "Ukraine"]
keywords_combinations = [
    ["Germany", "CDU", "Olaf Scholz", "confidence vote"],
    # ... other combinations ...
]

# Create an instance of the class and use it to analyze the titles and keywords
analyzer = TitleAndKeywordAnalyzer()
analyzer.analyze_titles(best_title, title_proposals)
analyzer.analyze_keywords(best_keywords, keywords_combinations)
```

This version of the script encapsulates the functionality in a class called `TitleAndKeywordAnalyzer`. The class has two methods: `analyze_titles` and `analyze_keywords`, which take the best title/keywords and the proposals/combinations as input and print the sorted and filtered results. The `_print_results` method is a helper method that prints the sorted items and the filtered items based on a threshold score.

The variables are defined outside the class, so they can be easily changed. To use the class, you create an instance of it and then call the `analyze_titles` and `analyze_keywords` methods with the appropriate variables.




