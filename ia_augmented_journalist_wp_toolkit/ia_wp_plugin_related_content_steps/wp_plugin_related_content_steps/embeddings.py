"""
Embedding module for generating semantic vectors from text
Uses sentence-transformers for multilingual support
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union, Dict
import logging
from functools import lru_cache
import hashlib

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """Generates embeddings for text content using pre-trained models"""
    
    # Recommended models for multilingual content
    AVAILABLE_MODELS = {
        'paraphrase-multilingual-mpnet-base-v2': {
            'description': 'Best quality, supports 50+ languages',
            'dimension': 768,
            'size': '1.1GB'
        },
        'paraphrase-multilingual-MiniLM-L12-v2': {
            'description': 'Faster, smaller, good quality',
            'dimension': 384,
            'size': '420MB'
        },
        'distiluse-base-multilingual-cased-v2': {
            'description': 'Fast, 15+ languages',
            'dimension': 512,
            'size': '500MB'
        },
        'LaBSE': {
            'description': 'Best for 109 languages, larger model',
            'dimension': 768,
            'size': '1.9GB'
        }
    }
    
    def __init__(self, model_name: str = 'paraphrase-multilingual-mpnet-base-v2'):
        """
        Initialize embedding generator
        
        Args:
            model_name: Name of sentence-transformer model to use
        """
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model"""
        try:
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Model loaded successfully. Embedding dimension: {self.get_dimension()}")
        except Exception as e:
            logger.error(f"Error loading model {self.model_name}: {e}")
            raise
    
    def get_dimension(self) -> int:
        """Get embedding dimension of current model"""
        return self.model.get_sentence_embedding_dimension()
    
    @staticmethod
    def compute_content_hash(text: str) -> str:
        """
        Compute SHA256 hash of content for change detection
        
        Args:
            text: Content to hash
            
        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    def generate_embedding(self, text: str, normalize: bool = True) -> np.ndarray:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text
            normalize: Whether to L2-normalize the embedding
            
        Returns:
            Numpy array of embedding vector
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for embedding")
            return np.zeros(self.get_dimension(), dtype=np.float32)
        
        try:
            embedding = self.model.encode(
                text,
                convert_to_numpy=True,
                normalize_embeddings=normalize,
                show_progress_bar=False
            )
            return embedding.astype(np.float32)
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return np.zeros(self.get_dimension(), dtype=np.float32)
    
    def generate_embeddings_batch(self, texts: List[str], 
                                  batch_size: int = 32,
                                  normalize: bool = True,
                                  show_progress: bool = True) -> np.ndarray:
        """
        Generate embeddings for multiple texts in batches
        
        Args:
            texts: List of input texts
            batch_size: Batch size for processing
            normalize: Whether to L2-normalize embeddings
            show_progress: Show progress bar
            
        Returns:
            Numpy array of shape (len(texts), embedding_dim)
        """
        if not texts:
            return np.array([])
        
        try:
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                convert_to_numpy=True,
                normalize_embeddings=normalize,
                show_progress_bar=show_progress
            )
            return embeddings.astype(np.float32)
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            return np.zeros((len(texts), self.get_dimension()), dtype=np.float32)
    
    @staticmethod
    def cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score between 0 and 1
        """
        # If embeddings are already normalized, dot product = cosine similarity
        similarity = np.dot(embedding1, embedding2)
        
        # Ensure result is between 0 and 1
        # (normalized embeddings should give results in [-1, 1], map to [0, 1])
        return float((similarity + 1) / 2)
    
    @staticmethod
    def cosine_similarity_batch(embedding: np.ndarray, 
                               embeddings_matrix: np.ndarray) -> np.ndarray:
        """
        Calculate cosine similarity between one embedding and multiple embeddings
        
        Args:
            embedding: Single embedding vector (1D array)
            embeddings_matrix: Matrix of embeddings (2D array, each row is an embedding)
            
        Returns:
            Array of similarity scores
        """
        # For normalized vectors, cosine similarity = dot product
        similarities = np.dot(embeddings_matrix, embedding)
        
        # Map from [-1, 1] to [0, 1]
        return (similarities + 1) / 2
    
    @staticmethod
    def pairwise_similarity_matrix(embeddings: np.ndarray) -> np.ndarray:
        """
        Calculate pairwise similarity matrix for all embeddings
        
        Args:
            embeddings: Matrix of embeddings (each row is an embedding)
            
        Returns:
            Similarity matrix where element [i,j] is similarity between i and j
        """
        # For normalized vectors, cosine similarity = dot product
        similarity_matrix = np.dot(embeddings, embeddings.T)
        
        # Map from [-1, 1] to [0, 1]
        return (similarity_matrix + 1) / 2


