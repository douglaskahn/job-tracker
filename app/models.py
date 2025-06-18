from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    location = Column(String, index=True)
    # Add other fields as necessary

class JobApplication(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    url = Column(String)
    status = Column(String, nullable=False)
    application_date = Column(String)
    met_with = Column(String)
    notes = Column(String)
    resume_file = Column(String)
    cover_letter_file = Column(String)
    order_number = Column(Integer)
    follow_up_required = Column(Boolean, default=False)
    pros = Column(String)
    cons = Column(String)
    salary = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
