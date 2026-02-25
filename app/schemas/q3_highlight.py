from pydantic import BaseModel
from typing import List, Optional


class Q3HighlightResponse(BaseModel):
    case_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    datalines: List[str] = []
    
    class Config:
        from_attributes = True
