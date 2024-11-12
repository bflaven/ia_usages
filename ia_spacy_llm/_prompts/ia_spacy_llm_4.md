# ia_spacy_llm_4.md


## PROMPT_1

As IA and Python expert, write a script that use "model" to load "SentenceTransformer" so it compute the cosine similarity  between "best_title" and each of the ten "Title Proposals" then sort the list of the ten "Title Proposals" by the highest cosine similarity score with the "best_title". In the script use the elements below that are defined.

```python
best_title="Suspect in Paris student murder to be extradited to France on Wednesday"
```


```python
from sentence_transformers import SentenceTransformer, util

# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
```

```text
Title Proposals:
1. Moroccan National Charged with Paris Student Murder to be Extradited from Switzerland
2. France Demands Extradition of Suspect in Paris University Student Homicide Case
3. Swiss Authorities to Hand Over Suspect in Paris Student Rape and Murder Case to France
4. French Request for Extradition of Alleged Paris Student Killer Granted by Swiss Courts
5. Illegal Immigrant Accused of Paris University Student Rape and Murder to be Extradited
6. Suspected Paris University Student Rapist and Murderer to Face Justice in France
7. Crackdown on Crime: French Authorities Seek Extradition of Moroccan National for Paris Homicide
8. Femicide in Paris: Swiss Courts Approve Extradition of Alleged Killer to France
9. Paris Student Murder Suspect to be Extradited from Switzerland amid Immigration Debate
10. Switz-French Cooperation: Extradition of Moroccan National for Paris University Student Murder
```

## MISTRAL_1 (codestral)


Here is the Python script that uses the SentenceTransformer model to compute the cosine similarity between the `best_title` and each of the ten `Title Proposals`. The script then sorts the list of the ten `Title Proposals` by the highest cosine similarity score with the `best_title`.

```python
from sentence_transformers import SentenceTransformer, util

# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Define the best title and the title proposals
best_title = "Suspect in Paris student murder to be extradited to France on Wednesday"
title_proposals = [
    "Moroccan National Charged with Paris Student Murder to be Extradited from Switzerland",
    "France Demands Extradition of Suspect in Paris University Student Homicide Case",
    "Swiss Authorities to Hand Over Suspect in Paris Student Rape and Murder Case to France",
    "French Request for Extradition of Alleged Paris Student Killer Granted by Swiss Courts",
    "Illegal Immigrant Accused of Paris University Student Rape and Murder to be Extradited",
    "Suspected Paris University Student Rapist and Murderer to Face Justice in France",
    "Crackdown on Crime: French Authorities Seek Extradition of Moroccan National for Paris Homicide",
    "Femicide in Paris: Swiss Courts Approve Extradition of Alleged Killer to France",
    "Paris Student Murder Suspect to be Extradited from Switzerland amid Immigration Debate",
    "Switz-French Cooperation: Extradition of Moroccan National for Paris University Student Murder"
]

# Compute the embeddings for the best title and the title proposals
best_title_embedding = model.encode(best_title, convert_to_tensor=True)
title_proposals_embeddings = model.encode(title_proposals, convert_to_tensor=True)

# Compute the cosine similarities between the best title and the title proposals
cosine_scores = util.cos_sim(best_title_embedding, title_proposals_embeddings)

# Sort the title proposals by the highest cosine similarity score with the best title
sorted_title_proposals = sorted(zip(title_proposals, cosine_scores[0]), key=lambda x: x[1], reverse=True)

# Print the sorted title proposals
for title, score in sorted_title_proposals:
    print(f"Title: {title} | Score: {score:.4f}")
```

This script uses the `sentence-transformers` library to compute the embeddings of the sentences and then calculates the cosine similarity between the embeddings. The `util.cos_sim` function from the `sentence-transformers` library is used to compute the cosine similarity. Finally, the script sorts the title proposals by the highest cosine similarity score with the best title using the `sorted` function with a custom key.


## PROMPT_2
Do the same but for keywords but with the following elements and return the best combinaison as an pyhton object.

```python
best_keywords=["France", "Switzerland", "rape", "murder", "immigration", "crime"]
```


```python
from sentence_transformers import SentenceTransformer, util

# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
```

```text
Keywords:
1. France, Switzerland, extradition, murder, rape, student, Paris, illegal immigration, crime, femicide, 
politicians, rights groups.
2. Extradition, France, Switzerland, Paris, university student, murder, Moroccan national, illegal immigration, 
crime, femicide, politics.
3. Swiss Courts, French Request, Paris Student Murder, Extradition, Immigration Debate, Crime, Moroccan National.
4. Paris Homicide, Extradition, French Authorities, Moroccan National, Switzerland, Illegal Immigration, Femicide.
5. Paris University Student, Rape and Murder, Suspect, Extradition, France, Switzerland, Illegal Immigrant.
6. Femicide, Paris, Student, Moroccan National, Extradition, France, Switzerland, Crackdown on Crime.
7. Paris Student Killer, Extradition, Moroccan National, Switzerland, France, Crime, Politics, Femicide.
8. French Politicians, Paris University Student Murder, Moroccan National, Swiss Courts, Extradition, Femicide.
9. Swiss Authorities, Paris University Student Rape and Murder, Extradition, Moroccan National, France, Immigration 
Debate.
10. Paris Homicide, Moroccan National, Extradition, Switzerland, France, Illegal Immigration, Femicide, Politics.
```


