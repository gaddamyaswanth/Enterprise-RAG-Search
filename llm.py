import requests


def generate_answer(question, context):


    prompt = f"""
You are an enterprise document assistant.

Answer the user's question using ONLY the provided company documents.

Rules:
- Do not make up information.
- If the document contains the answer, explain clearly.
- If the information is missing, say that it is not available.
- If conditions exist, mention them.


Company Documents:

{context}


User Question:

{question}


Answer:
"""


    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }
    )


    result = response.json()


    return result["response"]