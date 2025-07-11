import streamlit as st
import os
import tempfile
from src.document_processor import DocumentProcessor
from src.embedding_manager import EmbeddingManager
from src.summarizer_new import Summarizer  # Using the improved summarizer
from src.utils import count_tokens, timeit

# Initialize components
processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
embed_manager = EmbeddingManager()
summarizer = Summarizer()

st.title("📄 Document Summarization App")

# Add a brief description of the app
st.markdown("""
🚀 **Advanced RAG-powered Document Analysis**  
Generate intelligent summaries from your documents using Retrieval-Augmented Generation.  
📤 Upload PDF, TXT, or MD files • 📝 Get instant basic summaries • 📋 Generate detailed analysis
""")

uploaded_file = st.file_uploader("Drag and drop your paper (PDF, TXT, or Markdown)", type=["pdf", "txt", "md"])

if uploaded_file is not None:
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name
    
    # Clear previous chunks before processing the new file
    embed_manager.clear_documents()
    
    # Process the document
    # Handle file based on type
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    
    # For PDF files, use a different approach
    if file_extension == '.pdf':
        try:
            import PyPDF2
            with open(tmp_file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                content = ""
                for page in pdf_reader.pages:
                    content += page.extract_text() + "\n"
        except ImportError:
            st.error("PyPDF2 is not installed. Please install it with 'pip install PyPDF2'")
            content = "Error: Cannot process PDF files without PyPDF2."
    else:
        # For text files, try different encodings
        try:
            with open(tmp_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(tmp_file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            except UnicodeDecodeError:
                st.error("Unable to decode the file. Please check the file encoding.")
                content = "Error: Cannot process this file due to encoding issues."
    
    chunks = processor.create_chunks(content)
    st.write(f"Total chunks created: {len(chunks)}")

    # Embed and store chunks
    chunk_docs = []
    for i, chunk in enumerate(chunks):
        chunk_docs.append({
            "chunk_id": f"chunk_{i}",
            "text": chunk,
            "metadata": {"source": "uploaded_document", "index": i}
        })
    embed_manager.add_documents(chunk_docs)

    # Retrieve relevant chunks for summary
    summary_query = "Summarize this document."
    retrieved = embed_manager.search(summary_query, n_results=5)
    context_chunks = [item['text'] for item in retrieved]
    
    # Generate summary
    summary = summarizer.generate_summary(context_chunks, prompt=summary_query)

    # Display document information
    st.header("Document Information")
    st.subheader("File Details")
    st.write(f"**Filename:** {uploaded_file.name}")
    st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")
    st.write(f"**File Type:** {file_extension}")
    
    # Display document statistics
    st.subheader("Document Statistics")
    total_words = len(content.split())
    st.write(f"**Total Words:** {total_words}")
    st.write(f"**Total Chunks:** {len(chunks)}")
    st.write(f"**Tokens Used for Summary:** {sum(count_tokens(chunk) for chunk in context_chunks)}")
    
    # Display summary in a prominent box
    st.header("Document Summary")
    st.info(summary)
      # Show the top chunks used for generating the summary
    with st.expander("View Top Chunks Used for Summary"):
        for i, chunk in enumerate(context_chunks):
            st.markdown(f"**Chunk {i+1}**")
            st.text(chunk[:300] + "..." if len(chunk) > 300 else chunk)
            st.write("---")
    
    # Button for detailed summary
    st.header("📋 Detailed Summary")
    st.markdown("Generate a comprehensive analysis covering all key sections, methodologies, findings, and conclusions.")    
    # Add summary depth control
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Adjust the summary depth to control how much of the document is used:")
    with col2:
        summary_depth = st.select_slider(
            "Summary Depth",
            options=["Standard", "Detailed", "Comprehensive"],
            value="Comprehensive",
            label_visibility="collapsed"
        )
    
    # Map depth selection to number of chunks
    depth_to_chunks = {
        "Standard": min(len(chunks), 20),
        "Detailed": min(len(chunks), 35),
        "Comprehensive": min(len(chunks), 50)
    }
    selected_chunk_count = depth_to_chunks[summary_depth]
    
    if st.button("🚀 Generate Detailed Summary", type="primary"):
        try:
            with st.spinner("Generating detailed summary from entire document..."):
                st.info("Processing the entire document to create a comprehensive summary. This may take a moment for large documents.")
                # Use many more chunks for a comprehensive detailed summary
                # For detailed summary, use as many chunks as possible to cover the whole document
                chunk_count = selected_chunk_count  # Use the chunk count based on selected summary depth
                detailed_query = "Provide a comprehensive and detailed summary of this document covering all key sections, main points, methodologies, findings, and conclusions."
                detailed_retrieved = embed_manager.search(detailed_query, n_results=chunk_count)
                detailed_chunks = [item['text'] for item in detailed_retrieved]
                
                # Try to identify important sections for better coverage
                # Common section headings in academic and technical documents
                section_keywords = [
                    "abstract", "introduction", "background", "literature review",
                    "methodology", "methods", "experiment", "implementation",
                    "results", "findings", "discussion", "analysis",
                    "conclusion", "future work", "references"
                ]
                
                # Search for chunks that might contain these important sections
                section_chunks = []
                for keyword in section_keywords:
                    section_query = f"Find sections about {keyword}"
                    section_results = embed_manager.search(section_query, n_results=2)
                    section_chunks.extend([item['text'] for item in section_results])
                
                # Combine regular detailed chunks with section-specific chunks
                # Remove duplicates while preserving order
                all_chunks = []
                seen = set()
                for chunk in detailed_chunks + section_chunks:
                    if chunk not in seen:
                        all_chunks.append(chunk)
                        seen.add(chunk)
                
                # Generate detailed summary using the enhanced chunk collection
                detailed_summary = summarizer.generate_summary(all_chunks, prompt=detailed_query)
                  # Display detailed summary
                st.subheader("📄 Detailed Document Summary")
                st.markdown("---")
                
                # Use Streamlit's built-in styling for better readability
                st.markdown("### 📝 Summary Content")
                with st.container():
                    st.markdown(
                        f"""
                        <div style='
                            background-color: #ffffff; 
                            color: #000000; 
                            padding: 25px; 
                            border-radius: 12px; 
                            border: 2px solid #007bff; 
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            line-height: 1.6;
                            font-size: 16px;
                        '>
                            {detailed_summary}
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                st.markdown("---")
                
                # Display token usage statistics
                total_tokens_used = sum(count_tokens(chunk) for chunk in all_chunks)
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Chunks Used", len(all_chunks))
                with col2:
                    st.metric("Tokens Used", total_tokens_used)
                with col3:
                    st.metric("Summary Depth", summary_depth)
                
                # Add buttons for saving and downloading
                col1, col2 = st.columns(2)
                
                with col1:
                    # Save detailed summary to file
                    if st.button("💾 Save Detailed Summary"):
                        try:
                            os.makedirs("summaries", exist_ok=True)
                            detailed_summary_path = os.path.join("summaries", f"{os.path.splitext(uploaded_file.name)[0]}_detailed_summary.txt")
                            with open(detailed_summary_path, "w", encoding="utf-8") as f:
                                f.write(f"Detailed Summary of: {uploaded_file.name}\n")
                                f.write(f"Summary Depth: {summary_depth}\n")
                                f.write(f"Generated on: {st.session_state.get('current_time', 'Unknown')}\n")
                                f.write("=" * 60 + "\n\n")
                                f.write(detailed_summary)
                            st.success(f"✅ Detailed summary saved to: {detailed_summary_path}")
                        except Exception as e:
                            st.error(f"❌ Error saving detailed summary: {str(e)}")
                
                with col2:
                    # Download detailed summary
                    summary_download = f"""# Detailed Summary of {uploaded_file.name}

Summary Depth: {summary_depth}
Chunks Used: {len(all_chunks)}
Tokens Used: {total_tokens_used}

{detailed_summary}"""
                    st.download_button(
                        label="📥 Download Detailed Summary",
                        data=summary_download,
                        file_name=f"{os.path.splitext(uploaded_file.name)[0]}_detailed_summary.md",
                        mime="text/markdown"
                    )
                
                # For PDF files, offer page-by-page summaries
                if file_extension == '.pdf':
                    with st.expander("📖 Page-by-Page Summary"):
                        st.write("Summaries of individual pages in the document:")
                        
                        # Re-read the PDF to get page-specific content
                        try:
                            import PyPDF2
                            with open(tmp_file_path, 'rb') as f:
                                pdf_reader = PyPDF2.PdfReader(f)
                                for page_num, page in enumerate(pdf_reader.pages):
                                    page_text = page.extract_text()
                                    if len(page_text.strip()) > 100:  # Only summarize non-empty pages
                                        page_summary = summarizer.generate_summary([page_text], 
                                                                                  prompt=f"Summarize page {page_num+1} of this document.")
                                        st.markdown(f"**📄 Page {page_num+1}**")
                                        st.write(page_summary)
                                        st.write("---")
                        except Exception as e:
                            st.error(f"Could not generate page-by-page summaries: {str(e)}")
                
                # Show sections breakdown
                st.subheader("🔍 Document Structure Analysis")
                
                # Extract potential sections from the document
                lines = content.split('\n')
                potential_sections = []
                section_content = {}
                
                for i, line in enumerate(lines):
                    line = line.strip()
                    # More comprehensive detection of section headings
                    if (len(line) > 5 and len(line) < 100 and 
                        (line.isupper() or 
                         "section" in line.lower() or 
                         "chapter" in line.lower() or
                         any(keyword in line.lower() for keyword in ["abstract", "introduction", "background", 
                                                                  "methodology", "methods", "results", 
                                                                  "discussion", "conclusion", "references"]))):
                        potential_sections.append(line)
                        # Try to get a preview of the section content (next few lines)
                        preview_lines = []
                        for j in range(i+1, min(i+6, len(lines))):  # Get up to 5 lines of preview
                            if lines[j].strip() and len(lines[j].strip()) > 10:  # Skip empty or very short lines
                                preview_lines.append(lines[j].strip())
                        if preview_lines:
                            section_content[line] = " ".join(preview_lines)[:200] + "..."  # Limit preview length
                
                if potential_sections:
                    st.write("**📋 Document Structure Analysis:**")
                    for i, section in enumerate(potential_sections[:15]):  # Show up to 15 sections
                        st.markdown(f"**{i+1}. {section}**")
                        if section in section_content:
                            st.markdown(f"*Preview:* {section_content[section]}")
                        st.write("---")
                else:
                    st.write("No clear section structure detected in this document.")
                    
                # Show detailed chunks used for transparency
                with st.expander("🔍 View All Retrieved Chunks for Detailed Summary"):
                    st.markdown("*These are all the document chunks used to generate the detailed summary:*")
                    for i, chunk in enumerate(all_chunks):
                        st.markdown(f"**Chunk {i+1}** ({len(chunk)} characters)")
                        st.text_area(f"Content", chunk, height=150, key=f"detailed_chunk_{i}")
                        st.markdown("---")
                        
        except Exception as e:
            st.error(f"An error occurred while generating the detailed summary: {str(e)}")
            st.info("Try processing a smaller document or reducing the chunk size in the settings.")
      # Clean up temporary file
    os.unlink(tmp_file_path)

    # Add a button to save the basic summary
    if st.button("💾 Save Basic Summary"):
        try:
            # Ensure the summaries directory exists
            os.makedirs("summaries", exist_ok=True)
            
            # Define the file path for saving the summary
            summary_file_path = os.path.join("summaries", f"{os.path.splitext(uploaded_file.name)[0]}_summary.txt")
            
            # Write the summary to the file
            with open(summary_file_path, "w", encoding="utf-8") as summary_file:
                summary_file.write(f"Basic Summary of: {uploaded_file.name}\n")
                summary_file.write("=" * 50 + "\n\n")
                summary_file.write(summary)
            
            st.success(f"✅ Basic summary saved successfully to: {summary_file_path}")
        except Exception as e:
            st.error(f"❌ An error occurred while saving the summary: {str(e)}")

# Add helpful information when no file is uploaded
else:
    st.markdown("---")
    st.subheader("🚀 Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📄 Basic Summary:**
        - Quick overview of main points
        - Uses top 5 most relevant chunks
        - Fast generation
        - Perfect for quick understanding
        """)
    
    with col2:
        st.markdown("""
        **📋 Detailed Summary:**
        - Comprehensive analysis
        - Configurable depth (Standard/Detailed/Comprehensive)
        - Section-aware processing
        - Page-by-page analysis for PDFs
        """)
    
    st.markdown("---")
    st.subheader("📖 How it works")
    st.markdown("""
    1. **📤 Upload** your PDF, TXT, or MD document
    2. **⚙️ Processing** - Document is chunked and embedded
    3. **📝 Basic Summary** - Generated automatically using RAG
    4. **📋 Detailed Summary** - Click the button for comprehensive analysis
    5. **💾 Save** - Save summaries to local files
    6. **🔍 Transparency** - View all chunks used for generation
    """)
    
    st.markdown("---")
    st.markdown("*Built with Streamlit, ChromaDB, and SentenceTransformers*")
