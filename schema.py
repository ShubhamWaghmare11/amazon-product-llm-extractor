from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class Product(BaseModel):
    title: Optional[str] = None
    asin: Optional[str] = None
    brand: Optional[str] = None

    price: Optional[int] = Field(default=None, gt=0)
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    review_count: Optional[int] = None

    description: Optional[str] = None
    bullets: Optional[List[str]] = None
    specs: Optional[Dict[str, str]] = None
    tags: Optional[List[str]] = None
    search_filters: Optional[Dict[str, List[str]]] = None


