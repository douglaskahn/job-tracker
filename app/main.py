import os
import logging
from uuid import uuid4
from typing import List, Optional
from datetime import date

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app import models, crud, schemas, demo_models
from app.database import engine, SessionLocal
from app.demo_routes import router as demo_router
from app import demo_data

app = FastAPI()

# CORS middleware for frontend/backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],  # Allow various dev server ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the uploads directory to serve files statically
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

models.Base.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Startup event to initialize demo data
@app.on_event("startup")
def startup_event():
    # Initialize demo database
    demo_models.Base.metadata.create_all(bind=engine)
    
    # Initialize demo data (generated applications)
    demo_data.initialize_demo_data()
    logger.info("Application startup: Demo data initialized")

@app.get("/")
def read_root():
    """Root endpoint: Returns a welcome message."""
    return {"message": "Welcome to the Job Application Tracker API"}

# Include demo router
app.include_router(demo_router)

# --- API Endpoints ---

@app.post("/applications/", response_model=schemas.Application)
async def create_application(
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
    import traceback
    try:
        # Validate required fields
        if not company or not company.strip():
            company = "Untitled Company"
            logger.warning(f"Empty company name provided, using default: {company}")
            
        if not role or not role.strip():
            role = "Untitled Role"
            logger.warning(f"Empty role provided, using default: {role}")
            
        if not status or not status.strip():
            status = "Not Yet Applied"
            logger.warning(f"Empty status provided, using default: {status}")
            
        async def save_file(file: UploadFile, folder: str) -> str:
            if file:
                filename = f"{uuid4().hex}_{file.filename}"
                file_path = os.path.join(folder, filename)
                content = await file.read()
                with open(file_path, "wb") as f:
                    f.write(content)
                return filename
            return None

        resume_path = await save_file(resume_file, UPLOAD_FOLDER) if resume_file else None
        cover_letter_path = await save_file(cover_letter_file, UPLOAD_FOLDER) if cover_letter_file else None

        # Build ApplicationCreate object for CRUD
        app_create = schemas.ApplicationCreate(
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
            resume_file=resume_path,
            cover_letter_file=cover_letter_path
        )
        db_app = crud.create_application(db, application=app_create)
        return db_app
    except Exception as e:
        print("[DEBUG] Exception in POST /applications/:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/applications/", response_model=List[schemas.Application])
def list_applications(
    skip: int = 0,
    limit: int = 1000,  # Return up to 1000 records by default
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
async def update_application(
    app_id: int,
    company: str = Form(...),  # Required
    role: str = Form(...),     # Required
    status: str = Form(...),   # Required
    url: str = Form(""),       # Optional, explicitly handle empty string
    application_date: str = Form(""),  # Optional
    met_with: str = Form(""),  # Optional
    notes: str = Form(""),     # Optional
    pros: str = Form(""),      # Optional
    cons: str = Form(""),      # Optional
    salary: str = Form(""),    # Optional
    follow_up_required: bool = Form(False),
    resume_file: Optional[UploadFile] = File(None),
    cover_letter_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Update an existing job application."""
    try:
        # Get existing application
        existing_app = crud.get_application(db, application_id=app_id)
        if existing_app is None:
            raise HTTPException(status_code=404, detail="Application not found")

        # Log received data for debugging
        logger.info(f"Received form data for update: company={company}, role={role}, status={status}, follow_up_required={follow_up_required}")
        
        async def save_file(file: UploadFile, folder: str, existing_path: str) -> str:
            if file:
                # Delete existing file if it exists
                if existing_path and os.path.exists(existing_path):
                    try:
                        os.remove(existing_path)
                    except Exception as e:
                        logger.warning(f"Failed to delete old file {existing_path}: {e}")
                
                filename = f"{uuid4().hex}_{file.filename}"
                file_path = os.path.join(folder, filename)
                content = await file.read()
                with open(file_path, "wb") as f:
                    f.write(content)
                return file_path
            return existing_path  # Keep existing path if no new file

        # Handle file updates
        resume_path = await save_file(resume_file, UPLOAD_FOLDER, existing_app.resume_file) if resume_file else existing_app.resume_file
        cover_letter_path = await save_file(cover_letter_file, UPLOAD_FOLDER, existing_app.cover_letter_file) if cover_letter_file else existing_app.cover_letter_file

        # Debug logging
        update_data = {
            'company': company,
            'role': role,
            'status': status,
            'url': url,
            'application_date': application_date,
            'met_with': met_with,
            'notes': notes,
            'pros': pros,
            'cons': cons,
            'salary': salary,
            'follow_up_required': follow_up_required,
            'resume_file': resume_path,
        }
        logger.info(f"Updating application {app_id} with data: {update_data}")

        # Log received form data
        form_data = {
            'company': company,
            'role': role,
            'status': status,
            'url': url,
            'application_date': application_date,
            'met_with': met_with,
            'notes': notes,
            'pros': pros,
            'cons': cons,
            'salary': salary,
            'follow_up_required': follow_up_required,
            'resume_file': resume_path,
            'cover_letter_file': cover_letter_path
        }
        logger.info(f"Processing update form data: {form_data}")
        
        # Build ApplicationUpdate object
        app_update = schemas.ApplicationUpdate(**{
            k: v for k, v in form_data.items() if v is not None
        })
        
        # Log the processed update object
        logger.info(f"Created update object: {app_update.dict()}")

        updated_app = crud.update_application(db, application_id=app_id, application_update=app_update)
        if updated_app is None:
            raise HTTPException(status_code=404, detail="Application not found")
        return updated_app
        
    except ValueError as ve:
        logger.error(f"Validation error updating application {app_id}: {ve}")
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"Error updating application {app_id}: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.patch("/applications/{app_id}", response_model=schemas.Application)
async def patch_application(
    app_id: int,
    data: schemas.ApplicationUpdate,  # JSON data for update
    db: Session = Depends(get_db)
):
    """Update application data fields (excluding files)."""
    logger.info(f"PATCH request for application {app_id} with data: {data}")
    
    db_app = crud.update_application(db, app_id, data)
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return db_app

@app.delete("/applications/{app_id}", response_model=schemas.Application)
def delete_application(app_id: int, db: Session = Depends(get_db)) -> schemas.Application:
    """Delete a job application by ID."""
    deleted_app = crud.delete_application(db, application_id=app_id)
    if deleted_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return deleted_app

@app.get("/visualizations/")
def get_visualizations():
    # Return empty/default data structure for now
    return {
        "overTime": {},
        "statusDistribution": {},
        "calendar": {}
    }

@app.get("/demo/applications/")
def get_demo_applications():
    # Return a list of demo applications for the frontend demo mode
    return [
        {
            "id": 1,
            "company": "DemoCorp",
            "role": "Frontend Developer",
            "url": "https://democorp.com/jobs/1",
            "status": "Applied",
            "application_date": "2025-06-01",
            "met_with": "Jane Demo",
            "notes": "Demo application for testing.",
            "resume_file": None,
            "cover_letter_file": None,
            "order_number": 1,
            "follow_up_required": False,
            "pros": "Great team",
            "cons": "Long commute",
            "salary": "100000",
            "created_at": None,
            "updated_at": None
        },
        {
            "id": 2,
            "company": "Sample Inc.",
            "role": "Backend Engineer",
            "url": "https://sampleinc.com/jobs/2",
            "status": "Interviewing",
            "application_date": "2025-06-10",
            "met_with": "John Sample",
            "notes": "Second round scheduled.",
            "resume_file": None,
            "cover_letter_file": None,
            "order_number": 2,
            "follow_up_required": True,
            "pros": "Remote work",
            "cons": "Startup risk",
            "salary": "120000",
            "created_at": None,
            "updated_at": None
        }
    ]
