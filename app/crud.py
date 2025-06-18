from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from app import models, schemas
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

def get_filtered_applications(db: Session, filters: dict):
    query = db.query(models.Application)
    for key, value in filters.items():
        if value is not None:
            query = query.filter(getattr(models.Application, key) == value)
    return query.all()

def get_application(db: Session, application_id: int):
    return db.query(models.Application).filter(models.Application.id == application_id).first()

def update_application(db: Session, application_id: int, application_update: schemas.ApplicationUpdate):
    db_application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not db_application:
        return None
    for key, value in application_update.dict(exclude_unset=True).items():
        setattr(db_application, key, value)
    db.commit()
    db.refresh(db_application)
    return db_application

def delete_application(db: Session, application_id: int):
    db_application = db.query(models.Application).filter(models.Application.id == application_id).first()
    if db_application:
        db.delete(db_application)
        db.commit()
    return db_application
