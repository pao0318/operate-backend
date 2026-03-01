from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class DetailedFindingsY14Response(BaseModel):
    case_id: int
    warning_message: Optional[str] = None
    detailed_findings: List[Any] = []
    
    class Config:
        orm_mode = True
