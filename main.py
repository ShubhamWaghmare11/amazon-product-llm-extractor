# main.py
import os
import json
from dotenv import load_dotenv
import requests

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from parser import extract_amazon_sections, extract_text_for_llm
from schema import Product
from url_cleaner import clean_amazon_url


load_dotenv()

def fetch_html(url: str) -> str:
    """Download HTML from a given product URL."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.text


def build_chain():
    """Build LangChain model with strict Pydantic schema."""
    base_model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    # Force structured Pydantic output
    structured_model = base_model.with_structured_output(Product)

    # Minimal prompt (no formatting instructions needed)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract structured product data from the provided text."),
        ("user", "Extract structured product details:\n\n{text}")
    ])

    # LCEL pipeline
    chain = prompt | structured_model
    return chain

def extract_from_url(url: str, out_file="product.json"):
    url = clean_amazon_url(url)

    html = fetch_html(url)
    sections = extract_amazon_sections(html)
    text = extract_text_for_llm(sections)

    chain = build_chain()
    result: Product = chain.invoke({"text": text})

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result.model_dump(), f, indent=2)

    return result



if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python main.py <amazon_url>")
        exit(1)

    url = sys.argv[1]
    product = extract_from_url(url)
    print(product)
