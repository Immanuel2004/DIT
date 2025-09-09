# # utils/groq_handler.py
import os
from groq import Groq
from langchain_community.llms import Ollama

def call_ollama_model(prompt):
    llm = Ollama(model="llama3")
    return llm.invoke(prompt)

def call_groq_model(system_prompt, user_prompt):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt.strip()}
            ],
            temperature=0.4,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Groq API error: {e}")