# utils.py
import re
import json

def extract_json_like(text: str) -> str:
    """
    Try to find the first JSON object inside text.
    Returns JSON string or raises ValueError.
    """
    # find first { ... } balanced braces (simple approach using stack)
    start = None
    stack = []
    for i, ch in enumerate(text):
        if ch == "{":
            if start is None:
                start = i
            stack.append("{")
        elif ch == "}":
            if stack:
                stack.pop()
                if not stack and start is not None:
                    candidate = text[start:i+1]
                    # quick validity test
                    try:
                        json.loads(candidate)
                        return candidate
                    except:
                        # continue search
                        start = None
    # fallback: try regex for a big {...}
    m = re.search(r"(\{(?:.|\n){10,}\})", text)
    if m:
        cand = m.group(1)
        try:
            json.loads(cand)
            return cand
        except:
            pass
    raise ValueError("No valid JSON object found in model output.")
