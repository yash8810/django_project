from llama_cpp import Llama
from . import retriever

# Load local GGUF model (set the actual path)
llm = Llama(
    model_path="D:\\gymer\\intern_model.gguf",  # 👈 UPDATE this to your actual .gguf file path
    n_ctx=2048,
    n_gpu_layers=20,  # adjust based on your GPU (1650 Ti can handle ~20-30 layers)
    n_threads=8,
    verbose=True
)

def generate_response(user_query, user_data=None):
    """Generate a short and accurate LLM response based on retrieved data and optional user data."""
    retrieved_context = retriever.retrieve_similar(user_query, top_k=3)

    if not retrieved_context.strip():
        print("⚠️ Warning: Retrieved context is empty!")

    user_info = "" if not user_data else "\n".join(
        [f"{key}: {value}" for key, value in user_data.items() if value]
    )

    prompt = f"""
You are a helpful and professional marketing assistant.
Keep the response short, accurate, and helpful (2-4 sentences max). Avoid repetition and extra explanation.
---
User Query: {user_query}

User Data:
{user_info}

Retrieved Context:
{retrieved_context}
"""

    result = llm(
        prompt=prompt.strip(),
        max_tokens=200,
        temperature=0.3,
        top_p=0.8
    )

    return result["choices"][0]["text"].strip()

# For testing
if __name__ == "__main__":
    query = "What is internet marketing success?"
    user_data = {"business_type": "e-commerce", "experience_level": "beginner"}
    response = generate_response(query, user_data)
    print(f"\nResponse: {response}")
