from pydantic import BaseModel
from typing import Any, Dict, List


class DetailedFindingsOperationalResponse(BaseModel):
    case_id: int
    findings: List[Dict[str, Any]] = []
    
    class Config:
        from_attributes = True
