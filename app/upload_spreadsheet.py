import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import JobApplication
from datetime import datetime
from pydantic import field_validator

@field_validator("application_date", mode="before")
def parse_application_date(cls, value):
    if isinstance(value, str):
        try:
            # Try parsing MM/DD/YYYY format
            return datetime.strptime(value, "%m/%d/%Y").date()
        except ValueError:
            try:
                # Try parsing YYYY-MM-DD format
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(f"Invalid date format: {value}")
    return value  # Let Pydantic handle other formats

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

def upload_spreadsheet(file_path: str, sheet_name: str = "Sheet1"):
    # Read the spreadsheet into a DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Map DataFrame rows to database model
    applications = [
        JobApplication(
            order_number=row['Order number'],
            company=row['Company'],
            role=row['Role'],
            url=row['URL'],
            status=row['Status'],
            application_date=normalize_date(row['Application Date']) if row['Application Date'] else None,
            met_with=row['Met with'],
            notes=row['Notes'],
            resume_file=row['Resume Link'],  # Blank values will be stored as None
            cover_letter_file=row['Cover Letter Link'],  # Blank values will be stored as None
            follow_up_required=False,  # Default value
            pros=None,  # Default value
            cons=None,  # Default value
            salary=None,  # Default value
        )
        for _, row in df.iterrows()
    ]

    # Insert into the database
    with SessionLocal() as session:
        session: Session
        session.add_all(applications)
        session.commit()

    print(f"Successfully uploaded {len(applications)} applications.")

if __name__ == "__main__":
    file_path = "datasample/JobApplicationTracker2025.xlsx"  # Replace with your file path
    upload_spreadsheet(file_path)
