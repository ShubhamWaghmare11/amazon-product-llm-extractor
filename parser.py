# parser.py
from bs4 import BeautifulSoup
from typing import Tuple, Dict, List, Optional
import re

def load_html(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_amazon_sections(html: str) -> Dict:
    soup = BeautifulSoup(html, "html.parser")

    # Title
    title_tag = soup.find(id="productTitle") or soup.find("span", {"class": re.compile("title")})
    title = title_tag.get_text(strip=True) if title_tag else ""

    # Price (multiple possible selectors)
    price = ""
    for sel in ["#priceblock_ourprice", "#priceblock_dealprice", ".a-price .a-offscreen"]:
        tag = soup.select_one(sel)
        if tag and tag.get_text(strip=True):
            price = tag.get_text(strip=True)
            break

    # ASIN try from DOM or meta
    asin = ""
    asin_tag = soup.find("th", string=re.compile("ASIN", re.I))
    if asin_tag:
        td = asin_tag.find_next_sibling("td")
        if td:
            asin = td.get_text(strip=True)
    if not asin:
        # fallback: search in page text
        m = re.search(r"ASIN[:\s]*([A-Z0-9]{10})", html)
        if m:
            asin = m.group(1)

    # Brand
    brand = ""
    brand_tag = soup.find(id="bylineInfo") or soup.find("a", {"id": "brand"} )
    if brand_tag:
        brand = brand_tag.get_text(strip=True)

    # Bullets (features)
    bullets = []
    bullets_ul = soup.find(id="feature-bullets") or soup.select_one("#feature-bullets ul")
    if bullets_ul:
        for li in bullets_ul.find_all("li"):
            txt = li.get_text(" ", strip=True)
            if txt:
                bullets.append(txt)

    # Description
    desc = ""
    desc_tag = soup.find(id="productDescription")
    if desc_tag:
        desc = desc_tag.get_text(" ", strip=True)
    # If description empty, try feature bullets joined
    if not desc and bullets:
        desc = " ".join(bullets[:4])

    # Rating and review count
    rating = ""
    review_count = ""
    rtag = soup.select_one("span#acrPopover") or soup.select_one("span.a-icon-alt")
    if rtag:
        rating = rtag.get_text(strip=True)
    rc = soup.select_one("#acrCustomerReviewText") or soup.select_one("#acrCustomerReviewLink")
    if rc:
        review_count = rc.get_text(strip=True)

    # Technical details / Product details table
    specs = {}
    # Try common tables
    for table_id in ["productDetails_techSpec_section_1", "productDetails_detailBullets_sections1"]:
        t = soup.find(id=table_id)
        if t:
            for row in t.find_all("tr"):
                th = row.find("th")
                td = row.find("td")
                if th and td:
                    key = th.get_text(" ", strip=True)
                    val = td.get_text(" ", strip=True)
                    specs[key] = val
    # Some pages use detail bullets list
    if not specs:
        detail_block = soup.select_one("#detailBullets_feature_div")
        if detail_block:
            for li in detail_block.select("li"):
                parts = li.get_text(" ", strip=True).split(":")
                if len(parts) >= 2:
                    k = parts[0].strip()
                    v = ":".join(parts[1:]).strip()
                    specs[k] = v

    # Return everything
    return {
        "title": title,
        "price": price,
        "asin": asin,
        "brand": brand,
        "bullets": bullets,
        "description": desc,
        "rating": rating,
        "review_count": review_count,
        "specs": specs,
        "raw_text": soup.get_text(separator="\n")
    }

def extract_text_for_llm(sections: Dict, max_chars: int = 4000) -> str:
    """
    Compose a compact text blob to send to the LLM.
    Keep it concise to reduce cost; include the most relevant fields.
    """
    parts = []
    if sections.get("title"):
        parts.append("TITLE: " + sections["title"])
    if sections.get("brand"):
        parts.append("BRAND: " + sections["brand"])
    if sections.get("price"):
        parts.append("PRICE: " + sections["price"])
    if sections.get("rating"):
        parts.append("RATING: " + sections["rating"])
    if sections.get("review_count"):
        parts.append("REVIEWS: " + sections["review_count"])
    if sections.get("bullets"):
        parts.append("FEATURE BULLETS: " + " | ".join(sections["bullets"][:8]))
    if sections.get("specs"):
        # include key specs (first 12)
        spec_txt = " | ".join([f"{k}:{v}" for k, v in list(sections["specs"].items())[:12]])
        if spec_txt:
            parts.append("SPECS: " + spec_txt)
    if sections.get("description"):
        parts.append("DESCRIPTION: " + sections["description"][:1000])

    blob = "\n\n".join(parts)
    if len(blob) > max_chars:
        return blob[:max_chars]
    return blob
