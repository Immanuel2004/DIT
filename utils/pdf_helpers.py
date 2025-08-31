def format_chat_for_pdf(chat_history):
    """
    Format chat history into a consistent list for PDF export.
    Ensures 'source' is always present and valid.
    """
    supported_sources = {"openai", "groq", "ollama"}
    formatted = []
    for chat in chat_history:
        role = chat.get("role", "user")
        content = chat.get("content", "")
        source = chat.get("source") or "unknown"

        # Normalize or fallback
        if source not in supported_sources:
            source = "unknown"

        formatted.append({
            "role": role,
            "content": content,
            "source": source
        })
    return formatted
