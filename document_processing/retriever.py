# import os
# import json
# import faiss
# import numpy as np
# from sentence_transformers import SentenceTransformer

# base_path = os.path.dirname(__file__)
# model = SentenceTransformer("all-MiniLM-L6-v2")

# index = faiss.read_index(os.path.join(base_path, "vector_store", "faiss_index.faiss"))
# with open(os.path.join(base_path, "vector_store", "chunk_metadata.json"), "r", encoding="utf-8") as f:
#     chunk_metadata = json.load(f)

# def retrieve_similar(query, top_k=3):
#     query_vector = model.encode([query])
#     _, indices = index.search(np.array(query_vector, dtype=np.float32), top_k)
    
#     # Clean up the text by joining words and removing tab characters
#     results = [chunk_metadata[i]["text"] for i in indices[0] if i < len(chunk_metadata)]
#     cleaned_results = [" ".join(result.split("\t")) for result in results]  # Joining words and removing tabs
    
#     return cleaned_results

import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Define paths
BASE_DIR = os.path.dirname(__file__)
INDEX_PATH = os.path.join(BASE_DIR, "vector_store", "faiss_index.faiss")
CHUNK_METADATA_PATH = os.path.join(BASE_DIR, "vector_store", "chunk_metadata.json")

# Load model and FAISS index
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index(INDEX_PATH)

# Load chunk metadata
with open(CHUNK_METADATA_PATH, "r", encoding="utf-8") as f:
    chunk_metadata = json.load(f)

# Search function
def retrieve_similar_chunks(query, top_k=3):
    query_embedding = model.encode([query]).astype(np.float32)
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i in indices[0]:
        if 0 <= i < len(chunk_metadata):
            chunk = chunk_metadata[i]
            page = chunk.get("page", "N/A")
            text = chunk.get("text", "")
            results.append(f"📄 Page {page}:\n{text.strip()}")
    
    return "\n\n---\n\n".join(results)

  