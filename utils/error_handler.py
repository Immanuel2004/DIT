
def safe_llm_call(func, *args, default=None, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"[LLM ERROR] {e}")  # or use logging
        return default if default is not None else {"response": "An error occurred."}
