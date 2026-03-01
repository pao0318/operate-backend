from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class ExtractedKeyMetricsResponse(BaseModel):
    name: Optional[str] = None
    case_id: int
    info_lines: List[str] = []
    description: Optional[str] = None
    data_points: Dict[str, Any] = {}
    
    class Config:
        orm_mode = True
