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

# utils/openai_handler.py

# import os
# import openai
# from dotenv import load_dotenv

# load_dotenv()

# from langchain.chat_models import ChatOpenAI
# from langchain.schema import SystemMessage, HumanMessage
# from utils.usage_tracker import log_usage

# def call_openai_model(purpose: str, prompt: str, model="gpt-4-turbo", user_id="internal-user"):
#     try:
#         response = openai.ChatCompletion.create(
#             model=model,
#             messages=[
#                 {"role": "system", "content": "You are a helpful AI assistant."},
#                 {"role": "user", "content": prompt}
#             ]
#         )

#         # ✅ Token usage logging
#         tokens_input = response['usage']['prompt_tokens']
#         tokens_output = response['usage']['completion_tokens']
#         cost = (tokens_input * 0.01 + tokens_output * 0.03) / 1000

#         log_usage(
#             user_id=user_id,
#             model=model,
#             tokens_input=tokens_input,
#             tokens_output=tokens_output,
#             cost=cost
#         )

#         return response['choices'][0]['message']['content']
#     except Exception as e:
#         raise RuntimeError(f"LLM call failed: {str(e)}")


