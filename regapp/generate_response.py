from . import retriever
from groq import Groq
import os

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

    # Call Groq LLM
    result = client.chat.completions.create(
        model="llama3-8b-8192",  # You can change this to other Groq-supported models
        messages=[
            {"role": "system", "content": "You are a helpful and professional marketing assistant."},
            {"role": "user", "content": prompt.strip()}
        ],
        max_tokens=200,
        temperature=0.3,
        top_p=0.8
    )

    return result.choices[0].message.content.strip()

# For testing
if __name__ == "__main__":
    query = "What is internet marketing success?"
    user_data = {"business_type": "e-commerce", "experience_level": "beginner"}
    response = generate_response(query, user_data)
    print(f"\nResponse: {response}")
