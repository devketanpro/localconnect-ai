# app/schemas.py
from pydantic import BaseModel

class SearchQuery(BaseModel):
    query: str
