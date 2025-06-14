import json
from typing import List, Dict, Any
from tqdm import tqdm
import tiktoken

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def load_json_data(self, file_path: str) -> List[Dict[str, Any]]:
        """Load data from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def create_chunks(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        tokens = self.tokenizer.encode(text)
        chunks = []
        
        for i in range(0, len(tokens), self.chunk_size - self.chunk_overlap):
            chunk_tokens = tokens[i:i + self.chunk_size]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
            
            if i + self.chunk_size >= len(tokens):
                break
                
        return chunks
    
    def process_document(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process a single document into chunks with metadata."""
        chunks = []
          # Combine title and abstract for processing
        text = f"Title: {document.get('title', '')}\n\nAbstract: {document.get('abstract', '')}"
        text_chunks = self.create_chunks(text)
        
        for i, chunk in enumerate(text_chunks):
            chunk_data = {
                'chunk_id': f"{document.get('id', '')}_{i}",
                'text': chunk,
                'metadata': {
                    'paper_id': document.get('id', ''),
                    'title': document.get('title', ''),
                    'authors': str(document.get('authors', [])),  # Convert list to string
                    'chunk_index': i,
                    'total_chunks': len(text_chunks)
                }
            }
            chunks.append(chunk_data)
            
        return chunks
    
    def process_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process multiple documents into chunks."""
        all_chunks = []
        for doc in tqdm(documents, desc="Processing documents"):
            chunks = self.process_document(doc)
            all_chunks.extend(chunks)
        return all_chunks 