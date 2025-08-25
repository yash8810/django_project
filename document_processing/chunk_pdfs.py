import os
import json
import faiss
import numpy as np
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# Paths
base_path = os.path.dirname(__file__)
pdf_folder = 'Y:/YBAI/Document_AI/document_intelligence/document_processing/pdfs'
vector_folder = 'Y:/YBAI/Document_AI/document_intelligence/document_processing/vector_store'

print("📂 PDF Folder:", pdf_folder)
print("📁 Vector Store Folder:", vector_folder)
os.makedirs(vector_folder, exist_ok=True)

# Initialization
chunks = []
chunk_metadata = []
documents = []

# Function to process a new document
def process_new_document(pdf_path, doc_id):
    reader = PdfReader(pdf_path)

    chunks = []
    chunk_metadata = []

    # Split and track per page
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    for page_num, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        if not page_text.strip():
            continue

        page_chunks = splitter.split_text(page_text)
        chunks.extend(page_chunks)

        for chunk in page_chunks:
            chunk_metadata.append({
                "doc_id": doc_id,
                "text": chunk,
                "page": page_num
            })

    # Embed
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks).astype(np.float32)

    # FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return chunk_metadata, faiss.serialize_index(index) 

# If you want to process a directory of PDFs, uncomment the following code:
# for filename in os.listdir(pdf_folder):
#     if filename.endswith(".pdf"):
#         process_new_document(os.path.join(pdf_folder, filename))
