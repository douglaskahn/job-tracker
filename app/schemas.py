from pydantic import BaseModel, field_validator, Field
from typing import Optional
from datetime import datetime, date

def normalize_date(date_str: str) -> str:
    try:
        # Try parsing MM/DD/YYYY format
        return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
    except ValueError:
        try:
            # Try parsing YYYY-MM-DD format
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}")

class ApplicationCreate(BaseModel):
    company: str = Field(..., example="Example Company")
    role: str = Field(..., example="Software Engineer")
    url: Optional[str] = Field(None, example="https://example.com/job")
    status: str = Field(..., example="Applied")
    application_date: Optional[date] = Field(None, example="2025-06-17")
    met_with: Optional[str] = Field(None, example="John Doe")
    notes: Optional[str] = Field(None, example="Followed up via email")
    resume_file: Optional[str] = Field(None, example="resume.pdf")
    cover_letter_file: Optional[str] = Field(None, example="cover_letter.docx")
    order_number: Optional[int] = Field(None, example=1)
    follow_up_required: Optional[bool] = Field(False, example=True)
    pros: Optional[str] = Field(None, example="Great company culture")
    cons: Optional[str] = Field(None, example="Long commute")
    salary: Optional[str] = Field(None, example="100000")

    class Config:
        from_attributes = True

class ApplicationUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    url: Optional[str] = None
    status: Optional[str] = None
    application_date: Optional[str] = None
    met_with: Optional[str] = None
    notes: Optional[str] = None
    resume_file: Optional[str] = None
    cover_letter_file: Optional[str] = None
    order_number: Optional[int] = None
    follow_up_required: Optional[bool] = None
    pros: Optional[str] = None
    cons: Optional[str] = None
    salary: Optional[str] = None

    class Config:
        from_attributes = True

class ApplicationMetadata(BaseModel):
    met_with: Optional[str] = None
    notes: Optional[str] = None
    follow_up_required: Optional[bool] = False
    pros: Optional[str] = None
    cons: Optional[str] = None
    salary: Optional[str] = None

    class Config:
        from_attributes = True

class Application(ApplicationCreate):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