## MISTRAL_2 (codestral)

Here is the Python script that uses the SentenceTransformer model to compute the cosine similarity between the `best_keywords` and each of the ten `Keywords` combinations. The script then sorts the list of the ten `Keywords` combinations by the highest cosine similarity score with the `best_keywords` and returns the best combination as a Python object.

```python
from sentence_transformers import SentenceTransformer, util
from itertools import combinations

# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Define the best keywords and the keywords combinations
best_keywords = ["France", "Switzerland", "rape", "murder", "immigration", "crime"]
keywords_combinations = [
    ["France", "Switzerland", "extradition", "murder", "rape", "student", "Paris", "illegal immigration", "crime", "femicide", "politicians", "rights groups"],
    ["Extradition", "France", "Switzerland", "Paris", "university student", "murder", "Moroccan national", "illegal immigration", "crime", "femicide", "politics"],
    ["Swiss Courts", "French Request", "Paris Student Murder", "Extradition", "Immigration Debate", "Crime", "Moroccan National"],
    ["Paris Homicide", "Extradition", "French Authorities", "Moroccan National", "Switzerland", "Illegal Immigration", "Femicide"],
    ["Paris University Student", "Rape and Murder", "Suspect", "Extradition", "France", "Switzerland", "Illegal Immigrant"],
    ["Femicide", "Paris", "Student", "Moroccan National", "Extradition", "France", "Switzerland", "Crackdown on Crime"],
    ["Paris Student Killer", "Extradition", "Moroccan National", "Switzerland", "France", "Crime", "Politics", "Femicide"],
    ["French Politicians", "Paris University Student Murder", "Moroccan National", "Swiss Courts", "Extradition", "Femicide"],
    ["Swiss Authorities", "Paris University Student Rape and Murder", "Extradition", "Moroccan National", "France", "Immigration Debate"],
    ["Paris Homicide", "Moroccan National", "Extradition", "Switzerland", "France", "Illegal Immigration", "Femicide", "Politics"]
]

# Compute the embeddings for the best keywords and the keywords combinations
best_keywords_embedding = model.encode(" ".join(best_keywords), convert_to_tensor=True)
keywords_combinations_embeddings = [model.encode(" ".join(combination), convert_to_tensor=True) for combination in keywords_combinations]

# Compute the cosine similarities between the best keywords and the keywords combinations
cosine_scores = [util.cos_sim(best_keywords_embedding, combination_embedding) for combination_embedding in keywords_combinations_embeddings]

# Sort the keywords combinations by the highest cosine similarity score with the best keywords
sorted_keywords_combinations = sorted(zip(keywords_combinations, cosine_scores), key=lambda x: x[1], reverse=True)

# Return the best combination as a Python object
best_combination = sorted_keywords_combinations[0][0]
print(f"Best combination: {best_combination}")
```

This script uses the `sentence-transformers` library to compute the embeddings of the sentences and then calculates the cosine similarity between the embeddings. The `util.cos_sim` function from the `sentence-transformers` library is used to compute the cosine similarity. The script then sorts the keywords combinations by the highest cosine similarity score with the best keywords using the `sorted` function with a custom key. Finally, the script returns the best combination as a Python object.



## PROMPT_3
As IA and Python expert, rewrite the script that use "model" to load "SentenceTransformer" so it compute the cosine similarity  between "best_keywords" and each "keywords_combinations" then sort the list of the ten "keywords_combinations" by the highest cosine similarity score with the "best_keywords".



## MISTRAL_3 (codestral)

Here is the rewritten Python script that uses the SentenceTransformer model to compute the cosine similarity between the `best_keywords` and each `keywords_combinations`. The script then sorts the list of the ten `keywords_combinations` by the highest cosine similarity score with the `best_keywords`.

