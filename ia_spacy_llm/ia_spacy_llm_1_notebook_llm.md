# ia_spacy_llm_1_notebook_llm.md

**made with notebooklm**

The provided text explores the author's concerns about the potential downsides of artificial intelligence (AI). They express skepticism about AI's purported benefits, highlighting fears about its impact on the environment, the labor market, and the production of relevant, useful content. The author then focuses on the challenge of evaluating the quality of AI-generated text, specifically addressing how to ensure it is "correct" and avoids "hallucinations" - instances where AI produces inaccurate or nonsensical output. They introduce the concept of "sentence embeddings" as a potential solution, explaining how it allows for comparing sentences based on meaning rather than just words. The author then presents their approach for validating the quality of AI-generated text using the "spacy-llm" package, along with other tools like "pytextrank" and "pysentence-similarity," all with the goal of ensuring the usefulness of AI-generated content.


## prompt
As editorial journalist generate :
- 3 "sexy" titles proposal based on this summary and the content below.
- a list of most important keywords based on this summary and the content below. Print the keywords in comma separated list.

### summary
```text

The provided text explores the author's concerns about the potential downsides of artificial intelligence (AI). They express skepticism about AI's purported benefits, highlighting fears about its impact on the environment, the labor market, and the production of relevant, useful content. The author then focuses on the challenge of evaluating the quality of AI-generated text, specifically addressing how to ensure it is "correct" and avoids "hallucinations" - instances where AI produces inaccurate or nonsensical output. They introduce the concept of "sentence embeddings" as a potential solution, explaining how it allows for comparing sentences based on meaning rather than just words. The author then presents their approach for validating the quality of AI-generated text using the "spacy-llm" package, along with other tools like "pytextrank" and "pysentence-similarity," all with the goal of ensuring the usefulness of AI-generated content.
```


### content

I don't like much laudatory speeches. I'm wary of them. They often sound false, closer to magical thinking than anything else. Inevitably, on AI, these speeches are legion. Insisting on the necessarily "tremendous" help that generative AI could bring as an editorial assistant or to remove irritants on time-consuming tasks is in a way easy.

> Talk is cheap. Act is pricey. Action speaks louder than words.

Once made, a partial exploration of AI's possibilities and implementation. I was wondering: what are my greatest fears towards IA?

Here is my shortlist ideas/fears:

- From an ecological point of view, I already suspect that AI will probably be a disaster! 
- From an economic point of view, AI is the latest mutation of capitalism that once again increases the remuneration of capital to the detriment of labor. Oh My God, I speak like a Marxist.
- **From a working perspective, what could be the relevance for some AI generated text? And so can we measure this relevance? Indeed, what is the point of generating useless content?  Is there a way to lower a LLM's hallucination's level to an acceptable threshold?**
    


For me, the dilemna is more on "Making AI".
"Making AI" must be an activity that is both intellectual and practical. As a human being, it is rewarding to produce something whose result we can at least contemplate and be happy about.

Between us, this idea is neither more nor less than a light version of what Hannah Arendt sets out in "The Human Condition". Let it be said, occasionally, I also deliberately "make AI" to respond solely to corporate considerations!



## Quick insights on IA & Ecology
Interesting ressources and scaring figures on the large carbon footprint instigated by AI technology. No doubt that AI is an energy hog... See below some extracts.

**Hard to see how can IA can develop without harming the environment? As always, the ecological arguments are very guilt-inducing without any real effect by the way.**

> The global AI energy demand projected to exponentially increase to at least 10 times the current level and exceed the annual electricity consumption of a small country like Belgium by 2026.

Source: <a href="https://hbr.org/2024/07/the-uneven-distribution-of-ais-environmental-impacts" target="_blank" rel="noopener">https://hbr.org/2024/07/the-uneven-distribution-of-ais-environmental-impacts</a>

> ChatGPT, the chatbot created by OpenAI in San Francisco, California, is already consuming the energy of 33,000 homes.

Source: <a href="https://www.nature.com/articles/d41586-024-00478-x" target="_blank" rel="noopener">https://www.nature.com/articles/d41586-024-00478-x</a>



- Will AI Be Another Unsustainable Environmental Disaster? | Opinion <a href="https://www.newsweek.com/will-ai-another-unsustainable-environmental-disaster-opinion-1928737" target="_blank" rel="noopener">https://www.newsweek.com/will-ai-another-unsustainable-environmental-disaster-opinion-1928737</a>

- AI has an environmental problem. Here’s what the world can do about that. <a href="https://www.unep.org/news-and-stories/story/ai-has-environmental-problem-heres-what-world-can-do-about" target="_blank" rel="noopener">https://www.unep.org/news-and-stories/story/ai-has-environmental-problem-heres-what-world-can-do-about</a>

