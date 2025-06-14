# filepath: d:\Abdullah\GENESYS RAG\src\embedding_manager.py
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import numpy as np

class EmbeddingManager:
    def __init__(self, collection_name: str = "arxiv_papers"):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.Client(Settings(
            persist_directory="./chroma_db",
            anonymized_telemetry=False
        ))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for a list of texts."""
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the Chroma DB collection."""
        ids = [doc['chunk_id'] for doc in documents]
        texts = [doc['text'] for doc in documents]
        
        # Handle metadata - ensure it's not empty
        metadatas = []
        for doc in documents:
            # If metadata is empty, add a default value
            metadata = doc['metadata'] if doc['metadata'] else {"source": "document"}
            metadatas.append(metadata)
        
        # Create embeddings
        embeddings = self.create_embeddings(texts)
        
        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
    
    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents using a query."""
        query_embedding = self.create_embeddings([query])[0]
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['ids'][0])):
            formatted_results.append({
                'id': results['ids'][0][i],
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })
        
        return formatted_results
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        return {
            "count": self.collection.count(),
            "name": self.collection.name
        }
    def clear_documents(self):
        """Clear all documents from the Chroma DB collection."""
        # Get all document IDs first
        all_docs = self.collection.get()
        if all_docs['ids']:
            # Delete all documents by their IDs
            self.collection.delete(ids=all_docs['ids'])
