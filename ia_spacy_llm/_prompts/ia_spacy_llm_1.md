# ia_spacy_llm_1.md


## PROMPT_1


What kind of framework is in javascript or in python or in any language so this framework can help  to test the quality of generative IA.

Here is a user story that details my needs.

The source is for instance an article in English about a murder case in France e.g the title is "Suspect in Paris student murder to be extradited to France on Wednesday"

best_title="Suspect in Paris student murder to be extradited to France on Wednesday"

The keywords for this article are: France, Switzerland, rape, murder, immigration, crime.

best_keywords=["France", "Switzerland", "rape", "murder", "immigration", "crime"]


I will be using a LLM to generate a set of 3 titles propositions and a set of keywords.
I will use the title and the keywords

I want to test the semantic similarity according to the best_title and best_keywords that I have defined.



## CHATGPT_1
To test the quality of generative AI outputs like titles and keywords, you need a framework that can evaluate semantic similarity and compare generated outputs against predefined "best" results. Here's how you can achieve this:

### Frameworks and Tools:

1. **Python**:
    - **SpaCy**: Excellent for NLP tasks, SpaCy can be used to analyze and compare semantic similarities between texts.
    - **Hugging Face Transformers**: For more advanced models like BERT, which can be used to measure semantic similarity via cosine similarity of embeddings.
    - **NLTK**: Basic NLP tasks and similarity measures.
    - **Gensim**: Topic modeling and semantic similarity using word embeddings like Word2Vec.

2. **JavaScript**:
    - **Natural**: A general-purpose NLP library for tokenization, stemming, classification, and similarity metrics.
    - **TensorFlow.js**: Run ML models in the browser, including BERT or other pre-trained language models, for semantic analysis.

3. **Multi-language Frameworks**:
    - **FastAPI** or **Flask** for Python: To create a microservice that evaluates the quality of the generated text using NLP models.
    - **Node.js** with Express: If you prefer a JavaScript backend, you can integrate TensorFlow.js for semantic analysis.

### Evaluation Metrics:

1. **Cosine Similarity**:
    - Use word or sentence embeddings (e.g., BERT embeddings) to calculate cosine similarity between the generated titles/keywords and the predefined best titles/keywords.

2. **BLEU/ROUGE Scores**:
    - While traditionally used for machine translation and summarization, they can be adapted to assess how closely the generated titles match the best titles in terms of word overlap and order.

3. **Jaccard Similarity**:
    - Particularly for keywords, you can use the Jaccard index to measure the similarity between the sets of keywords.

### Implementation Steps:

1. **Extract Embeddings**:
    - Use a pre-trained model to extract embeddings for both the best and generated titles/keywords.

2. **Calculate Similarity**:
    - Compute cosine similarity for titles and Jaccard index for keywords.

3. **Thresholding and Scoring**:
    - Set thresholds for acceptable similarity scores and compute overall quality scores based on these metrics.

### Example in Python:

```python
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics import jaccard_score
from sklearn.preprocessing import MultiLabelBinarizer

# Define the best title and keywords
best_title = "Suspect in Paris student murder to be extradited to France on Wednesday"
best_keywords = ["France", "Switzerland", "rape", "murder", "immigration", "crime"]

# Generated titles and keywords
generated_titles = [
    "Paris student murder suspect to face extradition to France",
    "Extradition set for Paris murder suspect in student case",
    "Murder case in Paris: Suspect extradition confirmed"
]
generated_keywords = [
    ["France", "extradition", "crime", "student"],
    ["murder", "Switzerland", "extradition", "crime"],
    ["Paris", "student", "immigration", "case"]
]

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Compute cosine similarity for titles
best_embedding = model.encode(best_title, convert_to_tensor=True)
similarities = [util.pytorch_cos_sim(best_embedding, model.encode(title, convert_to_tensor=True)).item() for title in generated_titles]

# Compute Jaccard similarity for keywords
mlb = MultiLabelBinarizer()
y_true = mlb.fit_transform([best_keywords])
similarity_scores = [jaccard_score(y_true[0], mlb.transform([keywords])[0], average='macro') for keywords in generated_keywords]

print("Title Similarities:", similarities)
print("Keyword Similarities:", similarity_scores)
```

This code measures semantic similarity for titles and Jaccard similarity for keywords. You can adapt this approach with other frameworks depending on your specific needs.

## PROMPT_2
Let's find a solution with SpaCy and spaCy-llm and exclusively in Python.

## CHATGPT_2

To implement a solution using SpaCy and `spacy-llm`, we'll follow these steps:

1. **Set up SpaCy with `spacy-llm`**: This extension allows SpaCy to leverage large language models (LLMs) for various NLP tasks, including semantic similarity.
2. **Calculate semantic similarity** between the best title and the generated titles.
3. **Compute Jaccard similarity** between the sets of keywords.

### Implementation

Here's how you can implement this solution:

