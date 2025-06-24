from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database import SessionLocal
from backend.models import JobApplication, DemoApplication, DemoStatusHistory
from backend.generate_demo_data import generate_demo_data, clear_demo_data
from app.schemas import ApplicationCreate, ApplicationUpdate, Application
from datetime import datetime
import os
from uuid import uuid4
import pandas as pd

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "rtf", "txt"}
MAX_FILE_SIZE_MB = 5

# Helper to save uploaded files
def save_upload_file(upload_file: UploadFile, folder: str) -> str:
    ext = upload_file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file type: {upload_file.filename}")
    contents = upload_file.file.read()
    if len(contents) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File too large: {upload_file.filename}")
    filename = f"{uuid4().hex}_{upload_file.filename}"
    file_path = os.path.join(folder, filename)
    with open(file_path, "wb") as f:
        f.write(contents)
    return filename

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/applications/", response_model=Application)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    db_app = JobApplication(**application.model_dump())
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

@app.get("/applications/", response_model=List[Application])
def list_applications(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return db.query(JobApplication).offset(skip).limit(limit).all()

@app.get("/applications/{app_id}", response_model=Application)
def get_application(app_id: int, db: Session = Depends(get_db)):
    app_obj = db.query(JobApplication).filter(JobApplication.id == app_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    return app_obj

@app.put("/applications/{app_id}", response_model=Application)
def update_application(app_id: int, application: ApplicationUpdate, db: Session = Depends(get_db)):
    app_obj = db.query(JobApplication).filter(JobApplication.id == app_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    for key, value in application.model_dump(exclude_unset=True).items():
        setattr(app_obj, key, value)
    db.commit()
    db.refresh(app_obj)
    return app_obj

@app.delete("/applications/{app_id}")
def delete_application(app_id: int, db: Session = Depends(get_db)):
    app_obj = db.query(JobApplication).filter(JobApplication.id == app_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(app_obj)
    db.commit()
    return {"detail": "Application deleted"}

@app.post("/applications/upload/", response_model=Application)
def create_application_with_files(
    company: str = Form(...),
    role: str = Form(...),
    status: str = Form(...),
    url: Optional[str] = Form(None),
    application_date: Optional[str] = Form(None),
    met_with: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    pros: Optional[str] = Form(None),
    cons: Optional[str] = Form(None),
    salary: Optional[str] = Form(None),
    follow_up_required: Optional[bool] = Form(False),
    resume_file: Optional[UploadFile] = File(None),
    cover_letter_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    resume_filename = save_upload_file(resume_file, UPLOAD_FOLDER) if resume_file else None
    cover_letter_filename = save_upload_file(cover_letter_file, UPLOAD_FOLDER) if cover_letter_file else None
    db_app = JobApplication(
        company=company,
        role=role,
        status=status,
        url=url,
        application_date=application_date,
        met_with=met_with,
        notes=notes,
        pros=pros,
        cons=cons,
        salary=salary,
        follow_up_required=follow_up_required,
        resume_file=resume_filename,
        cover_letter_file=cover_letter_filename
    )
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

# Demo mode endpoints
@app.get("/demo/applications/", response_model=List[Application])
def get_demo_applications(db: Session = Depends(get_db)):
    """Get all demo applications."""
    return db.query(DemoApplication).all()

@app.post("/demo/applications/", response_model=Application)
def create_demo_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    """Create a new demo application."""
    db_app = DemoApplication(**application.model_dump())
    
    # Add status history
    status_history = DemoStatusHistory(
        status=db_app.status,
        changed_at=datetime.utcnow(),
        notes=db_app.notes
    )
    db_app.status_history.append(status_history)
    
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

@app.get("/demo/applications/{application_id}", response_model=Application)
def get_demo_application(application_id: int, db: Session = Depends(get_db)):
    """Get a specific demo application."""
    db_app = db.query(DemoApplication).filter(DemoApplication.id == application_id).first()
    if db_app is None:
        raise HTTPException(status_code=404, detail="Demo application not found")
    return db_app

@app.patch("/demo/applications/{application_id}", response_model=Application)
def update_demo_application(
    application_id: int,
    application: ApplicationUpdate,
    db: Session = Depends(get_db)
):
    """Update a demo application."""
    db_app = db.query(DemoApplication).filter(DemoApplication.id == application_id).first()
    if db_app is None:
        raise HTTPException(status_code=404, detail="Demo application not found")
    
    update_data = application.model_dump(exclude_unset=True)
    
    # If status is being updated, add to history
    if "status" in update_data and update_data["status"] != db_app.status:
        status_history = DemoStatusHistory(
            application_id=application_id,
            status=update_data["status"],
            changed_at=datetime.utcnow(),
            notes=update_data.get("notes", None)
        )
        db.add(status_history)
    
    for key, value in update_data.items():
        setattr(db_app, key, value)
    
    db.commit()
    db.refresh(db_app)
    return db_app

@app.delete("/demo/applications/{application_id}")
def delete_demo_application(application_id: int, db: Session = Depends(get_db)):
    """Delete a demo application."""
    db_app = db.query(DemoApplication).filter(DemoApplication.id == application_id).first()
    if db_app is None:
        raise HTTPException(status_code=404, detail="Demo application not found")
    
    # Delete associated status history
    db.query(DemoStatusHistory).filter(DemoStatusHistory.application_id == application_id).delete()
    db.delete(db_app)
    db.commit()
    return {"ok": True}

@app.post("/demo/reset")
def reset_demo_data(db: Session = Depends(get_db)):
    """Reset demo data to initial state."""
    clear_demo_data(db)
    generate_demo_data(db)
    return {"message": "Demo data reset successfully"}

@app.get("/visualizations/applications_over_time/")
def applications_over_time(db: Session = Depends(get_db)):
    apps = db.query(JobApplication).all()
    df = pd.DataFrame([{
        'application_date': a.application_date,
        'status': a.status
    } for a in apps if a.application_date])
    if df.empty:
        return []
    df['application_date'] = pd.to_datetime(df['application_date'])
    grouped = df.groupby(df['application_date'].dt.to_period('M')).size().reset_index(name='count')
    grouped['application_date'] = grouped['application_date'].astype(str)
    return grouped.to_dict(orient='records')

@app.get("/visualizations/status_distribution/")
def status_distribution(db: Session = Depends(get_db)):
    apps = db.query(JobApplication).all()
    df = pd.DataFrame([{'status': a.status} for a in apps])
    if df.empty:
        return []
    grouped = df['status'].value_counts().reset_index()
    grouped.columns = ['status', 'count']
    return grouped.to_dict(orient='records')

@app.get("/visualizations/calendar/")
def calendar_view(db: Session = Depends(get_db)):
    apps = db.query(JobApplication).all()
    df = pd.DataFrame([{
        'id': a.id,
        'company': a.company,
        'role': a.role,
        'status': a.status,
        'status_change_date': getattr(a, 'status_change_date', None)
    } for a in apps if getattr(a, 'status_change_date', None)])
    if df.empty:
        return []
    df['status_change_date'] = pd.to_datetime(df['status_change_date'])
    grouped = df.groupby('status_change_date').apply(lambda x: x.to_dict(orient='records')).to_dict()
    # Convert keys to string for JSON serialization
    return {str(k.date()): v for k, v in grouped.items()}