```python
from sentence_transformers import SentenceTransformer, util

# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Define the best keywords and the keywords combinations
best_keywords = ["France", "Switzerland", "rape", "murder", "immigration", "crime"]
keywords_combinations = [
    ["France", "Switzerland", "extradition", "murder", "rape", "student", "Paris", "illegal immigration", "crime", "femicide", "politicians", "rights groups"],
    ["Extradition", "France", "Switzerland", "Paris", "university student", "murder", "Moroccan national", "illegal immigration", "crime", "femicide", "politics"],
    ["Swiss Courts", "French Request", "Paris Student Murder", "Extradition", "Immigration Debate", "Crime", "Moroccan National"],
    ["Paris Homicide", "Extradition", "French Authorities", "Moroccan National", "Switzerland", "Illegal Immigration", "Femicide"],
    ["Paris University Student", "Rape and Murder", "Suspect", "Extradition", "France", "Switzerland", "Illegal Immigrant"],
    ["Femicide", "Paris", "Student", "Moroccan National", "Extradition", "France", "Switzerland", "Crackdown on Crime"],
    ["Paris Student Killer", "Extradition", "Moroccan National", "Switzerland", "France", "Crime", "Politics", "Femicide"],
    ["French Politicians", "Paris University Student Murder", "Moroccan National", "Swiss Courts", "Extradition", "Femicide"],
    ["Swiss Authorities", "Paris University Student Rape and Murder", "Extradition", "Moroccan National", "France", "Immigration Debate"],
    ["Paris Homicide", "Moroccan National", "Extradition", "Switzerland", "France", "Illegal Immigration", "Femicide", "Politics"]
]

# Compute the embeddings for the best keywords and the keywords combinations
best_keywords_embedding = model.encode(" ".join(best_keywords), convert_to_tensor=True)
keywords_combinations_embeddings = [model.encode(" ".join(combination), convert_to_tensor=True) for combination in keywords_combinations]

# Compute the cosine similarities between the best keywords and the keywords combinations
cosine_scores = [util.cos_sim(best_keywords_embedding, combination_embedding) for combination_embedding in keywords_combinations_embeddings]

# Sort the keywords combinations by the highest cosine similarity score with the best keywords
sorted_keywords_combinations = sorted(zip(keywords_combinations, cosine_scores), key=lambda x: x[1], reverse=True)

# Print the sorted keywords combinations
for combination, score in sorted_keywords_combinations:
    print(f"Combination: {combination} | Score: {score:.4f}")
```

This script uses the `sentence-transformers` library to compute the embeddings of the sentences and then calculates the cosine similarity between the embeddings. The `util.cos_sim` function from the `sentence-transformers` library is used to compute the cosine similarity. The script then sorts the keywords combinations by the highest cosine similarity score with the best keywords using the `sorted` function with a custom key. Finally, the script prints the sorted keywords combinations.

## PROMPT_4

Got an error for the script "TypeError: unsupported format string passed to Tensor.__format__"

## MISTRAL_4 (codestral)

The error message "TypeError: unsupported format string passed to Tensor.__format__" usually occurs when you try to format a PyTorch tensor using a format string that is not supported.

In the script, the error might be occurring when you try to print the cosine similarity score using the format string `{score:.4f}`. To fix this error, you can convert the tensor to a Python float before formatting it.

Here is the updated script with the fix:

```python
from sentence_transformers import SentenceTransformer, util

# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Define the best keywords and the keywords combinations
best_keywords = ["France", "Switzerland", "rape", "murder", "immigration", "crime"]
keywords_combinations = [
    ["France", "Switzerland", "extradition", "murder", "rape", "student", "Paris", "illegal immigration", "crime", "femicide", "politicians", "rights groups"],
    ["Extradition", "France", "Switzerland", "Paris", "university student", "murder", "Moroccan national", "illegal immigration", "crime", "femicide", "politics"],
    ["Swiss Courts", "French Request", "Paris Student Murder", "Extradition", "Immigration Debate", "Crime", "Moroccan National"],
    ["Paris Homicide", "Extradition", "French Authorities", "Moroccan National", "Switzerland", "Illegal Immigration", "Femicide"],
    ["Paris University Student", "Rape and Murder", "Suspect", "Extradition", "France", "Switzerland", "Illegal Immigrant"],
    ["Femicide", "Paris", "Student", "Moroccan National", "Extradition", "France", "Switzerland", "Crackdown on Crime"],
    ["Paris Student Killer", "Extradition", "Moroccan National", "Switzerland", "France", "Crime", "Politics", "Femicide"],
    ["French Politicians", "Paris University Student Murder", "Moroccan National", "Swiss Courts", "Extradition", "Femicide"],
    ["Swiss Authorities", "Paris University Student Rape and Murder", "Extradition", "Moroccan National", "France", "Immigration Debate"],
    ["Paris Homicide", "Moroccan National", "Extradition", "Switzerland", "France", "Illegal Immigration", "Femicide", "Politics"]
]

# Compute the embeddings for the best keywords and the keywords combinations
best_keywords_embedding = model.encode(" ".join(best_keywords), convert_to_tensor=True)
keywords_combinations_embeddings = [model.encode(" ".join(combination), convert_to_tensor=True) for combination in keywords_combinations]

# Compute the cosine similarities between the best keywords and the keywords combinations
cosine_scores = [util.cos_sim(best_keywords_embedding, combination_embedding) for combination_embedding in keywords_combinations_embeddings]

# Sort the keywords combinations by the highest cosine similarity score with the best keywords
sorted_keywords_combinations = sorted(zip(keywords_combinations, cosine_scores), key=lambda x: x[1], reverse=True)

# Print the sorted keywords combinations
for combination, score in sorted_keywords_combinations:
    print(f"Combination: {combination} | Score: {score.item():.4f}")
```

In this updated script, I added `.item()` to the `score` variable when printing it, which converts the tensor to a Python float. This should fix the error you were encountering.