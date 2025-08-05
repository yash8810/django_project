
import faiss
import numpy as np
import os
import json
from sentence_transformers import SentenceTransformer

# Paths (adjust if necessary)
data_folder = os.path.join(os.path.dirname(__file__), "regdata")
faiss_index_path = os.path.join(data_folder, "rag_data_index.faiss")
metadata_path = os.path.join(data_folder, "chunk_metadata.json")

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
if not os.path.exists(faiss_index_path):
    raise FileNotFoundError("FAISS index file not found.")
index = faiss.read_index(faiss_index_path)

# Load chunk metadata
with open(metadata_path, "r", encoding="utf-8") as f:
    chunk_metadata = json.load(f)

def retrieve_similar(query, top_k=3):
    """Retrieve top_k most relevant text chunks for the given query."""
    try:
        # Embed the query
        query_vector = embedding_model.encode([query])
        
        # Search FAISS index
        D, I = index.search(np.array(query_vector, dtype=np.float32), top_k)

        # Fetch matched texts
        retrieved_texts = []
        for idx in I[0]:
            if 0 <= idx < len(chunk_metadata):
                retrieved_texts.append(chunk_metadata[idx]["text"])

        return "\n\n".join(retrieved_texts)

    except Exception as e:
        print("❌ Error in retrieve_similar:", str(e))
        return ""

















# import faiss
# import json
# import numpy as np
# import os

# from sentence_transformers import SentenceTransformer

# # Paths
# base_dir = os.path.dirname(__file__)
# data_dir = os.path.join(base_dir, "regdata")

# # Load model & FAISS index
# model = SentenceTransformer("all-MiniLM-L6-v2")


# # Load FAISS index
# if not os.path.exists(os.path.join(data_dir, "rag_data_index.faiss")):
#     raise FileNotFoundError("FAISS index file not found. Please check the path.")

# index = faiss.read_index(os.path.join(data_dir, "rag_data_index.faiss"))

# # Load metadata
# with open(os.path.join(data_dir, "chunk_metadata.json"), "r", encoding="utf-8") as f:
#     metadata = json.load(f)

# # Load JSON files (assuming your JSON files are structured with "content" as a key or something similar)
# def load_json_data(file_name):
#     file_path = os.path.join(data_dir, file_name)
#     with open(file_path, "r", encoding="utf-8") as f:
#         return json.load(f)

# # Example JSON structure for each file (this will depend on your actual data format)
# # dietplan.json, recipes.json, workoutplan.json

# dietplan_data = load_json_data("dietplan.json")
# recipes_data = load_json_data("recipes.json")
# workoutplan_data = load_json_data("workoutplan_data.json")

# # Combine data into a list of documents (or chunks) for FAISS
# documents = []

# # Assuming JSON objects have a structure like this:
# # [{'title': 'recipe 1', 'ingredients': '...', 'instructions': '...'}, ...]

# def extract_text_from_json(data):
#     text_data = []
#     for item in data:
#         # Assuming 'title', 'ingredients', and 'instructions' are keys in the JSON files
#         text = ""
#         if "title" in item:
#             text += f"Title: {item['title']}\n"
#         if "ingredients" in item:
#             text += f"Ingredients: {item['ingredients']}\n"
#         if "instructions" in item:
#             text += f"Instructions: {item['instructions']}\n"
#         text_data.append(text)
#     return text_data

# # Collect text from all JSON data sources
# documents.extend(extract_text_from_json(dietplan_data))
# documents.extend(extract_text_from_json(recipes_data))
# documents.extend(extract_text_from_json(workoutplan_data))

# # Split documents into smaller chunks (if needed)
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
# chunks = []
# chunk_metadata = []

# for i, doc in enumerate(documents):
#     split_chunks = text_splitter.split_text(doc)
#     chunks.extend(split_chunks)
#     chunk_metadata.extend([{"doc_index": i, "source": f"chunk_{i}", "text": chunk} for chunk in split_chunks])


# print(f"Total chunks created: {len(chunks)}")
# print(f"Total metadata entries: {len(chunk_metadata)}")
# print(f"First chunk: {chunks[0]}")

# # Save chunk metadata for retrieval (if needed)
# with open(os.path.join(data_dir, "chunk_metadata.json"), "w", encoding="utf-8") as f:
#     json.dump(chunk_metadata, f, indent=4)

# # Convert text chunks into embeddings
# embeddings = model.encode(chunks)

# print(f"Embeddings shape: {np.array(embeddings).shape}")


# # Store embeddings in FAISS (if needed)
# dimension = embeddings.shape[1]
# index = faiss.IndexFlatL2(dimension)
# index.add(np.array(embeddings, dtype=np.float32))

# # Save the FAISS index
# faiss.write_index(index, os.path.join(data_dir, "rag_data_index.faiss"))

# # Retrieve top-k similar chunks based on query
# def retrieve_similar(query, top_k=5):
#     query_embedding = model.encode([query])
#     distances, indices = index.search(np.array(query_embedding, dtype=np.float32), top_k)

#     results = []
#     for i in indices[0]:
#         if i < len(metadata):
#             results.append(metadata[i]["text"])
#     return "\n\n".join(results)

# if __name__ == "__main__":
#     q = "What should I eat for muscle gain lunch?"
#     print(retrieve_similar(q))
