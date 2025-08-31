import re
import json

def extract_json_list(text):
    """
    Tries to extract a JSON list from messy or partially valid LLM output.
    """
    try:
        return json.loads(text)
    except Exception:
        pass

    try:
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            json_str = match.group()
            return json.loads(json_str)
    except Exception:
        pass

    raise ValueError(f"Failed to extract JSON list: {text}")
