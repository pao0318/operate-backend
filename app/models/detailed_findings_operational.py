from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class DetailedFindingsOperational(Base):
    __tablename__ = "detailed_findings_operational"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSONB, nullable=True, default={})
    case_id = Column(Integer, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    case = relationship("Case", back_populates="detailed_findings_operational")
