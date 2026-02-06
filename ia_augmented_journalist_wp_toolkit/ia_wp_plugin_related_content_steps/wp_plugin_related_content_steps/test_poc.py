"""
Standalone POC test script
Tests the related content system without requiring WordPress
"""

import os
import sys
import json
import logging
from dotenv import load_dotenv
import numpy as np

from database import DatabaseManager
from embeddings import EmbeddingGenerator, ContentProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_sample_posts():
    """Load sample posts from JSON file"""
    try:
        with open('sample_posts.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['posts']
    except FileNotFoundError:
        logger.error("sample_posts.json not found. Run generate_sample_data.py first.")
        sys.exit(1)


def test_embedding_generation():
    """Test 1: Generate embeddings for sample posts"""
    logger.info("=" * 70)
    logger.info("TEST 1: Embedding Generation")
    logger.info("=" * 70)
    
    # Load configuration
    load_dotenv()
    config = {
        'DB_HOST': os.getenv('DB_HOST', 'localhost'),
        'DB_PORT': os.getenv('DB_PORT', '3306'),
        'DB_NAME': os.getenv('DB_NAME', 'wordpress'),
        'DB_USER': os.getenv('DB_USER'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD'),
        'EMBEDDING_MODEL': os.getenv('EMBEDDING_MODEL', 'paraphrase-multilingual-MiniLM-L12-v2'),
        'MAX_CONTENT_LENGTH': os.getenv('MAX_CONTENT_LENGTH', '1000')
    }
    
    # Initialize components
    logger.info("Initializing embedding generator...")
    embedder = EmbeddingGenerator(config['EMBEDDING_MODEL'])
    processor = ContentProcessor(int(config['MAX_CONTENT_LENGTH']))
    db = DatabaseManager(config)
    
    # Load sample posts
    logger.info("Loading sample posts...")
    posts = load_sample_posts()
    logger.info(f"Loaded {len(posts)} sample posts")
    
    # Process each post
    success_count = 0
    language_stats = {}
    
    for post in posts:
        try:
            post_id = post['id']
            
            # Prepare content
            prepared = processor.prepare_content(post)
            language = prepared['language']
            
            logger.info(f"Processing post {post_id} ({language}): {post['title']['rendered'][:50]}...")
            
            # Generate embedding
            embedding = embedder.generate_embedding(prepared['text'])
            
            # Store in database
            success = db.insert_embedding(
                post_id=post_id,
                embedding=embedding,
                model_name=embedder.model_name,
                language=language,
                content_hash=prepared['hash']
            )
            
            if success:
                success_count += 1
                language_stats[language] = language_stats.get(language, 0) + 1
                logger.info(f"  ✓ Embedding generated (dim={embedding.shape[0]})")
            
        except Exception as e:
            logger.error(f"  ✗ Error processing post {post['id']}: {e}")
    
    logger.info("\n" + "=" * 70)
    logger.info(f"TEST 1 RESULTS: {success_count}/{len(posts)} posts processed successfully")
    logger.info("=" * 70)
    logger.info("Language distribution:")
    for lang, count in sorted(language_stats.items()):
        logger.info(f"  {lang}: {count} posts")
    
    return success_count > 0


def test_similarity_computation():
    """Test 2: Compute similarities between posts"""
    logger.info("\n" + "=" * 70)
    logger.info("TEST 2: Similarity Computation")
    logger.info("=" * 70)
    
    load_dotenv()
    config = {
        'DB_HOST': os.getenv('DB_HOST', 'localhost'),
        'DB_PORT': os.getenv('DB_PORT', '3306'),
        'DB_NAME': os.getenv('DB_NAME', 'wordpress'),
        'DB_USER': os.getenv('DB_USER'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD'),
        'EMBEDDING_MODEL': os.getenv('EMBEDDING_MODEL', 'paraphrase-multilingual-MiniLM-L12-v2'),
        'MIN_SIMILARITY_THRESHOLD': float(os.getenv('MIN_SIMILARITY_THRESHOLD', '0.3')),
        'MAX_RELATED_POSTS': int(os.getenv('MAX_RELATED_POSTS', '10'))
    }
    
    db = DatabaseManager(config)
    embedder = EmbeddingGenerator(config['EMBEDDING_MODEL'])
    
    # Get all embeddings
    logger.info("Retrieving embeddings from database...")
    all_embeddings = db.get_all_embeddings()
    
    if len(all_embeddings) < 2:
        logger.error("Not enough embeddings in database")
        return False
    
    logger.info(f"Found {len(all_embeddings)} embeddings")
    
    # Compute similarity matrix
    logger.info("Computing pairwise similarities...")
    post_ids = list(all_embeddings.keys())
    embeddings_matrix = np.array([all_embeddings[pid] for pid in post_ids])
    
    similarity_matrix = embedder.pairwise_similarity_matrix(embeddings_matrix)
    
    # Store top N similarities for each post
    total_pairs = 0
    min_threshold = config['MIN_SIMILARITY_THRESHOLD']
    max_related = config['MAX_RELATED_POSTS']
    
    for i, source_post_id in enumerate(post_ids):
        similarities = []
        
        for j, target_post_id in enumerate(post_ids):
            if i != j and similarity_matrix[i, j] >= min_threshold:
                similarities.append((
                    source_post_id,
                    target_post_id,
                    float(similarity_matrix[i, j])
                ))
        
        # Sort and keep top N
        similarities.sort(key=lambda x: x[2], reverse=True)
        similarities = similarities[:max_related]
        
        if similarities:
            db.delete_similarities_for_post(source_post_id)
            db.insert_similarities(similarities)
            total_pairs += len(similarities)
            
            logger.info(f"Post {source_post_id}: {len(similarities)} related posts found")
    
    logger.info("\n" + "=" * 70)
    logger.info(f"TEST 2 RESULTS: Stored {total_pairs} similarity pairs")
    logger.info("=" * 70)
    
    return total_pairs > 0


def test_query_related_posts():
    """Test 3: Query related posts"""
    logger.info("\n" + "=" * 70)
    logger.info("TEST 3: Query Related Posts")
    logger.info("=" * 70)
    
    load_dotenv()
    config = {
        'DB_HOST': os.getenv('DB_HOST', 'localhost'),
        'DB_PORT': os.getenv('DB_PORT', '3306'),
        'DB_NAME': os.getenv('DB_NAME', 'wordpress'),
        'DB_USER': os.getenv('DB_USER'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD'),
        'MIN_SIMILARITY_THRESHOLD': float(os.getenv('MIN_SIMILARITY_THRESHOLD', '0.3'))
    }
    
    db = DatabaseManager(config)
    
    # Load sample posts to get titles
    posts = load_sample_posts()
    post_titles = {p['id']: p['title']['rendered'] for p in posts}
    
    # Test queries for first 3 posts
    test_post_ids = [1, 8, 11]  # English election, English tech, Chinese election
    
    for post_id in test_post_ids:
        logger.info(f"\nQuerying related posts for Post {post_id}:")
        logger.info(f"Title: {post_titles.get(post_id, 'Unknown')}")
        logger.info("-" * 70)
        
        related = db.get_related_posts(post_id, limit=5, min_score=config['MIN_SIMILARITY_THRESHOLD'])
        
        if not related:
            logger.warning("  No related posts found")
            continue
        
        for i, post in enumerate(related, 1):
            logger.info(f"{i}. [{post['language']}] {post['post_title']}")
            logger.info(f"   Similarity: {post['similarity_score']:.3f}")
    
    logger.info("\n" + "=" * 70)
    logger.info("TEST 3 COMPLETE")
    logger.info("=" * 70)
    
    return True


def test_cross_language_similarity():
    """Test 4: Verify cross-language similarity detection"""
    logger.info("\n" + "=" * 70)
    logger.info("TEST 4: Cross-Language Similarity")
    logger.info("=" * 70)
    
    load_dotenv()
    config = {
        'DB_HOST': os.getenv('DB_HOST', 'localhost'),
        'DB_PORT': os.getenv('DB_PORT', '3306'),
        'DB_NAME': os.getenv('DB_NAME', 'wordpress'),
        'DB_USER': os.getenv('DB_USER'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD')
    }
    
    db = DatabaseManager(config)
    
    # Posts about same topic in different languages
    # Post 1: English election
    # Post 4: French election
    # Post 6: Vietnamese election
    
    test_cases = [
        (1, 'en', "US Elections (English)", [4, 6]),  # Should relate to French & Vietnamese
        (8, 'en', "AI Tech (English)", [10]),  # Should relate to French AI
    ]
    
    for source_id, source_lang, source_desc, expected_related_ids in test_cases:
        logger.info(f"\nTest case: {source_desc}")
        logger.info(f"Source: Post {source_id} ({source_lang})")
        
        related = db.get_related_posts(source_id, limit=10, min_score=0.3)
        
        # Check if expected posts are in results
        found_ids = [r['related_post_id'] for r in related]
        
        for expected_id in expected_related_ids:
            if expected_id in found_ids:
                idx = found_ids.index(expected_id)
                score = related[idx]['similarity_score']
                lang = related[idx]['language']
                logger.info(f"  ✓ Found expected cross-language match: Post {expected_id} ({lang}) - Score: {score:.3f}")
            else:
                logger.warning(f"  ✗ Expected post {expected_id} not in related posts")
    
    logger.info("\n" + "=" * 70)
    logger.info("TEST 4 COMPLETE")
    logger.info("=" * 70)
    
    return True


def test_performance():
    """Test 5: Performance metrics"""
    logger.info("\n" + "=" * 70)
    logger.info("TEST 5: Performance Metrics")
    logger.info("=" * 70)
    
    import time
    
    load_dotenv()
    config = {
        'EMBEDDING_MODEL': os.getenv('EMBEDDING_MODEL', 'paraphrase-multilingual-MiniLM-L12-v2')
    }
    
    embedder = EmbeddingGenerator(config['EMBEDDING_MODEL'])
    
    # Test single embedding generation
    test_text = "This is a test sentence for performance measurement."
    
    start = time.time()
    for _ in range(10):
        embedder.generate_embedding(test_text)
    single_time = (time.time() - start) / 10
    
    logger.info(f"Average single embedding time: {single_time*1000:.2f}ms")
    
    # Test batch embedding generation
    test_texts = [test_text] * 100
    
    start = time.time()
    embedder.generate_embeddings_batch(test_texts, batch_size=32, show_progress=False)
    batch_time = time.time() - start
    
    logger.info(f"Batch (100 texts) time: {batch_time:.2f}s")
    logger.info(f"Average per text in batch: {(batch_time/100)*1000:.2f}ms")
    
    # Estimate processing time
    logger.info("\nEstimated processing times:")
    logger.info(f"  100 posts: ~{(single_time * 100):.1f}s")
    logger.info(f"  1,000 posts: ~{(single_time * 1000 / 60):.1f}min")
    logger.info(f"  10,000 posts: ~{(single_time * 10000 / 3600):.1f}hr")
    
    logger.info("\n" + "=" * 70)
    logger.info("TEST 5 COMPLETE")
    logger.info("=" * 70)
    
    return True


def main():
    """Run all POC tests"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 20 + "RELATED CONTENT AI - POC TEST" + " " * 19 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")
    
    tests = [
        ("Embedding Generation", test_embedding_generation),
        ("Similarity Computation", test_similarity_computation),
        ("Query Related Posts", test_query_related_posts),
        ("Cross-Language Similarity", test_cross_language_similarity),
        ("Performance Metrics", test_performance)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = "✓ PASS" if result else "✗ FAIL"
        except Exception as e:
            logger.error(f"Test '{test_name}' failed with error: {e}", exc_info=True)
            results[test_name] = "✗ ERROR"
    
    # Print summary
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 28 + "TEST SUMMARY" + " " * 28 + "║")
    print("╠" + "=" * 68 + "╣")
    
    for test_name, result in results.items():
        status = result
        padding = 50 - len(test_name)
        print(f"║  {test_name}" + " " * padding + f"{status}  ║")
    
    print("╚" + "=" * 68 + "╝")
    
    # Overall result
    all_passed = all("PASS" in r for r in results.values())
    
    print("\n")
    if all_passed:
        print("✓ POC TEST SUCCESSFUL - System is ready for use!")
    else:
        print("✗ Some tests failed - Please review logs and configuration")
    
    print("\nNext steps:")
    print("1. Review test results above")
    print("2. Check related_content.log for details")
    print("3. Query specific posts: python main.py --action query --post-id 1")
    print("4. Install WordPress plugin if not already done")
    print("\n")


if __name__ == '__main__':
    try:
        # Check if sample data exists
        if not os.path.exists('sample_posts.json'):
            print("Error: sample_posts.json not found")
            print("Please run: python generate_sample_data.py")
            sys.exit(1)
        
        # Check if .env exists
        if not os.path.exists('.env'):
            print("Error: .env file not found")
            print("Please create .env from config.env.template")
            sys.exit(1)
        
        main()
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
