import json
import os
import faiss
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# Define the folder containing data files
data_folder = os.path.join(os.path.dirname(__file__), "regdata")

# Initialize lists to store text data and metadata
documents = []
chunk_metadata = []

# List of specific JSON files to process
json_files = [
    "dietplan.json", "recipes.json", "workoutplan_data.json"
]

# Load and prepare documents
for file_name in json_files:
    file_path = os.path.join(data_folder, file_name)

    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_name}")
        continue

    print(f"📄 Processing {file_name}...")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            text = json.dumps(data, ensure_ascii=False)  # avoid escaping unicode
            documents.append(text)
    except Exception as e:
        print(f"⚠️ Error loading {file_name}: {e}")

# Ensure documents were loaded
if not documents:
    print("❌ No documents were processed. Exiting.")
    exit(1)

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = []

for i, doc in enumerate(documents):
    split_chunks = text_splitter.split_text(doc)
    chunks.extend(split_chunks)
    chunk_metadata.extend([
        {"doc_index": i, "source": json_files[i], "text": chunk}
        for chunk in split_chunks
    ])

# Save chunk metadata
metadata_path = os.path.join(data_folder, "chunk_metadata.json")
try:
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(chunk_metadata, f, indent=4, ensure_ascii=False)
    print("✅ Chunk metadata saved successfully!")
except Exception as e:
    print(f"⚠️ Failed to save chunk metadata: {e}")

# Load embedding model and create embeddings
print("🔍 Generating embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")

try:
    embeddings = model.encode(chunks, show_progress_bar=True)
except Exception as e:
    print(f"❌ Error generating embeddings: {e}")
    exit(1)

# Create and save FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

try:
    index.add(np.array(embeddings, dtype=np.float32))
    faiss_path = os.path.join(data_folder, "rag_data_index.faiss")
    faiss.write_index(index, faiss_path)
    print("✅ FAISS index created and saved successfully!")
except Exception as e:
    print(f"❌ Error creating/saving FAISS index: {e}")
