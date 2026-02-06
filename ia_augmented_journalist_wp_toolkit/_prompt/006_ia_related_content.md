## PROMPT_1

As a python and IA expert, in few steps, can you describe based on this wp post parsing how can create related content feature for these posts meaning that will do 
- STEP_1. Content Vectorization
- STEP_2. Similarity Calculation
- STEP_3. Storage in SQLite or MySQL. Goes with SQLite
- STEP_4. Scalability, think to optimize for performance, especially if the dataset grows. Consider batch processing for vectorization and indexing.

Let's focus on the STEP_1 then you will do the script for each step in another prompt. I want a step-by-step implementation plan.



## OUTPUT_1

For STEP_1 (Content Vectorization), you want to turn each post (title + content, maybe slug) into a numerical vector using a good embedding model, in a way that’s reproducible and scalable. Here is a step‑by‑step implementation plan.

## 1. Decide what to vectorize per post

1. Choose the text fields that define the **semantic** of a post:  
   - Minimum: `title_rendered` + `content`.  
   - Optional: `slug`, tags/categories if you have them later.  
2. Define a clean concatenation strategy, e.g.:  
   - `"TITLE: {title_rendered}\n\nCONTENT: {content}"`.  
3. Add a small pre‑processing step:  
   - Strip HTML tags if `content` is HTML.  
   - Normalize whitespace, lower/upper case if you want consistency.  
   - Optionally truncate very long content to a token/char limit to avoid very slow embedding calls. [tigerdata](https://www.tigerdata.com/blog/how-we-built-a-content-recommendation-system-with-pgai-and-pgvectorscale)

### Example decision

- Use `title_rendered` + `content` primarily.  
- Fallback: if `content` is empty, embed only the title.  

## 2. Choose and configure an embedding model

1. Use a modern sentence embedding model, not TF‑IDF, so you get semantic similarity.  
2. For a local, free setup, use `sentence-transformers` with a small, fast model like `all-MiniLM-L6-v2` (384‑dim, good trade‑off). [sbert](https://sbert.net)
3. Install dependencies in your project:  
   - `pip install sentence-transformers` (and `torch` if needed). [safjan](https://safjan.com/text-vectorization-with-vectorhub-and-sentence-transformers/)
4. Initialize the model once at module level so you don’t reload it on each call.

Conceptually:

- Input: list of strings (one per post).  
- Output: list/array of vectors (one per post, same dimension for all). [sbert](https://sbert.net)

## 3. Design a small vectorization API

Create a clean separation so STEP_1 can evolve without touching STEP_2/3:

1. Keep your existing JSON parsing (returning `ParsedPost` objects).  
2. Add a function that takes `List[ParsedPost]` and returns a list of `(post_id, embedding_vector)`.

For example:

- `build_post_text(post: ParsedPost) -> str` builds the text to embed.  
- `embed_posts(posts: List[ParsedPost]) -> List[tuple[int, list[float]]]` runs the model in batch.

This way:

- If you change model or text pre‑processing, only STEP_1 code changes.  
- STEP_2 (similarity) and STEP_3 (SQLite) keep the same interface: they only see IDs and vectors.

## 4. Implement pre‑processing + batching

1. Pre‑processing function:

   - Strip HTML in `content` (e.g. `BeautifulSoup` or a simple regex if your HTML is simple).  
   - Fallback when `content` is empty: use title only.  
   - Optionally limit length (e.g. first N characters or tokens). [exchange.scale](https://exchange.scale.com/public/blogs/how-to-implement-nlp-preprocessing-techniques-in-python)

2. Batching strategy:

   - Embedding many posts at once is faster than one by one, but you don’t want to blow GPU/CPU RAM.  
   - Pick a `BATCH_SIZE` (e.g. 32, 64, 128) and process posts in chunks:  
     - `for i in range(0, len(posts), BATCH_SIZE)` …  
   - `SentenceTransformer.encode` already supports batch input; you just feed lists. [safjan](https://safjan.com/text-vectorization-with-vectorhub-and-sentence-transformers/)

3. Output shape:

   - For each batch, you get a matrix `batch_size x dim`.  
   - Convert each row to `list[float]` (for later SQLite storage) and pair it with `post.id`.

## 5. Plan for reproducibility and configuration

1. Fix a model name as a configuration constant:  
   - `EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"` or similar. [huggingface](https://huggingface.co/sentence-transformers)
2. Optionally store model name and embedding dimension as metadata in SQLite along with vectors so you know how they were produced. [dev](https://dev.to/techwithhari/my-journey-with-sentence-transformers-openai-embeddings-and-vector-databases-6d8)
3. Make the following parameters configurable (env vars or a small config file):  
   - Model name.  
   - Batch size.  
   - Max content length (characters or tokens).  

## 6. Connect STEP_1 to later steps (high level)

Just to ensure the design is future‑proof:

1. STEP_1 output should be a structure like:

   - `List[{"post_id": int, "embedding": List[float]}]`.

2. STEP_2 (Similarity):

   - Will consume these embeddings in memory or from DB and compute cosine similarity. [shaped](https://www.shaped.ai/blog/content-based-filtering-explained-recommending-based-on-what-you-like)

3. STEP_3 (SQLite):

   - Will persist `(post_id, embedding)`; you can store embeddings as blobs, JSON, or a simple separate table. [dev](https://dev.to/stephenc222/how-to-use-sqlite-vec-to-store-and-query-vector-embeddings-58mf)

4. STEP_4 (Scalability):

   - Because STEP_1 is already batched and decoupled, you can:  
     - Run vectorization offline as a cron/batch job.  
     - Re‑embed only updated posts.  
     - Swap in a faster/smaller model later if needed. [dev](https://dev.to/techwithhari/my-journey-with-sentence-transformers-openai-embeddings-and-vector-databases-6d8)

***

In the next prompt, we can turn this plan into concrete Python code for STEP_1: model initialization, text pre‑processing, batched embedding, and returning a clean data structure that STEP_2–3 can use directly.




