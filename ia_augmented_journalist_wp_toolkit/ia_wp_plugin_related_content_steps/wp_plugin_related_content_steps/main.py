"""
Main script for processing WordPress posts and generating related content recommendations
"""

import os
import sys
import logging
import argparse
from typing import List, Dict, Optional
from dotenv import load_dotenv
import numpy as np
from tqdm import tqdm
import requests

from database import DatabaseManager
from embeddings import EmbeddingGenerator, ContentProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('related_content.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class WordPressConnector:
    """Handles communication with WordPress REST API"""
    
    def __init__(self, base_url: str, api_endpoint: str = '/wp-json/wp/v2/posts'):
        """
        Initialize WordPress connector
        
        Args:
            base_url: WordPress site URL
            api_endpoint: REST API endpoint path
        """
        self.base_url = base_url.rstrip('/')
        self.api_endpoint = api_endpoint
        self.api_url = f"{self.base_url}{self.api_endpoint}"
    
    def get_posts(self, per_page: int = 100, page: int = 1, 
                  status: str = 'publish') -> List[Dict]:
        """
        Fetch posts from WordPress REST API
        
        Args:
            per_page: Number of posts per page
            page: Page number
            status: Post status filter
            
        Returns:
            List of post dictionaries
        """
        try:
            params = {
                'per_page': per_page,
                'page': page,
                'status': status,
                '_embed': True  # Include embedded data like featured images
            }
            
            response = requests.get(self.api_url, params=params, timeout=30)
            response.raise_for_status()
            
            posts = response.json()
            logger.info(f"Fetched {len(posts)} posts from page {page}")
            return posts
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching posts: {e}")
            return []
    
    def get_all_posts(self, max_posts: Optional[int] = None) -> List[Dict]:
        """
        Fetch all published posts from WordPress
        
        Args:
            max_posts: Maximum number of posts to fetch (None = all)
            
        Returns:
            List of all posts
        """
        all_posts = []
        page = 1
        per_page = 100
        
        logger.info("Fetching all posts from WordPress...")
        
        while True:
            posts = self.get_posts(per_page=per_page, page=page)
            
            if not posts:
                break
            
            all_posts.extend(posts)
            
            if max_posts and len(all_posts) >= max_posts:
                all_posts = all_posts[:max_posts]
                break
            
            page += 1
        
        logger.info(f"Total posts fetched: {len(all_posts)}")
        return all_posts
    
    def get_post_by_id(self, post_id: int) -> Optional[Dict]:
        """
        Fetch a single post by ID
        
        Args:
            post_id: WordPress post ID
            
        Returns:
            Post dictionary or None
        """
        try:
            url = f"{self.api_url}/{post_id}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching post {post_id}: {e}")
            return None


