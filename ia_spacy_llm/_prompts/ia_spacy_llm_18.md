# ia_spacy_llm_18.md

## PROMPT_1



## MISTRAL_1
Certainly! Here is a rewritten and clarified version of the user story, incorporating the context provided:

USER STORY

As a journalist,

I want to be able to compare the syntactic similarity of my best proposition (which includes a title, an abstract, and a set of 10 keywords) with a set of 10 identical propositions generated by a Mistral-type LLM.

So that I can rank the 10 sets of propositions from the most relevant to the least relevant.

I must be able to perform this comparison in multiple languages, such as English, Spanish, Russian, Portuguese, Vietnamese, etc.

Acceptance Criteria:

The system should allow me to input my best proposition, which includes a title, an abstract, and a set of 10 keywords.
The system should generate 10 identical propositions using a Mistral-type LLM.
The system should compare the syntactic similarity of my best proposition with each of the 10 generated propositions.
The system should rank the 10 sets of propositions from the most relevant to the least relevant based on the syntactic similarity.
The system should support performing this comparison in multiple languages, including but not limited to English, Spanish, Russian, Portuguese, and Vietnamese.
Definition of "Sentence Similarity":

Sentence Similarity is the task of determining how similar two texts are. Sentence similarity models convert input texts into vectors (embeddings) that capture semantic information and calculate how close (similar) they are between them. This task is particularly useful for information retrieval and clustering/grouping.




## CHATGPT_1
Here is a clarified and rephrased version of your user story:

**User Story**  
*As a journalist, I want to evaluate how closely a proposed set of content (title, abstract, and 10 keywords) aligns syntactically with 10 alternative content sets generated by a Mistral-type LLM. Using sentence similarity, I need the system to compare my original content set with each of the 10 generated sets, rank these generated sets from most relevant to least relevant, and display the results. This comparison should support multiple languages, including English, Spanish, Russian, Portuguese, and Vietnamese, among others.*

**Context**  
*Sentence Similarity refers to measuring how similar two texts are by converting them into vector embeddings that capture their semantic meaning, then calculating their proximity to one another. This is especially useful in ranking, clustering, and information retrieval tasks.*