- The Uneven Distribution of AI’s Environmental Impacts <a href="https://hbr.org/2024/07/the-uneven-distribution-of-ais-environmental-impacts" target="_blank" rel="noopener">https://hbr.org/2024/07/the-uneven-distribution-of-ais-environmental-impacts</a>

- AI is an energy hog. This is what it means for climate change. | MIT Technology Review <a href="https://www.technologyreview.com/2024/05/23/1092777/ai-is-an-energy-hog-this-is-what-it-means-for-climate-change/" target="_blank" rel="noopener">https://www.technologyreview.com/2024/05/23/1092777/ai-is-an-energy-hog-this-is-what-it-means-for-climate-change/</a>

- The Real Environmental Impact of AI | Earth.Org <a href="https://earth.org/the-green-dilemma-can-ai-fulfil-its-potential-without-harming-the-environment/" target="_blank" rel="noopener">https://earth.org/the-green-dilemma-can-ai-fulfil-its-potential-without-harming-the-environment/</a>

- Generative AI’s environmental costs are soaring — and mostly secret <a href="https://www.nature.com/articles/d41586-024-00478-x" target="_blank" rel="noopener">https://www.nature.com/articles/d41586-024-00478-x</a>

- Ecological footprints, carbon emissions, and energy transitions: the impact of artificial intelligence (AI) | Humanities and Social Sciences Communications <a href="https://www.nature.com/articles/s41599-024-03520-5" target="_blank" rel="noopener">https://www.nature.com/articles/s41599-024-03520-5</a>

- Making an image with generative AI uses as much energy as charging your phone <a href="https://www.technologyreview.com/2023/12/01/1084189/making-an-image-with-generative-ai-uses-as-much-energy-as-charging-your-phone/" target="_blank" rel="noopener">https://www.technologyreview.com/2023/12/01/1084189/making-an-image-with-generative-ai-uses-as-much-energy-as-charging-your-phone/</a>




## Quick insights on IA & Capitalism

I have already talked like many of the AI-driven doom. Again, a very pessimistic and guilt-inducing perspective!

More on the economic change to come: "Artificial Intelligence (AI) has the potential to reshape the global economy, especially in the realm of labor markets. Advanced economies will experience the benefits and pitfalls of AI sooner than emerging market and developing economies, largely due to their employment structure focused on cognitive-intensive roles."

It is true that AI disrupt the labor market on cognitive-intensive jobs. So far, historically, automation and information technology have tended to affect routine tasks, but one of the things that sets AI apart is its ability to impact high-skilled jobs.

AI will not only enhance productivity. It could lower labor demand, leading to lower wages and reduced hiring. In the most extreme cases, some of these jobs may disappear. Automation and AI will likely penetrate into domains that were heretofore considered immune.

- Forbes Daily: Will AI ‘Break’ Capitalism? <a href="https://www.forbes.com/sites/laurasmythe/2023/02/03/forbes-daily-will-ai-break-capitalism/" target="_blank" rel="noopener">https://www.forbes.com/sites/laurasmythe/2023/02/03/forbes-daily-will-ai-break-capitalism/</a>

- Gen-AI: Artificial Intelligence and the Future of Work <a href="https://www.imf.org/en/Publications/Staff-Discussion-Notes/Issues/2024/01/14/Gen-AI-Artificial-Intelligence-and-the-Future-of-Work-542379" target="_blank" rel="noopener">https://www.imf.org/en/Publications/Staff-Discussion-Notes/Issues/2024/01/14/Gen-AI-Artificial-Intelligence-and-the-Future-of-Work-542379</a>

- AI Will Transform the Global Economy. Let’s Make Sure It Benefits Humanity. <a href="https://www.imf.org/en/Blogs/Articles/2024/01/14/ai-will-transform-the-global-economy-lets-make-sure-it-benefits-humanity" target="_blank" rel="noopener">https://www.imf.org/en/Blogs/Articles/2024/01/14/ai-will-transform-the-global-economy-lets-make-sure-it-benefits-humanity</a>

- ScienceDirect <a href="https://www.sciencedirect.com/science/article/pii/S0160791X21002074" target="_blank" rel="noopener">https://www.sciencedirect.com/science/article/pii/S0160791X21002074</a>


## 1. The PITCH
Stop beating around the bush. Let's get back to reality, to the "making".

This is the real pitch I made to myself while discussing with my colleagues.

**Coming from web development, I have increased experience in testing. Testing is nothing more than the guarantee of proper functioning when delivering a feature and I wondered if it could be the same with an LLM used for generative AI.**


