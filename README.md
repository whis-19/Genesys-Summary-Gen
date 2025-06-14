# Document Summarization App

A powerful Document Summarization application built using Retrieval-Augmented Generation (RAG) architecture. This app allows users to upload PDF documents, processes them into chunks, stores them in a vector database, and generates comprehensive summaries using advanced language models.

## Table of Contents

- [Document Summarization App](#document-summarization-app)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Tech Stack](#tech-stack)
  - [RAG Architecture](#rag-architecture)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [Project Structure](#project-structure)
  - [Key Components](#key-components)
    - [Document Processing](#document-processing)
    - [Smart Chunking](#smart-chunking)
    - [Vector Embeddings](#vector-embeddings)
    - [Summary Generation](#summary-generation)
  - [Dependencies](#dependencies)
  - [Performance Tips](#performance-tips)
  - [Troubleshooting](#troubleshooting)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- **Document Upload**: Support for PDF document upload and processing
- **Smart Chunking**: Intelligent text segmentation with configurable chunk sizes and overlap
- **Vector Storage**: Efficient document storage using ChromaDB vector database
- **Semantic Search**: Advanced retrieval using sentence transformers for embeddings
- **AI-Powered Summarization**: Generate comprehensive summaries using Gemini's Llama models
- **Summary Management**: Save generated summaries to local files
- **Clean Interface**: User-friendly Streamlit web interface
- **Real-time Processing**: Instant document processing and summary generation

## Tech Stack

- **Frontend**: Streamlit for web interface
- **Document Processing**: PyPDF2 for PDF parsing
- **Vector Database**: ChromaDB for embedding storage and retrieval
- **Embeddings**: SentenceTransformers (`all-MiniLM-L6-v2` model)
- **Language Model**: Gemini API with Llama-3.1-70b-versatile
- **Text Processing**: Custom chunking algorithms
- **Backend**: Python with modular architecture

## RAG Architecture

The application implements a sophisticated Retrieval-Augmented Generation pipeline:

1. **Document Ingestion**: PDFs are loaded and parsed into raw text
2. **Text Chunking**: Documents are split into overlapping chunks for better context preservation
3. **Embedding Generation**: Each chunk is converted to vector embeddings using sentence transformers
4. **Vector Storage**: Embeddings are stored in ChromaDB for efficient similarity search
5. **Query Processing**: User queries are embedded and used to retrieve relevant chunks
6. **Context Augmentation**: Retrieved chunks provide context for the language model
7. **Summary Generation**: Gemini's Llama model generates comprehensive summaries

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Gemini API key (get from [Gemini API](https://aistudio.google.com/app/u/1/apikey))

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/whis-19/Genesys-Summary-Gen.git
   cd Genesys-Summary-Gen
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv .venv

   # On Windows
   .venv\Scripts\activate

   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:

   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Configuration

The application can be configured through the following parameters:

- **Chunk Size**: Default 1000 characters (configurable in `document_processor.py`)
- **Chunk Overlap**: Default 200 characters for context preservation
- **Embedding Model**: `all-MiniLM-L6-v2` (can be changed in `embedding_manager.py`)
- **Retrieval Count**: Top 5 most similar chunks (configurable in `rag_pipeline.py`)
- **Language Model**: Llama-3.1-70b-versatile via Gemini API

## Usage

1. **Start the application** by running `streamlit run app.py`
2. **Upload a PDF document** using the file uploader
3. **Wait for processing** - the app will chunk and embed your document
4. **Review the summary** generated automatically
5. **Save the summary** using the "Save Summary" button (optional)
6. **Upload new documents** - previous chunks are automatically cleared

## Project Structure

```
genesys-rag/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .env                  # Environment variables (create this)
├── summaries/            # Saved summaries directory
├── src/
│   ├── __init__.py
│   ├── document_processor.py    # PDF processing and chunking
│   ├── embedding_manager.py     # Vector embeddings and ChromaDB
│   └── rag_pipeline.py         # RAG implementation and summary generation

```

## Key Components

### Document Processing

- Extracts text from PDF files using PyPDF2
- Handles various PDF formats and encodings
- Implements robust error handling for corrupted files

### Smart Chunking

- Splits documents into overlapping chunks for better context
- Preserves sentence boundaries where possible
- Configurable chunk size and overlap parameters

### Vector Embeddings

- Uses SentenceTransformers for high-quality embeddings
- Stores vectors in ChromaDB for fast similarity search
- Supports incremental document addition and clearing

### Summary Generation

- Leverages Gemini's Llama-3.1-70b-versatile model
- Implements context-aware prompting
- Generates comprehensive, structured summaries

## Dependencies

- **streamlit**: Web application framework
- **PyPDF2**: PDF document processing
- **chromadb**: Vector database for embeddings
- **sentence-transformers**: Text embedding generation
- **gemin**: API client for gemini language models
- **python-dotenv**: Environment variable management

## Performance Tips

- **Chunk Size**: Larger chunks (1000+ chars) provide better context but slower processing
- **Overlap**: 20% overlap (200 chars for 1000 char chunks) balances context and efficiency
- **Batch Processing**: For multiple documents, process them sequentially to avoid memory issues
- **Model Selection**: The `all-MiniLM-L6-v2` model provides a good balance of speed and quality

## Troubleshooting

### Common Issues

1. **Import Errors**:

   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

2. **Gemini API Errors**:

   - Verify your API key in the `.env` file
   - Check your Gemini account quota and limits

3. **ChromaDB Issues**:

   - Delete the `chroma_db` folder and restart the application
   - Check disk space for database storage

4. **PDF Processing Errors**:

   - Ensure PDFs are not password-protected
   - Try with different PDF files to isolate the issue

5. **Memory Issues**:
   - Reduce chunk size for large documents
   - Process documents one at a time

### Performance Issues

- Clear the vector database periodically
- Use smaller embedding models for faster processing
- Optimize chunk size based on your document types

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request
