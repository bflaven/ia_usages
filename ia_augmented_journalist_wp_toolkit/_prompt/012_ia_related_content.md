## PROMPT_1

Let's proceed to the `POINT_6`
- Similarity computation (STEP_2: cosine similarity on these embeddings).
- SQLite storage of (post_id, vector) for a related‑content feature.
But bear in my mind that :
If you create a SQLite storage would I be able to know the if of the post selected and the posts related to it with the help of the post_id, so I can see the post selected and the post related to this post with the similarity.

When it will be stored in a temporary SQLite storage, I will migrate the result as describe above into a MYSQL table in mariadb, the database used by WP and the main idea behind this POC is to create a WP plugin that will help to have a related content feature on each post that will show for a selected post, 3 or 5 related posts based on the process you made an describe. You got the point.

```text
# POINT_1. Decide what to vectorize per post (DONE, 003_parsing_posts_vectorize_per_post.py)
# POINT_2. Choose and configure an embedding model (DONE, 004_parsing_posts_choose_embedding_model.py)
# POINT_3. Design a small vectorization API (DONE, 005_parsing_posts_vectorization_api.py)
# POINT_4. Implement pre‑processing + batching (DONE, 006_parsing_posts_vectorization_batching.py)
# POINT_5. Plan for reproducibility and configuration (DONE, 007_parsing_posts_reproducibility_config.py)
# POINT_6. Connect STEP_1 to later steps (high level) (TODO) 
```



## OUTPUT_1

You can absolutely wire this so you always know the “anchor” post and its related posts via `post_id`, and then later mirror the same structure in MariaDB for your WP plugin.

Here’s a concise plan for `POINT_6`, focused on similarity + SQLite, with your constraints in mind.

## 1. Data model in SQLite

Create a temporary SQLite DB that keeps:

- One table for embeddings:
  - `post_embeddings(post_id INTEGER PRIMARY KEY, embedding BLOB or TEXT)`
- One table for precomputed related posts (optional but recommended for WP):
  - `post_related(post_id INTEGER, related_post_id INTEGER, similarity REAL, rank INTEGER, PRIMARY KEY(post_id, related_post_id))`

This gives you, for any `post_id`:

- Its own embedding.  
- A list of `(related_post_id, similarity, rank)` you can export to MariaDB and use in your plugin.

You can store the embedding as JSON text to keep it simple for the POC; you don’t need a vector extension. [damian](https://damian.fyi/xamarin/2025/04/19/getting-storing-and-using-embeddings-in-dotnet.html)

## 2. Workflow overview

Using your existing `POINT_5` code as the source of `(post_id, embedding)`:

1. **Embed all posts** (already done in `007_parsing_posts_reproducibility_config.py`).  
2. **Write embeddings to SQLite**:
   - Insert one row per `post_id`.  
3. **Compute similarities in Python using cosine similarity**:
   - For each post vector, compute cosine similarity to all other vectors, pick top‑K (e.g. 5). [earthly](https://earthly.dev/blog/cosine_similarity_text_embeddings/)
4. **Write related posts table**:
   - For each `post_id`, insert rows with `related_post_id`, `similarity`, `rank`.  

Once this is in SQLite, you export `post_related` (and maybe `post_embeddings`) to MariaDB and expose it from your WP plugin.

## 3. Similarity computation (cosine, top‑K)

Core idea with NumPy:

- Stack all embeddings into a 2D array `E` of shape `(n_posts, dim)`.  
- Normalize rows to unit norm once.  
- Cosine similarity between all pairs is then `S = E @ E.T`. [stackoverflow](https://stackoverflow.com/questions/72328976/python-finding-cosine-similarity-between-two-groups-of-vectors-in-the-most-eff)
- For each row `i`, you:
  - Zero out or ignore `S[i, i]` (self‑similarity).  
  - Arg‑partition / sort to get the indices of top‑K highest similarity. [stackoverflow](https://stackoverflow.com/questions/70032777/quickly-performing-cosine-similarity-with-list-of-embeddings)

You’ll keep a mapping `index -> post_id` so you can go back to WP IDs.

## 4. SQLite storage pattern

In the temporary SQLite DB:

- `post_embeddings`:
  - `post_id INTEGER PRIMARY KEY`
  - `embedding_json TEXT NOT NULL` (JSON array of floats)  
- `post_related`:
  - `post_id INTEGER NOT NULL`
  - `related_post_id INTEGER NOT NULL`
  - `similarity REAL NOT NULL`
  - `rank INTEGER NOT NULL`
  - `PRIMARY KEY (post_id, related_post_id)`

This structure makes it trivial to later:

- Dump `post_related` to MariaDB.  
- For a given post in WP, select top‑N related posts using `ORDER BY rank` or `ORDER BY similarity DESC`.  

***

If you want, next step I can generate a concrete script (e.g. `008_parsing_posts_similarity_sqlite.py`) that:

- Takes the embeddings from `EmbeddingConfig` / `embed_posts_batched`.  
- Computes cosine similarities and top‑K related posts.  
- Creates the SQLite DB with `post_embeddings` and `post_related`.


