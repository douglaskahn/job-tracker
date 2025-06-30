from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
import models, schemas
from datetime import datetime
from typing import Optional
import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the upload folder exists

def create_application(db: Session, application: schemas.ApplicationCreate):
    db_application = models.Application(**application.dict())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_filtered_applications(
    db: Session,
    search: str = None,
    status: str = None,
    follow_up_required: bool = None,
    missing_date: bool = None,
    sort_by: str = "created_at",
    sort_order: str = "asc",
    skip: int = 0,
    limit: int = 10,
):
    query = db.query(models.Application)
    if search:
        query = query.filter(
            models.Application.company.ilike(f"%{search}%") |
            models.Application.role.ilike(f"%{search}%")
        )
    if status:
        query = query.filter(models.Application.status == status)
    if follow_up_required is not None:
        query = query.filter(models.Application.follow_up_required == follow_up_required)
    if missing_date:
        query = query.filter(models.Application.application_date == None)
    if sort_by and hasattr(models.Application, sort_by):
        sort_column = getattr(models.Application, sort_by)
        if sort_order == "desc":
            sort_column = desc(sort_column)
        else:
            sort_column = asc(sort_column)
        query = query.order_by(sort_column)
    query = query.offset(skip).limit(limit)
    return query.all()

def get_application(db: Session, application_id: int):
    return db.query(models.Application).filter(models.Application.id == application_id).first()

def update_application(db: Session, application_id: int, application_update: schemas.ApplicationUpdate):
    """Update an application with new data. Handles empty fields by converting them to NULL."""
    try:
        print(f"Updating application {application_id} with data: {application_update}")
        
        db_application = db.query(models.Application).filter(models.Application.id == application_id).first()
        if not db_application:
            return None
            
        # Convert the update data to dict, excluding unset values
        update_data = application_update.dict(exclude_unset=True)
        print(f"Update data after conversion: {update_data}")
        
        # Handle special fields
        if 'follow_up_required' in update_data:
            # Handle boolean field
            if isinstance(update_data['follow_up_required'], str):
                update_data['follow_up_required'] = update_data['follow_up_required'].lower() == 'true'
            
        if 'application_date' in update_data:
            # Handle empty date
            if not update_data['application_date']:
                update_data['application_date'] = None
            else:
                try:
                    update_data['application_date'] = datetime.strptime(
                        update_data['application_date'], 
                        "%Y-%m-%d"
                    ).date()
                except ValueError as e:
                    raise ValueError(f"Invalid date format: {e}")
        
        # Add updated timestamp
        update_data['updated_at'] = datetime.now()
        
        print(f"Final update data before applying: {update_data}")
        
        # Update fields and track changes
        changes = []
        optional_text_fields = {'url', 'met_with', 'notes', 'pros', 'cons', 'salary'}
        
        for key, value in update_data.items():
            old_value = getattr(db_application, key, None)
            
            # Special handling for string values
            if isinstance(value, str):
                # For optional text fields, empty string means NULL
                if key in optional_text_fields and value.strip() == '':
                    value = None
                # For required fields, keep the non-empty value
                elif key in {'company', 'role', 'status'}:
                    if value.strip() == '':
                        continue  # Skip empty required fields
                    value = value.strip()
            
            # Special handling for dates
            if key == 'application_date' and value == '':
                value = None
            
            # Check for actual changes
            if old_value != value:
                changes.append(f"{key}: {old_value} -> {value}")
                # Log extra details for debugging string/None transitions
                print(f"Field {key} changing: type(old)={type(old_value)}, type(new)={type(value)}, "
                      f"old={repr(old_value)}, new={repr(value)}")
                setattr(db_application, key, value)
        
        if changes:
            print(f"Changes made to application {application_id}:")
            for change in changes:
                print(f"  {change}")
        else:
            print(f"No changes detected for application {application_id}")
        
        # Force the session to recognize the changes and commit
        db.flush()
        db.commit()
        db.refresh(db_application)  # Refresh to ensure we have the latest state
        
        # Refresh and verify
        db.refresh(db_application)
        print(f"Updated application state: {db_application.__dict__}")
        
        return db_application
            
        db.commit()
        db.refresh(db_application)
        return db_application
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to update application: {str(e)}")

def delete_application(db: Session, application_id: int):
    db_application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if db_application:
        db.delete(db_application)
        db.commit()
    return db_application
