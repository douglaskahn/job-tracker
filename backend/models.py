from sqlalchemy import Column, Integer, String, Boolean, Date
from backend.database import Base

class JobApplication(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    status = Column(String, nullable=False)
    application_date = Column(Date, nullable=True)
    met_with = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    follow_up_required = Column(Boolean, default=False)
    pros = Column(String, nullable=True)
    cons = Column(String, nullable=True)
    salary = Column(String, nullable=True)