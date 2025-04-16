"""
Knowledge Base for Retrieval-Augmented Generation (RAG).

This module implements a vector store for the RAG pipeline, supporting
embedding generation, storage, and semantic search of documents.
"""

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple

import numpy as np
from openai import OpenAI
from pydantic import BaseModel, Field

from llamasearch_experimentalagents_product_growth.utils.config import get_settings, load_dotenv
from llamasearch_experimentalagents_product_growth.utils.logging import setup_logging

# Load environment variables
load_dotenv()

# Set up logging
logger = setup_logging()


@dataclass
class KnowledgeChunk:
    """A chunk of knowledge from a document with its embedding vector."""
    
    # Content and metadata
    content: str
    source: str
    chunk_id: str = field(default_factory=lambda: f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{id(object)}")
    embedding: Optional[List[float]] = None
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self) -> None:
        """Ensure metadata has basic fields."""
        if not self.metadata.get("source_type"):
            # Try to infer source type from extension
            if "." in self.source:
                ext = self.source.split(".")[-1].lower()
                if ext in ["md", "markdown"]:
                    self.metadata["source_type"] = "markdown"
                elif ext in ["txt", "text"]:
                    self.metadata["source_type"] = "plaintext"
                elif ext in ["py", "python"]:
                    self.metadata["source_type"] = "code"
                elif ext in ["csv"]:
                    self.metadata["source_type"] = "data"
                elif ext in ["json"]:
                    self.metadata["source_type"] = "data"
                else:
                    self.metadata["source_type"] = "unknown"
            else:
                self.metadata["source_type"] = "unknown"


class VectorStoreType:
    """Vector store types supported by the system."""
    
    SQLITE = "sqlite"
    FAISS = "faiss"
    MEMORY = "memory"


class EmbeddingGenerator:
    """Generates embeddings for text using OpenAI or other models."""
    
    def __init__(
        self,
        model: str = "text-embedding-ada-002",
        api_key: Optional[str] = None,
        fallback_to_local: bool = True,
    ):
        """
        Initialize the embedding generator.
        
        Args:
            model: The embedding model to use
            api_key: OpenAI API key (defaults to environment variable)
            fallback_to_local: Whether to fall back to local models if API fails
        """
        self.model = model
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.fallback_to_local = fallback_to_local
        
        # Initialize OpenAI client if API key is available
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        
        # State to track API failures
        self.api_failed = False
    
    def generate(self, text: str) -> List[float]:
        """
        Generate an embedding for the given text.
        
        Args:
            text: The text to generate an embedding for
            
        Returns:
            A list of floats representing the embedding vector
        """
        # First try OpenAI API if available and not failed before
        if self.client and not self.api_failed:
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=text,
                )
                return response.data[0].embedding
            except Exception as e:
                logger.warning(f"Error generating embedding with OpenAI: {e}")
                self.api_failed = True
                
                # Fall back to local model if enabled
                if self.fallback_to_local:
                    logger.info("Falling back to local embedding model")
                    return self._generate_local(text)
                else:
                    raise
        
        # Use local model if API is not available or failed before
        return self._generate_local(text)
    
    def _generate_local(self, text: str) -> List[float]:
        """
        Generate an embedding using a local model.
        
        Args:
            text: The text to generate an embedding for
            
        Returns:
            A list of floats representing the embedding vector
        """
        try:
            # Try to use Simon Willison's llm CLI if installed
            import subprocess
            import json
            
            # Use llm CLI to generate embedding
            try:
                result = subprocess.run(
                    ["llm", "embed", "-f", "json", text],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                embedding_data = json.loads(result.stdout)
                return embedding_data["embedding"]
            except (subprocess.SubprocessError, json.JSONDecodeError) as e:
                logger.warning(f"Error using llm CLI for embeddings: {e}")
                
            # Try to use sentence-transformers if installed
            try:
                from sentence_transformers import SentenceTransformer
                
                # Load model (first run will download it)
                model = SentenceTransformer("all-MiniLM-L6-v2")
                
                # Generate embedding
                embedding = model.encode(text)
                return embedding.tolist()
            except ImportError:
                logger.warning("sentence-transformers not installed")
            
            # Last resort: generate a random embedding
            # This is just a fallback and not suitable for production
            logger.warning("Using random embedding (NOT SUITABLE FOR PRODUCTION)")
            import numpy as np
            
            # Generate a random embedding with 1536 dimensions (same as OpenAI's ada-002)
            embedding = np.random.normal(0, 1, 1536)
            
            # Normalize to unit length
            embedding = embedding / np.linalg.norm(embedding)
            
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"Failed to generate local embedding: {e}")
            raise


