"""
Database module for related content system
Handles all MySQL database operations
"""

import mysql.connector
from mysql.connector import Error, pooling
import numpy as np
import pickle
import logging
from typing import List, Dict, Optional, Tuple
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and operations for post embeddings"""
    
    def __init__(self, config: Dict[str, str]):
        """
        Initialize database manager
        
        Args:
            config: Dictionary with DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
        """
        self.config = config
        self.pool = None
        self._create_connection_pool()
    
    def _create_connection_pool(self):
        """Create a connection pool for better performance"""
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name="related_content_pool",
                pool_size=5,
                pool_reset_session=True,
                host=self.config['DB_HOST'],
                port=int(self.config.get('DB_PORT', 3306)),
                database=self.config['DB_NAME'],
                user=self.config['DB_USER'],
                password=self.config['DB_PASSWORD'],
                charset='utf8mb4',
                use_unicode=True
            )
            logger.info("Database connection pool created successfully")
        except Error as e:
            logger.error(f"Error creating connection pool: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        connection = None
        try:
            connection = self.pool.get_connection()
            yield connection
        except Error as e:
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if connection and connection.is_connected():
                connection.close()
    
    def insert_embedding(self, post_id: int, embedding: np.ndarray, 
                        model_name: str, language: str, content_hash: str) -> bool:
        """
        Insert or update post embedding in database
        
        Args:
            post_id: WordPress post ID
            embedding: Numpy array of embedding vectors
            model_name: Name of the embedding model used
            language: Language code (e.g., 'en', 'fr', 'vi')
            content_hash: SHA256 hash of content for change detection
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Serialize embedding to binary
            embedding_blob = pickle.dumps(embedding.astype(np.float32))
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                INSERT INTO wp_post_embeddings 
                (post_id, embedding, embedding_model, language, content_hash)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    embedding = VALUES(embedding),
                    embedding_model = VALUES(embedding_model),
                    language = VALUES(language),
                    content_hash = VALUES(content_hash),
                    updated_at = CURRENT_TIMESTAMP
                """
                
                cursor.execute(query, (post_id, embedding_blob, model_name, language, content_hash))
                conn.commit()
                
                logger.debug(f"Inserted/updated embedding for post {post_id}")
                return True
                
        except Error as e:
            logger.error(f"Error inserting embedding for post {post_id}: {e}")
            return False
    
    def get_embedding(self, post_id: int) -> Optional[Tuple[np.ndarray, str]]:
        """
        Retrieve embedding for a post
        
        Args:
            post_id: WordPress post ID
            
        Returns:
            Tuple of (embedding array, language) or None if not found
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                SELECT embedding, language 
                FROM wp_post_embeddings 
                WHERE post_id = %s
                """
                
                cursor.execute(query, (post_id,))
                result = cursor.fetchone()
                
                if result:
                    embedding = pickle.loads(result[0])
                    language = result[1]
                    return (embedding, language)
                
                return None
                
        except Error as e:
            logger.error(f"Error retrieving embedding for post {post_id}: {e}")
            return None
    
    def get_all_embeddings(self, language: Optional[str] = None) -> Dict[int, np.ndarray]:
        """
        Retrieve all embeddings, optionally filtered by language
        
        Args:
            language: Optional language filter (e.g., 'en', 'fr')
            
        Returns:
            Dictionary mapping post_id to embedding array
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if language:
                    query = """
                    SELECT pe.post_id, pe.embedding 
                    FROM wp_post_embeddings pe
                    JOIN wp_posts p ON pe.post_id = p.ID
                    WHERE pe.language = %s AND p.post_status = 'publish'
                    """
                    cursor.execute(query, (language,))
                else:
                    query = """
                    SELECT pe.post_id, pe.embedding 
                    FROM wp_post_embeddings pe
                    JOIN wp_posts p ON pe.post_id = p.ID
                    WHERE p.post_status = 'publish'
                    """
                    cursor.execute(query)
                
                results = cursor.fetchall()
                
                embeddings = {}
                for post_id, embedding_blob in results:
                    embeddings[post_id] = pickle.loads(embedding_blob)
                
                logger.info(f"Retrieved {len(embeddings)} embeddings" + 
                          (f" for language '{language}'" if language else ""))
                return embeddings
                
        except Error as e:
            logger.error(f"Error retrieving embeddings: {e}")
            return {}
    
    def insert_similarities(self, similarities: List[Tuple[int, int, float]]) -> bool:
        """
        Batch insert similarity scores
        
        Args:
            similarities: List of tuples (source_post_id, related_post_id, score)
            
        Returns:
            True if successful, False otherwise
        """
        if not similarities:
            return True
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                INSERT INTO wp_post_similarities 
                (source_post_id, related_post_id, similarity_score)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    similarity_score = VALUES(similarity_score),
                    updated_at = CURRENT_TIMESTAMP
                """
                
                cursor.executemany(query, similarities)
                conn.commit()
                
                logger.info(f"Inserted {len(similarities)} similarity scores")
                return True
                
        except Error as e:
            logger.error(f"Error inserting similarities: {e}")
            return False
    
    def get_related_posts(self, post_id: int, limit: int = 10, 
                         min_score: float = 0.3) -> List[Dict]:
        """
        Get related posts for a given post
        
        Args:
            post_id: Source post ID
            limit: Maximum number of related posts to return
            min_score: Minimum similarity score threshold
            
        Returns:
            List of dictionaries with related post information
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                
                query = """
                SELECT 
                    ps.related_post_id,
                    ps.similarity_score,
                    p.post_title,
                    p.post_date,
                    p.post_name as slug,
                    pe.language
                FROM wp_post_similarities ps
                JOIN wp_posts p ON ps.related_post_id = p.ID
                JOIN wp_post_embeddings pe ON ps.related_post_id = pe.post_id
                WHERE ps.source_post_id = %s
                    AND ps.similarity_score >= %s
                    AND p.post_status = 'publish'
                ORDER BY ps.similarity_score DESC
                LIMIT %s
                """
                
                cursor.execute(query, (post_id, min_score, limit))
                results = cursor.fetchall()
                
                return results
                
        except Error as e:
            logger.error(f"Error getting related posts for {post_id}: {e}")
            return []
    
    def delete_similarities_for_post(self, post_id: int) -> bool:
        """
        Delete all similarity records for a post (when updating)
        
        Args:
            post_id: Post ID to clear similarities for
            
        Returns:
            True if successful
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                DELETE FROM wp_post_similarities 
                WHERE source_post_id = %s
                """
                
                cursor.execute(query, (post_id,))
                conn.commit()
                
                logger.debug(f"Deleted similarities for post {post_id}")
                return True
                
        except Error as e:
            logger.error(f"Error deleting similarities for post {post_id}: {e}")
            return False
    
    def get_posts_without_embeddings(self) -> List[int]:
        """
        Get list of published post IDs that don't have embeddings
        
        Returns:
            List of post IDs
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                SELECT p.ID 
                FROM wp_posts p
                LEFT JOIN wp_post_embeddings pe ON p.ID = pe.post_id
                WHERE p.post_status = 'publish'
                    AND p.post_type = 'post'
                    AND pe.post_id IS NULL
                """
                
                cursor.execute(query)
                results = cursor.fetchall()
                
                post_ids = [row[0] for row in results]
                logger.info(f"Found {len(post_ids)} posts without embeddings")
                return post_ids
                
        except Error as e:
            logger.error(f"Error getting posts without embeddings: {e}")
            return []
    
    def check_content_changed(self, post_id: int, new_hash: str) -> bool:
        """
        Check if post content has changed since last embedding
        
        Args:
            post_id: Post ID to check
            new_hash: New content hash
            
        Returns:
            True if content has changed or no embedding exists
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                SELECT content_hash 
                FROM wp_post_embeddings 
                WHERE post_id = %s
                """
                
                cursor.execute(query, (post_id,))
                result = cursor.fetchone()
                
                if not result:
                    return True  # No embedding exists
                
                return result[0] != new_hash  # Compare hashes
                
        except Error as e:
            logger.error(f"Error checking content change for post {post_id}: {e}")
            return True  # Assume changed on error
