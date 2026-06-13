## PROMPT_3

Give a wikidata definition in English for "Epoch" plus a set for "subclass of", "uses". Add also "aliases" with a pipe | separated list. Give an answer that eases the cut and paste of each element of the answer. No explanations just say the essential. Advise also how to add the official URL. Do not forget to remind the ID on wikidata for "subclass of" and "uses" e.g Subclass of: (P279), Uses: (P2283). In order to avoid duplicates, advice on a strategy to promote disambiguation is important. The description should clearly state something to distinguish it.

- source of definition
Complete pass through the entire training dataset. A model is typically trained over multiple epochs.

Print the result as plain text ```text...``` and not as a readme file by removing all tags like `**`, `##`, etc.


## A_PROMPT_3

```text
Label:
Epoch (machine learning)

Aliases:
Training Epoch | ML Epoch | Epoch (deep learning) | Epoch (neural network training)

Description:
Single complete pass through an entire training dataset during the training
of a machine learning or deep neural network model; models are typically
trained over multiple successive epochs to minimize loss and improve accuracy.

---

Subclass of (P279):
- training iteration (Q) → may need to be created
- machine learning concept (Q Q485396)
- hyperparameter (Q) → may need to be created

---

Uses (P2283):
- machine learning (Q2539)
- deep learning (Q197536)
- neural network (Q192776)
- stochastic gradient descent (Q901543)
- loss function (Q3027902)

---

Official website (P856):
No dedicated URL — concept defined at https://ludwig.ai/latest/ and
general ML glossaries. Use a reference (P854) pointing to a reputable
source such as https://developers.google.com/machine-learning/glossary#epoch

---

Disambiguation strategy:
- Use label "Epoch (machine learning)" not bare "Epoch" to avoid collision
  with Unix epoch (Q1263714), geological epoch (Q226995), Epoch magazine, etc.
- Add the qualifier "applies to part" or a haswbstatement distinguishing
  it from Q1263714 (Unix time) and Q226995 (geological epoch).
- Search before creating:
  https://www.wikidata.org/w/index.php?search=Epoch+machine+learning
- In the description, always include the qualifier "(machine learning)"
  as the first disambiguating term.
```


## PROMPT_2

Give a wikidata definition in english for "Ludwig" plus a set for "subclass of", "uses". Add also "aliases" with a pipe | separated list. Give an answer that eases the cut and paste of each element of the answer. No explanations just say the essential. Advise also how to add the official URL. Do not forget to remind the ID on wikidata for "subclass of" and "uses" e.g Subclass of: (P279), Uses: (P2283).

- source of definition
Ludwig is a low-code framework for building custom AI models like LLMs and other deep neural networks.



Source : https://ludwig.ai/latest/



## A_PROMPT_2

**Label:**
Ludwig

**Aliases:**
Ludwig AI | Ludwig Framework | Ludwig Low-Code AI | Uber Ludwig

**Description:**
Open-source low-code Python framework for building, training and deploying custom AI models including large language models and deep neural networks, without requiring extensive machine learning expertise.

---

**Subclass of (P279):**
- machine learning framework (Q107517065)
- software framework (Q271668)
- free and open-source software (Q341)

---

**Uses (P2283):**
- Python (Q28865)
- deep learning (Q197536)
- large language model (Q107520748)
- neural network (Q192776)
- AutoML (Q114633987)

---

**Official website (P856):**
`https://ludwig.ai/latest/`

---

**To add the official URL:**
On the Wikidata item page, add a statement with property **official website (P856)** and value `https://ludwig.ai/latest/`

> **Note:** Search `https://www.wikidata.org/w/index.php?search=Ludwig+AI` before creating a new item to avoid duplicates — "Ludwig" is a common name (composer, king) so disambiguation is important. The description should clearly state "AI framework" to distinguish it.


## PROMPT_1

Give a wikidata definition in english for "NLTK" plus a set for "subclass of", "uses". Add also "aliases" with a pipe | separated list. Give an answer that eases the cut and paste of each element of the answer. No explanations just say the essential. Advise also how to add the official URL. Do not forget to remind the ID on wikidata for "subclass of" and "uses" e.g Subclass of: (P279), Uses: (P2283).

- source of definition
NLTK is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum.

Source : https://www.nltk.org/

## A_PROMPT_1

**Label:**
NLTK

**Aliases:**
Natural Language Toolkit | NLTK Python | Python NLP Library | Natural Language Processing Toolkit

**Description:**
Open-source Python platform for building natural language processing programs, providing interfaces to corpora and lexical resources, text processing libraries for classification, tokenization, stemming, tagging, parsing and semantic reasoning.

---

**Subclass of (P279):**
- natural language processing toolkit (Q107520748)
- software library (Q188860)
- free and open-source software (Q341)

---

**Uses (P2283):**
- Python (Q28865)
- WordNet (Q223469)
- natural language processing (Q30642)
- tokenization (Q1070681)
- text corpus (Q1700246)

---

**Official website (P856):**
`https://www.nltk.org/`

---

**To add the official URL:**
On the Wikidata item page, add a statement with property **official website (P856)** and value `https://www.nltk.org/`

> **Note:** NLTK likely already has a Wikidata entry. Search `https://www.wikidata.org/w/index.php?search=NLTK` before creating a new item to avoid duplicates.


## DEPOT
-- source
AI, artificial intelligence, categorization, CMS, coding, Deep Learning, epoch, experimentation, IA, language, Ludwig, Machine Learning, Natural language processing, neural networks, NTLK, numpy, P.O, python, TensorFlow, TensorFlow Keras, toolbox, visualization

-- todo
--- NTLK (done)
Ludwig (artificial intelligence)
epoch (artificial intelligence) (machine learning)
epoch (machine learning)
neural network library

Complete pass through the entire training dataset. A model is typically trained over multiple epochs.





