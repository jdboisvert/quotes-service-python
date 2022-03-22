from typing import Optional

from pydantic import BaseModel


class QuoteCreateRequest(BaseModel):
    quote: str
    author_name: str


class QuoteUpdateRequest(BaseModel):
    quote: Optional[str] = None
    author_name: Optional[str] = None
