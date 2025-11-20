import re
from urllib.parse import urlparse

def clean_amazon_url(url: str) -> str:
    url = url.strip()

    # If "/dp/" not in URL → invalid product link
    if "/dp/" not in url:
        raise ValueError("Invalid Amazon product link (missing /dp/).")

    # Split and extract ASIN
    asin_part = url.split("/dp/")[1]     # everything after dp/
    asin = asin_part.split("/")[0]       # cut after first slash or ?
    asin = asin.split("?")[0]            # cut query params
    asin = asin.split("&")[0]            # cut extra params

    # Validate ASIN length
    if len(asin) != 10:
        raise ValueError(f"Invalid ASIN extracted: {asin}")

    # Determine domain
    from urllib.parse import urlparse
    domain = urlparse(url).netloc.lower()

    if "amazon." not in domain:
        domain = "www.amazon.in"

    # Return canonical URL
    return f"https://{domain}/dp/{asin}"
