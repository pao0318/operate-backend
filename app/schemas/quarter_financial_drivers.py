from pydantic import BaseModel
from typing import Any, List


class QuarterFinancialDriversResponse(BaseModel):
    case_id: int
    data_points: List[Any] = []
    
    class Config:
        orm_mode = True
