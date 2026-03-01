from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class FRY14ScheduleTemplateDataPoint(Base):
    __tablename__ = "fr_y14_schedule_template_data_points"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    label = Column(String(255), nullable=True)
    case_id = Column(Integer, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    case = relationship("Case", back_populates="schedule_template_data_points")
    details = relationship("FRY14ScheduleTemplateDataPointDetail", back_populates="data_point", cascade="all, delete-orphan")


class FRY14ScheduleTemplateDataPointDetail(Base):
    __tablename__ = "fr_y14_schedule_template_data_point_details"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    label = Column(String(255), nullable=True)
    value = Column(String(500), nullable=True)
    additional_data = Column(JSONB, nullable=True, default=None)
    template_data_point_id = Column(Integer, ForeignKey("fr_y14_schedule_template_data_points.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    data_point = relationship("FRY14ScheduleTemplateDataPoint", back_populates="details")
