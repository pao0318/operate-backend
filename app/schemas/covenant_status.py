from pydantic import BaseModel
from typing import Optional


class CovenantStatusResponse(BaseModel):
    case_id: int
    name: Optional[str] = None
    label: Optional[str] = None
    value: Optional[str] = None
    indicator: Optional[str] = None
    status: Optional[str] = None
    
    class Config:
        orm_mode = True
