






## ENHANCE_PROMPT_1

Can you improve the prompt: 
```text
Here is a user story. I want a solution with IA, using script in python, that will enable a feature named related content for different content. For instance let's say I have a post about eg "American President elections". The solution should be able to grab related content in the same language that talks about the same subject. You should be able to calculate an indice from 0 to 1 (1 meaning that it is the same post).




1. The solution should be working fo many languages and on many subjects e.g Vietnamese, Portuguese do Brazil, Portuguese,Chinese,Persian,Khmer,Portuguese,Romanian,Russian,Swahili,Hausa

2. Start from the simple to the more complex solution
3. Think about the implementation. With a one shot


For instance I will make a POC for Wordpress. I have a certain amount of posts, I need to make a easy vectorization may be from a summary of the post and with the help of Keywords, then make the calculation for the related content that can be easily stored in a mysql database one post against each posts selected in a dataset. Everything needs to be stored in a wp plugin.

Describe step by step what has to be done.
```

Print the result as plain text ```text...``` and not as a readme file, removing all tags such as `**`, `##`... etc


## OUTPUT_1
Here is an improved and more structured version of your prompt, focusing on clarity, technical precision, and actionable steps:

---

```text
I need an AI-powered solution, implemented in Python, to create a "related content" feature for a content management system. The goal is to automatically find and rank related content (e.g., articles, posts) based on semantic similarity, regardless of language. For example, if a user reads a post about "American Presidential Elections," the system should suggest other posts in the same language that discuss similar topics. The similarity should be quantified as an index between 0 and 1, where 1 indicates identical content.

---

### Requirements

1. **Multilingual Support**:
   The solution must work across multiple languages, including but not limited to:
   Vietnamese, Brazilian Portuguese, Portuguese, Chinese, Persian, Khmer, Romanian, Russian, Swahili, and Hausa.
   The system should handle language-specific nuances and avoid bias toward any particular language.

2. **Implementation Approach**:
   - Start with a simple, scalable solution and iteratively enhance it.
   - Focus on a one-shot implementation: a proof of concept (POC) for WordPress.
   - The POC should use a subset of existing posts to demonstrate feasibility.

3. **Technical Workflow**:
   - **Content Vectorization**:
     Generate embeddings (vector representations) for each post. Use a combination of:
     - A summary of the post (e.g., first paragraph or abstract).
     - Keywords extracted from the post (e.g., using TF-IDF or named entity recognition).
     - Consider using pre-trained multilingual models (e.g., sentence-transformers, LaBSE, or multilingual BERT) for embedding generation.
   - **Similarity Calculation**:
     Compute pairwise similarity scores between posts using cosine similarity or another appropriate metric.
     Normalize the scores to a 0-1 range, where 1 indicates identical content.
   - **Storage**:
     Store the embeddings and similarity scores in a MySQL database.
     Design a WordPress plugin to integrate this functionality, ensuring efficient querying and retrieval of related posts.
   - **Scalability**:
     Optimize for performance, especially if the dataset grows. Consider batch processing for vectorization and indexing.

4. **Deliverables**:
   - A step-by-step implementation plan, including:
     1. Data preprocessing (e.g., cleaning, summarization, keyword extraction).
     2. Embedding generation for each post.
     3. Similarity calculation and scoring.
     4. Database schema design for storing embeddings and relationships.
     5. WordPress plugin development for seamless integration.
     6. Testing and validation (e.g., manual review of suggested related posts).
   - Python scripts for each step, with clear documentation.
   - A sample dataset (e.g., 10-20 posts in 2-3 languages) to demonstrate the POC.

5. **Constraints**:
   - The solution should be lightweight and efficient, suitable for deployment in a WordPress environment.
   - Avoid external dependencies that may not be compatible with WordPress or require complex setup.
   - Prioritize accuracy and relevance in related content suggestions.

---

### Expected Output
Provide a detailed, step-by-step plan for implementing this solution. Focus on practicality, scalability, and ease of integration with WordPress. Include code snippets or pseudocode where helpful, and suggest tools/libraries for each step (e.g., Hugging Face for embeddings, SQLAlchemy for database interactions).
```


## depot

In English, convert the text "1. Usecase" into "2. User Story Model" in a way that is suitable for creating a Jira ticket and is understandable by the stakeholder (journalist, management).

Retain the "As a " persona.
