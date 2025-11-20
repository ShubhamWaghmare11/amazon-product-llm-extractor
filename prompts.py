# prompts.py
JSON_SCHEMA = {
    "title": "",
    "asin": "",
    "brand": "",
    "price": "",
    "rating": "",
    "review_count": "",
    "description": "",
    "bullets": [],
    "specs": {},             # arbitrary key: value specs
    "tags": [],              # LLM generated short tags
    "search_filters": {}     # structured filters like {"color": ["black"], "size":["M","L"]}
}

PROMPT = """
You are a strict extractor. Given the following product page content, extract the product information
and return ONLY a JSON object that follows the schema exactly. Do NOT include any explanation or extra text.

Schema example:
{
  "title": "",
  "asin": "",
  "brand": "",
  "price": "",
  "rating": "",
  "review_count": "",
  "description": "",
  "bullets": [],
  "specs": {},
  "tags": [],
  "search_filters": {}
}

Content:
{text}

RULES:
1) Output valid JSON only. No markdown, no backticks.
2) For fields you cannot find, return empty string (for text) or empty list/dict for collections.
3) tags: produce 5 concise tags (single words or short phrases).
4) search_filters: for common attributes (color, size, material, capacity, dimensions), map them to arrays of normalized values if found.
5) specs: include any explicit technical specs from the page (key: value).
6) Keep price in the original currency string if present (e.g., "₹3,499" or "$49.99").
7) If multiple values exist (sizes or colors), return comma-separated strings in the arrays.
8) Be conservative and consistent.

Return only JSON now.
"""