**Are there any techniques to ensure that the generated text is "correct" i.e. intelligible, relevant, in a word useful with an index measuring this relevance? Any mechanisms that prevent hallucinations. Hallucination is when the LLM goes Bananas!**


To have a clear idea of my need, I have decided to write a User Story.

> "As a [persona], I [want to], [so that]."

Source: <a href="https://www.atlassian.com/agile/project-management/user-stories" target="_blank" rel="noopener">https://www.atlassian.com/agile/project-management/user-stories</a>

One last thing, my role as AI coordinator is to make AI functionalities available to my company's staff. So, I'd better ensure the shipped feature has some added value!



```text
# User Story
As a journalist, I want to evaluate how closely a proposed set of content (title, abstract, and 10 keywords) aligns syntactically with 10 alternative content sets generated by a Mistral-type LLM. Using sentence similarity, I need the system to compare my original content set with each of the 10 generated sets, rank these generated sets from most relevant to least relevant, and display the results. This comparison should support multiple languages, including English, Spanish, Russian, Portuguese, and Vietnamese, among others.

# Context
Sentence Similarity refers to measuring how similar two texts are by converting them into vector embeddings that capture their semantic meaning, then calculating their proximity to one another. This is especially useful in ranking, clustering, and information retrieval tasks.
```


While surfing, I finally discovered a lot of things that are not all related to my subject but any opportunity is good to seize to learn:

I explored several packages and a technique for validating the output of an LLM by another LLM. For this last one, locally, I have used "all-MiniLM-L6-v2" check the output of "Mistral", operated witj Ollama.


Here is the list of packages used:


- **spacy-llm**: This package integrates Large Language Models (LLMs) into spaCy, featuring a modular system for fast prototyping and prompting, and turning unstructured responses into robust outputs for various NLP tasks, no training data required. Source: <a href="https://github.com/explosion/spacy-llm" target="_blank" rel="noopener">https://github.com/explosion/spacy-llm</a> 

- **pytextrank**: PyTextRank is a Python implementation of TextRank as a spaCy pipeline extension, for graph-based natural language work -- and related knowledge graph practices. This includes the family of textgraph algorithms: TextRank, PositionRank, Biased TextRank, TopicRank. Popular use cases for this library include: phrase extraction: get the top-ranked phrases from a text document, low-cost extractive summarization of a text document, help infer concepts from unstructured text into more structured representation. Source: <a href="https://pypi.org/project/pytextrank/" target="_blank" rel="noopener">https://pypi.org/project/pytextrank/</a>




- **pysentence-similarity**: PySentence-Similarity is a tool designed to identify and find similarities between sentences and a base sentence, expressed as a percentage 📊. It compares the semantic value of each input sentence to the base sentence, providing a score that reflects how related or similar they are. This tool is useful for various natural language processing tasks such as clustering similar texts 📚, paraphrase detection 🔍 and textual consequence measurement 📈. Source: <a href="https://pypi.org/project/pysentence-similarity/" target="_blank" rel="noopener">https://pypi.org/project/pysentence-similarity/</a>

Finally, I keep going around this question of validating the relevance of a result produced by an LLM, this time in a more qualitative way. Unlike the previous post where I was rather carrying out surface checks using promptfoo, this time, I sought more to control the quality of what the LLMs that I am about to use produce and especially to automate it without a human intervening to validate this result.



## 2. The HOW-TO
I always give myself the leisure to dress up the scripts with screens using Streamlit. It is always with the perspective of presenting the result of my investigations to the greatest number.



- **Step #1:** Generate the output from the LLM: check 024_ia_ollama_streamlit.py
- **Step #2:** Append some other variables to the output from the LLM: check 027a_ia_ollama_streamlit_append_files.py. This step should be probably merged with the Step #1, you lazy slob!
- **Step #3:** Measure the semantic similarity betwwen the ouput IA generated and the human proposal. Comparison id made with "all-MiniLM-L6-v2".
check 029_ia_sentence_transformers_import.py



## 3. The CONCEPTS
To test this User Story, I needed to explore a few ideas related to "sentence embeddings." 

Simply put, a **sentence embedding** is a way to represent a sentence as a list of numbers (a "vector") that captures its meaning. With this, we can easily compare, group, or search for sentences based on what they mean rather than just the words they contain.

For example, the *all-MiniLM-L6-v2* model is a compact tool that creates these embeddings. It takes a sentence or short paragraph and turns it into a 384-number vector. This makes it useful for:


- **Semantic search:** Finding sentences with similar meanings
- **Clustering:** Grouping similar sentences together
- **Sentence similarity:** Measuring how close two sentences are in meaning


