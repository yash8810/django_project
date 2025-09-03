import os
from groq import Groq
from .retriever import retrieve_similar

# Use environment variable (safer than hardcoding the key)
client = Groq(api_key=os.getenv("GROK_API_KEY"))

def generate_response(query):
    context = retrieve_similar(query)
    context_text = "\n\n".join(context)

    prompt = f"""
You are a helpful assistant. Use only the context below to answer.
If unsure, say: "I'm not sure based on the provided info."

---Context---
{context_text}

---Question---
{query}
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",  # valid Groq model
        messages=[
            {"role": "system", "content": "You are an intelligent assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=150,
    )

    return response.choices[0].message.content.strip()

# Optional quick test
if __name__ == "__main__":
    resp = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": "Test"}],
        max_tokens=10
    )
    print(resp.choices[0].message.content)

