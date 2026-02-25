from pydantic import BaseModel
from typing import List, Optional


class FRY14DetailResponse(BaseModel):
    id: int
    name: str
    label: Optional[str] = None
    value: Optional[str] = None
    
    class Config:
        from_attributes = True


class FRY14DataPointResponse(BaseModel):
    id: int
    name: str
    label: Optional[str] = None
    details: List[FRY14DetailResponse] = []
    
    class Config:
        from_attributes = True


class FRY14ScheduleTemplateResponse(BaseModel):
    case_id: int
    data_points: List[FRY14DataPointResponse] = []
    
    class Config:
        from_attributes = True