class RelatedContentProcessor:
    """Main processor for generating related content recommendations"""
    
    def __init__(self, config: Dict[str, str]):
        """
        Initialize processor
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.db = DatabaseManager(config)
        self.embedder = EmbeddingGenerator(config.get('EMBEDDING_MODEL', 
                                                      'paraphrase-multilingual-mpnet-base-v2'))
        self.content_processor = ContentProcessor(
            max_length=int(config.get('MAX_CONTENT_LENGTH', 1000))
        )
        self.min_similarity = float(config.get('MIN_SIMILARITY_THRESHOLD', 0.3))
        self.max_related = int(config.get('MAX_RELATED_POSTS', 10))
        self.batch_size = int(config.get('BATCH_SIZE', 32))
    
    def process_single_post(self, post: Dict) -> bool:
        """
        Process a single post: generate and store embedding
        
        Args:
            post: WordPress post dictionary
            
        Returns:
            True if successful
        """
        try:
            post_id = post['id']
            
            # Prepare content
            prepared = self.content_processor.prepare_content(post)
            
            # Check if content has changed
            if not self.db.check_content_changed(post_id, prepared['hash']):
                logger.debug(f"Post {post_id} content unchanged, skipping")
                return True
            
            # Generate embedding
            embedding = self.embedder.generate_embedding(prepared['text'])
            
            # Store in database
            success = self.db.insert_embedding(
                post_id=post_id,
                embedding=embedding,
                model_name=self.embedder.model_name,
                language=prepared['language'],
                content_hash=prepared['hash']
            )
            
            if success:
                logger.info(f"Processed post {post_id} ({prepared['language']})")
            
            return success
            
        except Exception as e:
            logger.error(f"Error processing post {post.get('id', 'unknown')}: {e}")
            return False
    
    def process_posts_batch(self, posts: List[Dict]) -> int:
        """
        Process multiple posts in batch
        
        Args:
            posts: List of WordPress post dictionaries
            
        Returns:
            Number of successfully processed posts
        """
        success_count = 0
        
        logger.info(f"Processing {len(posts)} posts...")
        
        for post in tqdm(posts, desc="Processing posts"):
            if self.process_single_post(post):
                success_count += 1
        
        logger.info(f"Successfully processed {success_count}/{len(posts)} posts")
        return success_count
    
    def compute_similarities(self, post_id: Optional[int] = None, 
                            language: Optional[str] = None) -> int:
        """
        Compute and store similarity scores
        
        Args:
            post_id: If provided, compute only for this post
            language: If provided, compute only within this language
            
        Returns:
            Number of similarity pairs stored
        """
        if post_id:
            return self._compute_similarities_for_post(post_id, language)
        else:
            return self._compute_all_similarities(language)
    
    def _compute_similarities_for_post(self, post_id: int, 
                                       language: Optional[str] = None) -> int:
        """
        Compute similarities for a single post
        
        Args:
            post_id: Post ID to compute similarities for
            language: Optional language filter
            
        Returns:
            Number of similarity pairs stored
        """
        # Get embedding for target post
        result = self.db.get_embedding(post_id)
        if not result:
            logger.warning(f"No embedding found for post {post_id}")
            return 0
        
        target_embedding, target_language = result
        
        # Use post's language if not specified
        if not language:
            language = target_language
        
        # Get all embeddings in the same language
        all_embeddings = self.db.get_all_embeddings(language=language)
        
        if post_id in all_embeddings:
            del all_embeddings[post_id]  # Remove self
        
        if not all_embeddings:
            logger.warning(f"No other embeddings found for language {language}")
            return 0
        
        # Compute similarities
        similarities = []
        post_ids = list(all_embeddings.keys())
        embeddings_matrix = np.array([all_embeddings[pid] for pid in post_ids])
        
        scores = self.embedder.cosine_similarity_batch(target_embedding, embeddings_matrix)
        
        for pid, score in zip(post_ids, scores):
            if score >= self.min_similarity:
                similarities.append((post_id, pid, float(score)))
        
        # Sort by score and keep top N
        similarities.sort(key=lambda x: x[2], reverse=True)
        similarities = similarities[:self.max_related]
        
        # Delete old similarities and insert new ones
        self.db.delete_similarities_for_post(post_id)
        self.db.insert_similarities(similarities)
        
        logger.info(f"Computed {len(similarities)} related posts for post {post_id}")
        return len(similarities)
    
    def _compute_all_similarities(self, language: Optional[str] = None) -> int:
        """
        Compute similarities for all posts
        
        Args:
            language: Optional language filter
            
        Returns:
            Total number of similarity pairs stored
        """
        all_embeddings = self.db.get_all_embeddings(language=language)
        
        if len(all_embeddings) < 2:
            logger.warning("Not enough posts with embeddings to compute similarities")
            return 0
        
        post_ids = list(all_embeddings.keys())
        embeddings_matrix = np.array([all_embeddings[pid] for pid in post_ids])
        
        logger.info(f"Computing pairwise similarities for {len(post_ids)} posts...")
        
        # Compute full similarity matrix
        similarity_matrix = self.embedder.pairwise_similarity_matrix(embeddings_matrix)
        
        # Extract top N similar posts for each post
        total_pairs = 0
        
        for i, source_post_id in enumerate(tqdm(post_ids, desc="Storing similarities")):
            similarities = []
            
            # Get similarities for this post (excluding self)
            scores = similarity_matrix[i]
            
            for j, target_post_id in enumerate(post_ids):
                if i != j and scores[j] >= self.min_similarity:
                    similarities.append((source_post_id, target_post_id, float(scores[j])))
            
            # Sort and keep top N
            similarities.sort(key=lambda x: x[2], reverse=True)
            similarities = similarities[:self.max_related]
            
            # Store in database
            if similarities:
                self.db.delete_similarities_for_post(source_post_id)
                self.db.insert_similarities(similarities)
                total_pairs += len(similarities)
        
        logger.info(f"Stored {total_pairs} total similarity pairs")
        return total_pairs
    
    def get_related_posts(self, post_id: int, limit: int = 5) -> List[Dict]:
        """
        Get related posts for display
        
        Args:
            post_id: Source post ID
            limit: Maximum number of related posts
            
        Returns:
            List of related post information
        """
        return self.db.get_related_posts(post_id, limit, self.min_similarity)


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='WordPress Related Content Processor')
    parser.add_argument('--action', choices=['process', 'similarities', 'query', 'full'],
                       default='full', help='Action to perform')
    parser.add_argument('--post-id', type=int, help='Specific post ID to process')
    parser.add_argument('--language', help='Language filter (e.g., en, fr, vi)')
    parser.add_argument('--max-posts', type=int, help='Maximum posts to fetch from WordPress')
    parser.add_argument('--config', default='.env', help='Path to config file')
    
    args = parser.parse_args()
    
    # Load configuration
    load_dotenv(args.config)
    
    config = {
        'DB_HOST': os.getenv('DB_HOST', 'localhost'),
        'DB_PORT': os.getenv('DB_PORT', '3306'),
        'DB_NAME': os.getenv('DB_NAME', 'wordpress'),
        'DB_USER': os.getenv('DB_USER'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD'),
        'WP_URL': os.getenv('WP_URL'),
        'WP_API_ENDPOINT': os.getenv('WP_API_ENDPOINT', '/wp-json/wp/v2/posts'),
        'EMBEDDING_MODEL': os.getenv('EMBEDDING_MODEL', 'paraphrase-multilingual-mpnet-base-v2'),
        'MAX_CONTENT_LENGTH': os.getenv('MAX_CONTENT_LENGTH', '1000'),
        'MIN_SIMILARITY_THRESHOLD': os.getenv('MIN_SIMILARITY_THRESHOLD', '0.3'),
        'MAX_RELATED_POSTS': os.getenv('MAX_RELATED_POSTS', '10'),
        'BATCH_SIZE': os.getenv('BATCH_SIZE', '32')
    }
    
    # Initialize processor
    processor = RelatedContentProcessor(config)
    
    try:
        if args.action in ['process', 'full']:
            # Fetch posts from WordPress
            wp = WordPressConnector(config['WP_URL'], config['WP_API_ENDPOINT'])
            
            if args.post_id:
                post = wp.get_post_by_id(args.post_id)
                if post:
                    processor.process_single_post(post)
            else:
                posts = wp.get_all_posts(max_posts=args.max_posts)
                processor.process_posts_batch(posts)
        
        if args.action in ['similarities', 'full']:
            # Compute similarities
            if args.post_id:
                processor.compute_similarities(post_id=args.post_id, language=args.language)
            else:
                processor.compute_similarities(language=args.language)
        
        if args.action == 'query' and args.post_id:
            # Query related posts
            related = processor.get_related_posts(args.post_id, limit=10)
            
            print(f"\nRelated posts for ID {args.post_id}:")
            print("-" * 80)
            
            for post in related:
                print(f"ID: {post['related_post_id']}")
                print(f"Title: {post['post_title']}")
                print(f"Score: {post['similarity_score']:.3f}")
                print(f"Language: {post['language']}")
                print(f"Date: {post['post_date']}")
                print("-" * 80)
        
        logger.info("Processing completed successfully")
        
    except Exception as e:
        logger.error(f"Error during processing: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
