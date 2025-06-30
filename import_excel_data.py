#!/usr/bin/env python
"""
Import data from JobApplicationTracker2025.xlsx into the real database
"""

import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Application, Base
from datetime import datetime
import os

def normalize_date(date_str):
    if pd.isna(date_str) or not date_str:
        return None
    try:
        return datetime.strptime(str(date_str), "%m/%d/%Y").date()
    except ValueError:
        try:
            return datetime.strptime(str(date_str), "%Y-%m-%d").date()
        except ValueError:
            return None

def parse_timestamp(timestamp_str):
    if pd.isna(timestamp_str) or not timestamp_str:
        return None  # Return None instead of default timestamp
    try:
        # Parse ISO format timestamp
        timestamp_str = str(timestamp_str)
        if 'Z' in timestamp_str:
            # Remove microseconds if present and replace Z with +00:00
            timestamp_str = timestamp_str.split('.')[0] + '+00:00'
        return datetime.fromisoformat(timestamp_str)
    except (ValueError, AttributeError) as e:
        print(f"Error parsing timestamp {timestamp_str}: {e}")
        return None  # Return None instead of default timestamp

def main():
    # Path to the Excel file
    file_path = os.path.join(os.path.dirname(__file__), "datasample", "JobApplicationTracker2025.xlsx")
    
    if not os.path.exists(file_path):
        print(f"Error: Excel file not found at {file_path}")
        return
    
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # First, clear the existing data
        from sqlalchemy import delete
        
        with SessionLocal() as session:
            session.execute(delete(Application))
            session.commit()
            print("Cleared existing applications from the real database.")
        
        # Now import the new data
        df = pd.read_excel(file_path, sheet_name="Sheet1")
        
        # Print column names for debugging
        print("Excel columns:", list(df.columns))
        print(f"Found {len(df)} rows in the Excel file")
        
        # Add debugging for timestamp column
        if 'Timestamp' in df.columns:
            print("Sample timestamps:", df['Timestamp'].iloc[:5].tolist())
        
        applications = []
        
        for _, row in df.iterrows():
            # Skip rows with missing required fields
            company = row.get('Company')
            role = row.get('Role')
            status = row.get('Status')
            
            if pd.isna(company) or pd.isna(role) or pd.isna(status):
                continue
                
            # For debugging, print the first row
            if _ == 0:
                print("Sample row:", dict(row))
                
            app = Application(
                order_number=row.get('Order number') if not pd.isna(row.get('Order number')) else None,
                company=company,
                role=role,
                url=row.get('URL') if not pd.isna(row.get('URL')) else None,
                status=status,
                application_date=normalize_date(row.get('Application Date')),
                met_with=row.get('Met with') if not pd.isna(row.get('Met with')) else None,
                notes=row.get('Notes') if not pd.isna(row.get('Notes')) else None,
                resume_file=row.get('Resume Link') if not pd.isna(row.get('Resume Link')) else None,
                cover_letter_file=row.get('Cover Letter Link') if not pd.isna(row.get('Cover Letter Link')) else None,
                follow_up_required=False,  # Default since column is missing
                pros=None,  # Default since column is missing
                cons=None,  # Default since column is missing
                salary=None  # Default since column is missing
                # Let created_at and updated_at use their default values
            )
            applications.append(app)
        
        with SessionLocal() as session:
            session.add_all(applications)
            session.commit()
        
        print(f"Successfully imported {len(applications)} applications.")
        
    except Exception as e:
        print(f"Error importing data: {e}")

if __name__ == "__main__":
    main()
