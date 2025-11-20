## Amazon Product Extractor (LangChain + OpenAI + Pydantic)

This tool extracts structured product information (title, price, rating, bullets, specs, description, etc.) directly from any Amazon product URL. It cleans messy URLs, downloads the HTML, parses product sections using BeautifulSoup, and uses LangChain + OpenAI to generate a validated JSON output following a strict Pydantic schema.

====================
## SETUP
====================

1. Create virtual environment:
python -m venv venv
(Windows) .\venv\Scripts\Activate.ps1
(Mac/Linux) source venv/bin/activate

2. Install dependencies:
pip install -r requirements.txt

3. Add your OpenAI API key to .env:
OPENAI_API_KEY=sk-xxxxxxxxxxxx

====================
## USAGE
====================

Run extraction with any Amazon URL:
python main.py "https://www.amazon.in/dp/B0FQ26LPWN"

Or paste any long messy URL:
python main.py "https://www.amazon.in/Kargeens-Brown-Baggy-Loose-Cargo/dp/B0FQ26LPWN/?_encoding=UTF8&pd_rd_w=..."

Output is saved to:
product.json

====================
## OUTPUT
====================

The script produces a validated JSON file containing the extracted product metadata.