**Sentence-Transformers**
The Sentence-Transformers library is a Python tool that makes it easy to work with sentence embeddings. It's widely used for tasks like finding similar text, measuring similarity, and more.

Source: <a href="https://www.sbert.net/" target="_blank" rel="noopener">https://www.sbert.net/</a>


**Here is a quick definition of Sentence Similarity that is useful for our User Story.**

> Sentence Similarity is the task of determining how similar two texts are. Sentence similarity models convert input texts into vectors (embeddings) that capture semantic information and calculate how close (similar) they are between them. This task is particularly useful for information retrieval and clustering/grouping.

Source: <a href="https://huggingface.co/tasks/sentence-similarity" target="_blank" rel="noopener">https://huggingface.co/tasks/sentence-similarity</a>

## 4. EXTRA CODE


**Sample in French for "best proposition"**
```python
best_content = "'Lors de son mandat à la Maison Blanche, Donald Trump avait retiré les États-Unis de plusieurs accords internationaux et agences de l\'ONU, menaçant même de quitter l\'Otan. À l\'époque, des hauts fonctionnaires de son équipe agissaient comme \"garde-fous\" et l\'Europe n\'était pas en proie à un conflit sur son territoire. Aujourd\'hui, face à la possibilité d\'un retour au pouvoir du milliardaire, l\'Europe se prépare activement à se protéger d\'une nouvelle présidence du républicain.\n'"
best_title = "'\"Les garde-fous ont disparu\" : l\'UE se prépare face à l\'hypothèse d\'une victoire de Trump'"
best_keywords = ["'Union européenne'", "'Pour aller plus loin'", "'États-Unis'", "'Présidentielle américaine'", "'USA 2024'", "'Donald Trump'", "'Décryptage'", '"l\'été dernier"']
```

**A simple script to see in action "embeddings" that is the starting base to work on Sentence Similarity.**
```python
from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# List of sentences
sentences = ["This is an example sentence", "Each sentence is converted to an embedding"]

# Convert sentences to embeddings
embeddings = model.encode(sentences)

# Output the embeddings
print(embeddings)

```

**Unfortunately, Spacy-llm is not Ollama compliant for the moment, so it still requires to have a paid license to leverage on ChatGPT for instance. A patch is on it way apparently.**
Check out: <a href="https://github.com/explosion/spacy-llm/discussions/481" target="_blank" rel="noopener">https://github.com/explosion/spacy-llm/discussions/481</a>

```text
# should be working soon
[nlp]
lang = "en"
pipeline = ["llm"]
[components]
[components.llm]
factory = "llm"
[components.llm.task]
@llm_tasks = "spacy.NER.v3"
labels = ["label 1", "label 2", "label 3"]
[components.llm.model]
@llm_models = "langchain.Ollama.v1"
name =  "qwen2:7b"
config = {
    "base_url": "https://samplePlace.com",
    "temperature": 1.0
    }
```


<h3>CASES FROM SPACY-LLM</h3>

**Why I found spacy-llm interesting, here is below what caught my attention! It is all about money and security.**

Indeed, sometime, using an LLM in some NLP task is overkill like using sledgehammer to crack a nut! That is the main reason for the spacy-llm package existence! It provides simple and easier way to replace the use of an LLM.

> Of course, there can be components in your system for which the power of an LLM is fully justified. If you want a system that can synthesize information from multiple documents in subtle ways and generate a nuanced summary for you, bigger is better. However, even if your production system needs an LLM for some of the task, that doesn't mean you need an LLM for all of it. Maybe you want to use a cheap text classification model to help you find the texts to summarize, or maybe you want to add a rule-based system to sanity check the output of the summary. These before-and-after tasks are much easier with a mature and well-thought-out library, which is exactly what spaCy provides.

Source : <a href="https://github.com/explosion/spacy-llm/tree/main" target="_blank" rel="noopener">https://github.com/explosion/spacy-llm/tree/main</a>


## mistral

- 3 "Sexy" Title Proposals

-- "AI's Dark Side: Environmental Impact, Job Loss, and the Battle for Content Quality"
-- "Beyond Words: The Revolution of Sentence Embeddings in AI Text Validation"
-- "Unmasking AI Hallucinations: How Sentence Embeddings Can Save AI-Generated Content"

- List of Most Important Keywords
Artificial Intelligence, AI, Downsides, Environment, Labor Market, Content Quality, Sentence Embeddings, Hallucinations, Correctness, AI-Generated Text, spacy-llm, pytextrank, pysentence-similarity, Validation, Usefulness


Title: Content Quality: How Sentence Embeddings Can Save AI-Generated Content and some other conncerns on AI: Environmental Impact, Job Loss


