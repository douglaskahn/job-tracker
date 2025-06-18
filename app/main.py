from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
import os
from uuid import uuid4
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import logging

from app import models, crud, schemas
from app.database import engine, SessionLocal

from typing import List, Optional
from datetime import date

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

logger = logging.getLogger(__name__)

# CORS middleware for frontend/backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    """Root endpoint: Returns a welcome message."""
    return {"message": "Welcome to the Job Application Tracker API"}

# --- API Endpoints ---

@app.post("/applications/", response_model=schemas.Application)
async def create_application(
    company: str,
    role: str,
    status: str,
    job_url: Optional[str] = None,
    application_date: Optional[date] = None,
    met_with: Optional[str] = None,
    notes: Optional[str] = None,
    follow_up: Optional[bool] = False,
    pros: Optional[str] = None,
    cons: Optional[str] = None,
    salary: Optional[str] = None,
    resume_file: Optional[UploadFile] = File(None),
    cover_letter_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
) -> schemas.Application:
    logger.info(f"Incoming data: company={company}, role={role}, status={status}, application_date={application_date}")
    allowed_extensions = {"pdf", "doc", "docx"}

    if resume_file and resume_file.filename == "":
        raise HTTPException(status_code=400, detail="Resume file is empty")
    if cover_letter_file and cover_letter_file.filename == "":
        raise HTTPException(status_code=400, detail="Cover letter file is empty")

    def save_file(file: UploadFile, folder: str) -> str:
        if file:
            filename = f"{uuid4().hex}_{file.filename}"
            file_path = os.path.join(folder, filename)
            with open(file_path, "wb") as f:
                f.write(file.file.read())
            return file_path
        return None

    resume_path = save_file(resume_file, UPLOAD_FOLDER) if resume_file else None
    cover_letter_path = save_file(cover_letter_file, UPLOAD_FOLDER) if cover_letter_file else None

    app_data = schemas.ApplicationMetadata(
        company=company,
        role=role,
        status=status,
        job_url=job_url,
        application_date=application_date,
        met_with=met_with,
        notes=notes,
        follow_up=follow_up,
        pros=pros,
        cons=cons,
        salary=salary,
    )

    return crud.create_application(db=db, app_data=app_data, resume_path=resume_path, cover_letter_path=cover_letter_path)

@app.get("/applications/", response_model=List[schemas.Application])
def list_applications(
    skip: int = 0,
    limit: int = 10,
    search: str = None,
    status: str = None,
    follow_up_required: bool = None,
    missing_date: bool = None,
    sort_by: str = "created_at",
    sort_order: str = "asc",
    db: Session = Depends(get_db),
) -> List[schemas.Application]:
    """List job applications with advanced filtering, searching, and sorting."""
    return crud.get_filtered_applications(
        db=db,
        search=search,
        status=status,
        follow_up_required=follow_up_required,
        missing_date=missing_date,
        sort_by=sort_by,
        sort_order=sort_order,
        skip=skip,
        limit=limit,
    )

@app.get("/applications/{app_id}", response_model=schemas.Application)
def read_application(app_id: int, db: Session = Depends(get_db)) -> schemas.Application:
    """Retrieve a specific job application by ID."""
    app = crud.get_application(db, application_id=app_id)
    if app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return app

@app.put("/applications/{app_id}", response_model=schemas.Application)
def update_application(app_id: int, app_data: schemas.ApplicationUpdate, db: Session = Depends(get_db)) -> schemas.Application:
    """Update an existing job application."""
    updated_app = crud.update_application(db, application_id=app_id, app_data=app_data)
    if updated_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return updated_app

@app.delete("/applications/{app_id}", response_model=schemas.Application)
def delete_application(app_id: int, db: Session = Depends(get_db)) -> schemas.Application:
    """Delete a job application by ID."""
    deleted_app = crud.delete_application(db, application_id=app_id)
    if deleted_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return deleted_app
