from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class DemoApplication(Base):
    __tablename__ = "demo_applications"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    status = Column(String, nullable=False)
    url = Column(String, nullable=True)
    application_date = Column(Date, nullable=True)
    met_with = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    pros = Column(String, nullable=True)
    cons = Column(String, nullable=True)
    salary = Column(String, nullable=True)
    follow_up_required = Column(Boolean, default=False)
    resume_file = Column(String, nullable=True)
    cover_letter_file = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    status_change_date = Column(DateTime, nullable=True)
    order_number = Column(Integer, nullable=True)
    
    # Relationship to status history
    status_history = relationship("DemoStatusHistory", back_populates="application")

class DemoStatusHistory(Base):
    __tablename__ = "demo_status_history"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey('demo_applications.id'))
    status = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    
    # Relationship back to application
    application = relationship("DemoApplication", back_populates="status_history")
