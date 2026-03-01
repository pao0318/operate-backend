from pydantic import BaseModel
from typing import Any, Dict, List


class DatasimulatorBenefitsResponse(BaseModel):
    case_id: int
    offerings: List[Any] = []
    speed: Dict[str, Any] = {}
    accuracy: Dict[str, Any] = {}
    compliance: Dict[str, Any] = {}
    
    class Config:
        orm_mode = True
