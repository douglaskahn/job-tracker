import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Application
from datetime import datetime

def normalize_date(date_str: str):
    if pd.isna(date_str) or not date_str:
        return None
    try:
        return datetime.strptime(str(date_str), "%m/%d/%Y").date()
    except ValueError:
        try:
            return datetime.strptime(str(date_str), "%Y-%m-%d").date()
        except ValueError:
            return None

def upload_spreadsheet(file_path: str, sheet_name: str = "Sheet1"):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    applications = []
    for _, row in df.iterrows():
        app = Application(
            order_number=row.get('Order number'),
            company=row.get('Company'),
            role=row.get('Role'),
            url=row.get('URL'),
            status=row.get('Status'),
            application_date=normalize_date(row.get('Application Date')),
            met_with=row.get('Met with'),
            notes=row.get('Notes'),
            resume_file=row.get('Resume Link'),
            cover_letter_file=row.get('Cover Letter Link'),
            follow_up_required=bool(row.get('Follow Up Required', False)),
            pros=row.get('Pros'),
            cons=row.get('Cons'),
            salary=row.get('Salary'),
        )
        applications.append(app)
    with SessionLocal() as session:
        session: Session
        session.add_all(applications)
        session.commit()
    print(f"Successfully uploaded {len(applications)} applications.")

if __name__ == "__main__":
    file_path = "datasample/JobApplicationTracker2025.xlsx"
    upload_spreadsheet(file_path)