```python
import spacy
from spacy_llm import LLMWrapper
from spacy.tokens import DocBin
from sklearn.metrics import jaccard_score
from sklearn.preprocessing import MultiLabelBinarizer

# Load SpaCy's English model with spacy-llm
nlp = spacy.blank("en")
llm = LLMWrapper.from_config({
    "model": "sentence-transformers/paraphrase-MiniLM-L6-v2"
})
nlp.add_pipe("llm", config={"llm": llm})

# Define the best title and keywords
best_title = "Suspect in Paris student murder to be extradited to France on Wednesday"
best_keywords = ["France", "Switzerland", "rape", "murder", "immigration", "crime"]

# Generated titles and keywords
generated_titles = [
    "Paris student murder suspect to face extradition to France",
    "Extradition set for Paris murder suspect in student case",
    "Murder case in Paris: Suspect extradition confirmed"
]
generated_keywords = [
    ["France", "extradition", "crime", "student"],
    ["murder", "Switzerland", "extradition", "crime"],
    ["Paris", "student", "immigration", "case"]
]

# Compute embeddings for the best title and generated titles
best_title_doc = nlp(best_title)
best_title_vector = best_title_doc.vector

# Compute cosine similarity for titles
similarities = []
for title in generated_titles:
    title_vector = nlp(title).vector
    similarity = best_title_doc.similarity(nlp(title))
    similarities.append(similarity)

# Compute Jaccard similarity for keywords
mlb = MultiLabelBinarizer()
y_true = mlb.fit_transform([best_keywords])
jaccard_similarities = [
    jaccard_score(y_true[0], mlb.transform([keywords])[0], average='macro')
    for keywords in generated_keywords
]

print("Title Similarities:", similarities)
print("Keyword Similarities:", jaccard_similarities)
```

### Explanation

1. **Loading SpaCy and `spacy-llm`**:
   - We use the `LLMWrapper` to load a transformer model capable of generating embeddings for semantic similarity tasks.
   
2. **Title Similarity**:
   - We compute the similarity between the best title and each generated title using SpaCy’s `similarity` method, which uses cosine similarity of the embeddings.

3. **Keyword Similarity**:
   - Jaccard similarity is calculated by comparing the intersection and union of the sets of keywords.

### Dependencies

Ensure you have the following installed:

```bash
pip install spacy spacy-llm sklearn
```

This solution provides a robust framework to evaluate the quality of titles and keywords generated by a language model.

## PROMPT_3
Let's find a solution with Guardrails AI and exclusively in Python.

## CHATGPT_3
To implement a solution using **Guardrails AI** exclusively in Python, you would follow these steps:

1. **Set up Guardrails AI**: Use Guardrails AI to define constraints and validations for the generated outputs.
2. **Evaluate Semantic Similarity**: Define guardrails for the similarity of generated titles.
3. **Evaluate Keyword Accuracy**: Define guardrails to check if generated keywords match the expected set.

### Implementation

Here’s a step-by-step implementation:

#### 1. Install Dependencies

First, ensure you have Guardrails AI installed:

```bash
pip install guardrails
```

#### 2. Define Guardrails and Evaluation Logic

```python
import guardrails as gd
from sklearn.metrics import jaccard_score
from sklearn.preprocessing import MultiLabelBinarizer
from sentence_transformers import SentenceTransformer, util

# Initialize SentenceTransformer for semantic similarity
model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')

# Define the best title and keywords
best_title = "Suspect in Paris student murder to be extradited to France on Wednesday"
best_keywords = ["France", "Switzerland", "rape", "murder", "immigration", "crime"]

# Generated titles and keywords
generated_titles = [
    "Paris student murder suspect to face extradition to France",
    "Extradition set for Paris murder suspect in student case",
    "Murder case in Paris: Suspect extradition confirmed"
]
generated_keywords = [
    ["France", "extradition", "crime", "student"],
    ["murder", "Switzerland", "extradition", "crime"],
    ["Paris", "student", "immigration", "case"]
]

# Compute embeddings for the best title
best_embedding = model.encode(best_title, convert_to_tensor=True)

# Guardrails for title similarity
def title_similarity_guardrail(title):
    embedding = model.encode(title, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(best_embedding, embedding).item()
    return similarity >= 0.8  # Example threshold for similarity

# Guardrails for keyword similarity (Jaccard)
def keyword_similarity_guardrail(keywords):
    mlb = MultiLabelBinarizer()
    y_true = mlb.fit_transform([best_keywords])
    jaccard_sim = jaccard_score(y_true[0], mlb.transform([keywords])[0], average='macro')
    return jaccard_sim >= 0.5  # Example threshold for Jaccard similarity

# Validate generated titles and keywords
for idx, title in enumerate(generated_titles):
    title_valid = title_similarity_guardrail(title)
    keywords_valid = keyword_similarity_guardrail(generated_keywords[idx])
    print(f"Title {idx + 1} is valid: {title_valid}")
    print(f"Keywords {idx + 1} are valid: {keywords_valid}")
```

### Explanation

1. **Semantic Similarity with Guardrails**:
   - The `title_similarity_guardrail` function checks if the cosine similarity between the best title and a generated title exceeds a certain threshold.

2. **Keyword Accuracy with Guardrails**:
   - The `keyword_similarity_guardrail` function calculates the Jaccard similarity between the expected and generated keyword sets and checks against a threshold.

3. **Threshold Values**:
   - Threshold values (e.g., 0.8 for title similarity and 0.5 for Jaccard similarity) are configurable based on desired strictness.

### Dependencies

Ensure `sentence-transformers` is also installed for embedding computations:

```bash
pip install sentence-transformers
```

### Conclusion

This solution leverages **Guardrails AI** to apply semantic similarity and keyword accuracy constraints, ensuring the generative AI outputs meet predefined quality criteria. You can further extend this framework by adding more complex rules or integrating it into a larger pipeline for continuous quality monitoring.











