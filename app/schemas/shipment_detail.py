from pydantic import BaseModel
from typing import Optional
from datetime import date


class ShipmentDetailResponse(BaseModel):
    id: int
    name: str
    promised_delivery_date: Optional[date] = None
    actual_delivery_date: Optional[date] = None
    
    class Config:
        orm_mode = True
