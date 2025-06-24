from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.demo_models import DemoApplication
import os
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)

# Get all applications with optional skip/limit for pagination
def get_demo_applications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DemoApplication).offset(skip).limit(limit).all()

# Get a single application by ID
def get_demo_application(db: Session, app_id: int):
    return db.query(DemoApplication).filter(DemoApplication.id == app_id).first()

# Create a new application
def create_demo_application(db: Session, application_data: Dict[str, Any]):
    db_app = DemoApplication(**application_data)
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    logger.info(f"Created demo application: {db_app.id} - {db_app.company} - {db_app.role}")
    return db_app

# Update an existing application
def update_demo_application(db: Session, app_id: int, application_data: Dict[str, Any]):
    db_app = db.query(DemoApplication).filter(DemoApplication.id == app_id).first()
    if db_app:
        for key, value in application_data.items():
            setattr(db_app, key, value)
        db.commit()
        db.refresh(db_app)
        logger.info(f"Updated demo application: {db_app.id} - {db_app.company} - {db_app.role}")
    return db_app

# Delete an application
def delete_demo_application(db: Session, app_id: int):
    db_app = db.query(DemoApplication).filter(DemoApplication.id == app_id).first()
    if db_app:
        db.delete(db_app)
        db.commit()
        logger.info(f"Deleted demo application: {app_id}")
    return db_app

# Handle file upload for demo applications
def save_demo_upload_file(file, file_type: str) -> str:
    if not file:
        return None
    
    filename = file.filename
    # Generate unique filename
    unique_filename = f"{uuid4().hex}_{filename}"
    upload_folder = "uploads"
    
    # Ensure folder exists
    os.makedirs(upload_folder, exist_ok=True)
    
    # Save file
    file_path = os.path.join(upload_folder, unique_filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    logger.info(f"Saved demo {file_type} file: {unique_filename}")
    return unique_filename
