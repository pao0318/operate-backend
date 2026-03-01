from pydantic import BaseModel, Field
from typing import Optional


class DocumentBase(BaseModel):
    name: str = Field(..., max_length=255)
    url: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = Field(None, max_length=1000)
    type: Optional[str] = Field(None, max_length=100)
    filename: Optional[str] = Field(None, max_length=255)


class DocumentCreate(DocumentBase):
    case_id: int


class DocumentResponse(BaseModel):
    id: int
    name: str
    url: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    filename: Optional[str] = None
    
    class Config:
        orm_mode = True