class KnowledgeBase:
    """A knowledge base for storing and retrieving document embeddings."""
    
    def __init__(
        self,
        name: str = "default",
        description: str = "Default knowledge base",
        vector_store_type: str = VectorStoreType.SQLITE,
        vector_store_path: Optional[str] = None,
        embedding_model: str = "text-embedding-ada-002",
    ):
        """
        Initialize the knowledge base.
        
        Args:
            name: Name of the knowledge base
            description: Description of the knowledge base
            vector_store_type: Type of vector store to use
            vector_store_path: Path to the vector store
            embedding_model: Model to use for generating embeddings
        """
        self.name = name
        self.description = description
        self.vector_store_type = vector_store_type
        
        # Set default vector store path if not provided
        settings = get_settings()
        if vector_store_path is None:
            if vector_store_type == VectorStoreType.SQLITE:
                vector_store_path = settings.vector_db_path
            elif vector_store_type == VectorStoreType.FAISS:
                vector_store_path = Path(settings.vector_db_path).with_suffix(".faiss")
        
        self.vector_store_path = vector_store_path
        
        # Create embedding generator
        self.embedding_generator = EmbeddingGenerator(model=embedding_model)
        
        # Initialize vector store based on type
        self._init_vector_store()
        
        # Cache of chunks
        self.chunks: List[KnowledgeChunk] = []
        
        # Load chunks from store if it exists
        self._load_chunks()
    
    def _init_vector_store(self) -> None:
        """Initialize the vector store based on the configured type."""
        if self.vector_store_type == VectorStoreType.SQLITE:
            self._init_sqlite_store()
        elif self.vector_store_type == VectorStoreType.FAISS:
            self._init_faiss_store()
        elif self.vector_store_type == VectorStoreType.MEMORY:
            # Memory store uses in-memory lists, so no initialization needed
            pass
        else:
            raise ValueError(f"Unsupported vector store type: {self.vector_store_type}")
    
    def _init_sqlite_store(self) -> None:
        """Initialize the SQLite vector store."""
        try:
            from sqlite_utils import Database
            
            # Ensure directory exists
            if self.vector_store_path:
                os.makedirs(os.path.dirname(self.vector_store_path), exist_ok=True)
                
                # Create database connection
                self.db = Database(self.vector_store_path)
                
                # Create tables if they don't exist
                if "chunks" not in self.db.table_names():
                    self.db["chunks"].create({
                        "chunk_id": str,
                        "content": str,
                        "source": str,
                        "metadata": str,  # JSON string
                        "created_at": str,
                    }, pk="chunk_id")
                
                if "embeddings" not in self.db.table_names():
                    self.db["embeddings"].create({
                        "chunk_id": str,
                        "embedding": str,  # JSON string
                    }, pk="chunk_id")
                
                logger.info(f"Initialized SQLite vector store at {self.vector_store_path}")
            else:
                logger.warning("No vector store path provided for SQLite store")
        
        except ImportError:
            logger.error("sqlite-utils is required for SQLite vector store")
            raise
    
    def _init_faiss_store(self) -> None:
        """Initialize the FAISS vector store."""
        try:
            import faiss
            
            # Store FAISS index if needed
            self.index = None
            
            # Load existing index if it exists
            if self.vector_store_path and os.path.exists(self.vector_store_path):
                try:
                    self.index = faiss.read_index(self.vector_store_path)
                    logger.info(f"Loaded FAISS index from {self.vector_store_path}")
                except Exception as e:
                    logger.warning(f"Failed to load FAISS index: {e}")
            
            # Create a new index if needed
            if self.index is None:
                # Default to L2 distance and 1536 dimensions (OpenAI ada-002)
                self.index = faiss.IndexFlatL2(1536)
                logger.info("Created new FAISS index")
            
            # Load metadata if it exists
            self.metadata_path = str(Path(self.vector_store_path).with_suffix(".json"))
            self.chunk_metadata = {}
            
            if os.path.exists(self.metadata_path):
                try:
                    with open(self.metadata_path, "r") as f:
                        self.chunk_metadata = json.load(f)
                except Exception as e:
                    logger.warning(f"Failed to load FAISS metadata: {e}")
        
        except ImportError:
            logger.error("faiss-cpu is required for FAISS vector store")
            raise
    
    def _load_chunks(self) -> None:
        """Load chunks from the vector store."""
        if self.vector_store_type == VectorStoreType.SQLITE:
            self._load_chunks_from_sqlite()
        elif self.vector_store_type == VectorStoreType.FAISS:
            self._load_chunks_from_faiss()
        # Memory store starts empty, so no loading needed
    
    def _load_chunks_from_sqlite(self) -> None:
        """Load chunks from the SQLite vector store."""
        if not hasattr(self, "db"):
            logger.warning("SQLite database not initialized")
            return
        
        try:
            # Get all chunks
            chunks_data = self.db["chunks"].rows
            embeddings_data = {row["chunk_id"]: json.loads(row["embedding"]) 
                              for row in self.db["embeddings"].rows}
            
            # Convert to KnowledgeChunk objects
            for chunk_data in chunks_data:
                chunk_id = chunk_data["chunk_id"]
                
                # Parse metadata and created_at
                metadata = json.loads(chunk_data["metadata"]) if chunk_data["metadata"] else {}
                created_at = datetime.fromisoformat(chunk_data["created_at"])
                
                # Get embedding
                embedding = embeddings_data.get(chunk_id)
                
                # Create chunk
                chunk = KnowledgeChunk(
                    content=chunk_data["content"],
                    source=chunk_data["source"],
                    chunk_id=chunk_id,
                    embedding=embedding,
                    metadata=metadata,
                    created_at=created_at,
                )
                
                self.chunks.append(chunk)
            
            logger.info(f"Loaded {len(self.chunks)} chunks from SQLite store")
        
        except Exception as e:
            logger.error(f"Error loading chunks from SQLite: {e}")
    
    def _load_chunks_from_faiss(self) -> None:
        """Load chunks from the FAISS vector store."""
        if not hasattr(self, "chunk_metadata") or not self.chunk_metadata:
            logger.warning("No FAISS metadata available")
            return
        
        try:
            # Convert metadata to chunks
            for chunk_id, metadata in self.chunk_metadata.items():
                # Extract chunk data from metadata
                chunk = KnowledgeChunk(
                    content=metadata["content"],
                    source=metadata["source"],
                    chunk_id=chunk_id,
                    embedding=None,  # FAISS stores embeddings separately
                    metadata=metadata.get("metadata", {}),
                    created_at=datetime.fromisoformat(metadata["created_at"]),
                )
                
                self.chunks.append(chunk)
            
            logger.info(f"Loaded {len(self.chunks)} chunks from FAISS metadata")
        
        except Exception as e:
            logger.error(f"Error loading chunks from FAISS: {e}")
    
    def add_chunk(self, chunk: KnowledgeChunk, compute_embedding: bool = True) -> None:
        """
        Add a chunk to the knowledge base.
        
        Args:
            chunk: The chunk to add
            compute_embedding: Whether to compute embedding if not present
        """
        # Compute embedding if not present and requested
        if chunk.embedding is None and compute_embedding:
            chunk.embedding = self.embedding_generator.generate(chunk.content)
        
        # Add to the store
        if self.vector_store_type == VectorStoreType.SQLITE:
            self._add_chunk_to_sqlite(chunk)
        elif self.vector_store_type == VectorStoreType.FAISS:
            self._add_chunk_to_faiss(chunk)
        elif self.vector_store_type == VectorStoreType.MEMORY:
            # Just add to in-memory list
            pass
        
        # Add to chunks list
        self.chunks.append(chunk)
    
    def _add_chunk_to_sqlite(self, chunk: KnowledgeChunk) -> None:
        """Add a chunk to the SQLite vector store."""
        if not hasattr(self, "db"):
            logger.warning("SQLite database not initialized")
            return
        
        try:
            # Add chunk to chunks table
            self.db["chunks"].insert({
                "chunk_id": chunk.chunk_id,
                "content": chunk.content,
                "source": chunk.source,
                "metadata": json.dumps(chunk.metadata),
                "created_at": chunk.created_at.isoformat(),
            }, pk="chunk_id", replace=True)
            
            # Add embedding to embeddings table if present
            if chunk.embedding is not None:
                self.db["embeddings"].insert({
                    "chunk_id": chunk.chunk_id,
                    "embedding": json.dumps(chunk.embedding),
                }, pk="chunk_id", replace=True)
        
        except Exception as e:
            logger.error(f"Error adding chunk to SQLite: {e}")
    
    def _add_chunk_to_faiss(self, chunk: KnowledgeChunk) -> None:
        """Add a chunk to the FAISS vector store."""
        if not hasattr(self, "index"):
            logger.warning("FAISS index not initialized")
            return
        
        try:
            # Add embedding to FAISS index if present
            if chunk.embedding is not None:
                # Convert to numpy array
                import numpy as np
                vector = np.array([chunk.embedding], dtype=np.float32)
                
                # Add to index
                self.index.add(vector)
                
                # Update metadata
                self.chunk_metadata[chunk.chunk_id] = {
                    "content": chunk.content,
                    "source": chunk.source,
                    "metadata": chunk.metadata,
                    "created_at": chunk.created_at.isoformat(),
                }
                
                # Save metadata to file
                if hasattr(self, "metadata_path"):
                    with open(self.metadata_path, "w") as f:
                        json.dump(self.chunk_metadata, f)
                
                # Save index to file
                if hasattr(self, "vector_store_path"):
                    import faiss
                    faiss.write_index(self.index, self.vector_store_path)
        
        except Exception as e:
            logger.error(f"Error adding chunk to FAISS: {e}")
    
    def add_chunks(self, chunks: List[KnowledgeChunk], compute_embeddings: bool = True) -> None:
        """
        Add multiple chunks to the knowledge base.
        
        Args:
            chunks: The chunks to add
            compute_embeddings: Whether to compute embeddings if not present
        """
        for chunk in chunks:
            self.add_chunk(chunk, compute_embedding=compute_embeddings)
    
    def search(
        self, 
        query: Union[str, List[float]], 
        top_k: int = 5,
        threshold: float = 0.6
    ) -> List[Dict[str, Any]]:
        """
        Search the knowledge base for chunks similar to the query.
        
        Args:
            query: The search query (either text or embedding vector)
            top_k: Number of results to return
            threshold: Similarity threshold (0-1)
            
        Returns:
            A list of search results with scores
        """
        # Convert query to embedding if it's a string
        query_embedding = query
        if isinstance(query, str):
            query_embedding = self.embedding_generator.generate(query)
        
        # Search based on store type
        if self.vector_store_type == VectorStoreType.SQLITE:
            return self._search_sqlite(query_embedding, top_k, threshold)
        elif self.vector_store_type == VectorStoreType.FAISS:
            return self._search_faiss(query_embedding, top_k, threshold)
        elif self.vector_store_type == VectorStoreType.MEMORY:
            return self._search_memory(query_embedding, top_k, threshold)
        else:
            raise ValueError(f"Unsupported vector store type: {self.vector_store_type}")
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            a: First vector
            b: Second vector
            
        Returns:
            Cosine similarity (0-1)
        """
        # Use Rust implementation if available
        try:
            from llamasearch_experimentalagents_product_growth.rust import cosine_similarity
            return cosine_similarity([a], [b])[0]
        except (ImportError, AttributeError):
            # Fall back to numpy
            import numpy as np
            a_array = np.array(a)
            b_array = np.array(b)
            
            # Calculate cosine similarity
            dot_product = np.dot(a_array, b_array)
            norm_a = np.linalg.norm(a_array)
            norm_b = np.linalg.norm(b_array)
            
            # Handle zero norms
            if norm_a == 0 or norm_b == 0:
                return 0.0
                
            return dot_product / (norm_a * norm_b)
    
    def _search_memory(
        self, 
        query_embedding: List[float], 
        top_k: int, 
        threshold: float
    ) -> List[Dict[str, Any]]:
        """
        Search the in-memory store.
        
        Args:
            query_embedding: The query embedding vector
            top_k: Number of results to return
            threshold: Similarity threshold (0-1)
            
        Returns:
            A list of search results with scores
        """
        # Get chunks with embeddings
        valid_chunks = [c for c in self.chunks if c.embedding is not None]
        
        # Calculate similarities
        similarities = []
        for i, chunk in enumerate(valid_chunks):
            score = self._cosine_similarity(query_embedding, chunk.embedding)
            similarities.append((i, score))
        
        # Sort by score (descending) and filter by threshold
        similarities.sort(key=lambda x: x[1], reverse=True)
        filtered_similarities = [(i, score) for i, score in similarities if score >= threshold]
        
        # Take top_k
        top_indices = [i for i, _ in filtered_similarities[:top_k]]
        
        # Convert to results
        results = []
        for idx, (chunk_idx, score) in enumerate(filtered_similarities[:top_k]):
            chunk = valid_chunks[chunk_idx]
            
            results.append({
                "chunk_id": chunk.chunk_id,
                "content": chunk.content,
                "source": chunk.source,
                "score": float(score),
                "metadata": chunk.metadata
            })
        
        return results
    
    def _search_sqlite(
        self, 
        query_embedding: List[float], 
        top_k: int, 
        threshold: float
    ) -> List[Dict[str, Any]]:
        """
        Search the SQLite vector store.
        
        Args:
            query_embedding: The query embedding vector
            top_k: Number of results to return
            threshold: Similarity threshold (0-1)
            
        Returns:
            A list of search results with scores
        """
        # For now, use the in-memory approach
        # In a real implementation, we'd use a SQL query with a vector extension
        return self._search_memory(query_embedding, top_k, threshold)
    
    def _search_faiss(
        self, 
        query_embedding: List[float], 
        top_k: int, 
        threshold: float
    ) -> List[Dict[str, Any]]:
        """
        Search the FAISS vector store.
        
        Args:
            query_embedding: The query embedding vector
            top_k: Number of results to return
            threshold: Similarity threshold (0-1)
            
        Returns:
            A list of search results with scores
        """
        if not hasattr(self, "index"):
            logger.warning("FAISS index not initialized")
            return []
        
        try:
            # Convert to numpy array
            import numpy as np
            query_vector = np.array([query_embedding], dtype=np.float32)
            
            # Search index
            distances, indices = self.index.search(query_vector, top_k)
            
            # Convert distances to scores (FAISS uses L2 distance, lower is better)
            # Transform to 0-1 range where 1 is best
            max_dist = 16.0  # Reasonable max L2 distance for normalized vectors
            scores = 1.0 - np.clip(distances[0] / max_dist, 0.0, 1.0)
            
            # Filter by threshold
            filtered_indices = [idx for idx, score in zip(indices[0], scores) if score >= threshold]
            filtered_scores = [score for score in scores if score >= threshold]
            
            # Get results from metadata
            results = []
            for idx, (faiss_idx, score) in enumerate(zip(filtered_indices, filtered_scores)):
                # Get chunk id from metadata (assumes sorted order)
                chunk_id = list(self.chunk_metadata.keys())[faiss_idx]
                metadata = self.chunk_metadata[chunk_id]
                
                results.append({
                    "chunk_id": chunk_id,
                    "content": metadata["content"],
                    "source": metadata["source"],
                    "score": float(score),
                    "metadata": metadata.get("metadata", {})
                })
            
            return results
        
        except Exception as e:
            logger.error(f"Error searching FAISS index: {e}")
            return []
    
    def get_all_embeddings(self) -> List[List[float]]:
        """
        Get all embeddings as a list.
        
        Returns:
            A list of embedding vectors
        """
        return [chunk.embedding for chunk in self.chunks if chunk.embedding is not None]
    
    def __len__(self) -> int:
        """Get the number of chunks in the knowledge base."""
        return len(self.chunks)


# Convenience function to create a knowledge base
def get_knowledge_base() -> KnowledgeBase:
    """
    Get or create a knowledge base instance.
    
    Returns:
        A KnowledgeBase instance
    """
    settings = get_settings()
    
    # Create knowledge base
    kb = KnowledgeBase(
        name=settings.knowledge_base_name,
        description=settings.knowledge_base_description,
        vector_store_type=settings.vector_store_type,
        vector_store_path=settings.vector_db_path,
        embedding_model=settings.embedding_model,
    )
    
    return kb 