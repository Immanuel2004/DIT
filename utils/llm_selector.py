from utils.groq_handler import call_groq_model, call_ollama_model

def get_llm(model_source="groq"):
    if model_source == "groq":
        def llm(prompt):
            system_prompt = "You are a helpful data analyst. Provide clear and concise responses."
            return call_groq_model(system_prompt, prompt)
        return llm
    elif model_source == "ollama":
        def llm(prompt):
            return call_ollama_model(prompt)
        return llm
    else:
        raise ValueError(f"Unsupported model source: {model_source}")