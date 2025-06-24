from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    location = Column(String, index=True)
    # Add other fields as necessary

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    status = Column(String, nullable=False)
    url = Column(String, nullable=True)
    application_date = Column(Date, nullable=True)
    met_with = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    resume_file = Column(String, nullable=True)
    cover_letter_file = Column(String, nullable=True)
    order_number = Column(Integer, nullable=True)
    follow_up_required = Column(Boolean, default=False)
    pros = Column(String, nullable=True)
    cons = Column(String, nullable=True)
    salary = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    cons = Column(String, nullable=True)
    salary = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Demo models moved to demo_models.py for better isolation
