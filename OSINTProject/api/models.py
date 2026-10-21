from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    subject_name: str
    location: str
    occupation: Optional[str] = None
    associates: Optional[List[str]] = None
    interests: Optional[List[str]] = None