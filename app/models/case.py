from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Case(Base):
    __tablename__ = "cases"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    case_no = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    applied_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    documents = relationship("Document", back_populates="case", cascade="all, delete-orphan")
    schedule_template_data_points = relationship("FRY14ScheduleTemplateDataPoint", back_populates="case", cascade="all, delete-orphan")
    shipment_details = relationship("ShipmentDetail", back_populates="case", cascade="all, delete-orphan")
    detailed_findings_operational = relationship("DetailedFindingsOperational", back_populates="case", cascade="all, delete-orphan")
    extracted_key_metrics = relationship("ExtractedKeyMetrics", back_populates="case", uselist=False, cascade="all, delete-orphan")
    covenant_status = relationship("CovenantStatus", back_populates="case", uselist=False, cascade="all, delete-orphan")
    quarterly_dscr = relationship("QuarterlyDSCR", back_populates="case", uselist=False, cascade="all, delete-orphan")
    quarter_financial_drivers = relationship("QuarterByQuarterFinancialDrivers", back_populates="case", uselist=False, cascade="all, delete-orphan")
    q3_highlight = relationship("Q3Highlight", back_populates="case", uselist=False, cascade="all, delete-orphan")
    detailed_findings_y14 = relationship("DetailedFindingsY14", back_populates="case", uselist=False, cascade="all, delete-orphan")
    datasimulator_benefits = relationship("DatasimulatorBenefits", back_populates="case", uselist=False, cascade="all, delete-orphan")