class ContentProcessor:
    """Processes post content for embedding generation"""
    
    def __init__(self, max_length: int = 1000):
        """
        Initialize content processor
        
        Args:
            max_length: Maximum character length for content
        """
        self.max_length = max_length
    
    @staticmethod
    def clean_html(text: str) -> str:
        """
        Remove HTML tags from text
        
        Args:
            text: HTML text
            
        Returns:
            Clean text
        """
        from bs4 import BeautifulSoup
        
        try:
            soup = BeautifulSoup(text, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        except Exception as e:
            logger.warning(f"Error cleaning HTML: {e}")
            return text
    
    @staticmethod
    def detect_language(text: str) -> str:
        """
        Detect language of text
        
        Args:
            text: Input text
            
        Returns:
            ISO 639-1 language code (e.g., 'en', 'fr', 'vi')
        """
        from langdetect import detect, LangDetectException
        
        try:
            return detect(text)
        except LangDetectException:
            logger.warning("Could not detect language, defaulting to 'en'")
            return 'en'
    
    def prepare_content(self, post: Dict) -> Dict:
        """
        Prepare post content for embedding
        
        Args:
            post: Dictionary with 'title', 'content', 'excerpt' keys
            
        Returns:
            Dictionary with 'text', 'language', 'hash' keys
        """
        # Combine title and content
        title = post.get('title', {}).get('rendered', '') if isinstance(post.get('title'), dict) else post.get('title', '')
        content = post.get('content', {}).get('rendered', '') if isinstance(post.get('content'), dict) else post.get('content', '')
        excerpt = post.get('excerpt', {}).get('rendered', '') if isinstance(post.get('excerpt'), dict) else post.get('excerpt', '')
        
        # Clean HTML
        clean_title = self.clean_html(title)
        clean_content = self.clean_html(content or excerpt)
        
        # Create text: title is weighted more heavily
        combined_text = f"{clean_title}. {clean_title}. {clean_content}"
        
        # Truncate to max length
        if len(combined_text) > self.max_length:
            combined_text = combined_text[:self.max_length]
        
        # Detect language
        language = self.detect_language(clean_content or clean_title)
        
        # Compute hash for change detection
        content_hash = hashlib.sha256(
            (clean_title + clean_content).encode('utf-8')
        ).hexdigest()
        
        return {
            'text': combined_text,
            'language': language,
            'hash': content_hash
        }
    
    @staticmethod
    def extract_keywords(text: str, top_n: int = 10) -> List[str]:
        """
        Extract keywords using TF-IDF (optional enhancement)
        
        Args:
            text: Input text
            top_n: Number of keywords to extract
            
        Returns:
            List of keywords
        """
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        try:
            vectorizer = TfidfVectorizer(max_features=top_n, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([text])
            feature_names = vectorizer.get_feature_names_out()
            return list(feature_names)
        except Exception as e:
            logger.warning(f"Error extracting keywords: {e}")
            return []


def get_recommended_model(priority: str = 'quality') -> str:
    """
    Get recommended model based on priority
    
    Args:
        priority: 'quality', 'speed', or 'balanced'
        
    Returns:
        Model name
    """
    recommendations = {
        'quality': 'paraphrase-multilingual-mpnet-base-v2',
        'speed': 'paraphrase-multilingual-MiniLM-L12-v2',
        'balanced': 'paraphrase-multilingual-MiniLM-L12-v2',
        'max_languages': 'LaBSE'
    }
    
    return recommendations.get(priority, 'paraphrase-multilingual-mpnet-base-v2')
