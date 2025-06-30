# Import JSON for debugging
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from database import get_db
import demo_crud, demo_models, schemas
import logging
import json

router = APIRouter(prefix="/demo", tags=["demo"])
logger = logging.getLogger(__name__)

# Get all applications
@router.get("/applications/", response_model=List[schemas.Application])
def read_demo_applications(db: Session = Depends(get_db)):
    applications = demo_crud.get_demo_applications(db)
    logger.info(f"Fetched {len(applications)} demo applications")
    return applications

# Get single application
@router.get("/applications/{app_id}", response_model=schemas.Application)
def read_demo_application(app_id: int, db: Session = Depends(get_db)):
    db_app = demo_crud.get_demo_application(db, app_id)
    if db_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_app

# Create application
@router.post("/applications/", response_model=schemas.Application)
async def create_demo_application(
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
    try:
        logger.info(f"Received demo form data: company={company}, role={role}, status={status}, application_date={application_date}")
        
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
        
        # Process file uploads
        resume_filename = None
        cover_letter_filename = None
        
        if resume_file:
            resume_filename = demo_crud.save_demo_upload_file(resume_file, "resume")
        
        if cover_letter_file:
            cover_letter_filename = demo_crud.save_demo_upload_file(cover_letter_file, "cover_letter")
        
        # Create application data
        application_data = {
            "company": company,
            "role": role,
            "status": status,
            "url": url,
            "met_with": met_with,
            "notes": notes,
            "pros": pros,
            "cons": cons,
            "salary": salary,
            "follow_up_required": follow_up_required,
            "resume_file": resume_filename,
            "cover_letter_file": cover_letter_filename,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "status_change_date": datetime.now()
        }
        
        # Handle application_date separately with more robust validation
        if application_date and application_date.strip():
            try:
                application_data["application_date"] = datetime.strptime(application_date, "%Y-%m-%d").date()
                logger.info(f"Parsed application_date: {application_data['application_date']}")
            except ValueError as e:
                logger.error(f"Error parsing application_date '{application_date}': {str(e)}")
                # Set to None if we can't parse it
                application_data["application_date"] = None
        else:
            application_data["application_date"] = None
        
        return demo_crud.create_demo_application(db, application_data)
    except Exception as e:
        logger.error(f"Error creating application: {str(e)}")
        logger.exception("Detailed error:")
        raise
    
    logger.info(f"Creating demo application: {company} - {role}")
    return demo_crud.create_demo_application(db, application_data)

# Update application - support both PUT and PATCH
@router.put("/applications/{app_id}", response_model=schemas.Application)
@router.patch("/applications/{app_id}", response_model=schemas.Application)
async def update_demo_application(
    app_id: int,
    company: Optional[str] = Form(None),
    role: Optional[str] = Form(None),
    status: Optional[str] = Form(None),
    url: Optional[str] = Form(None),
    application_date: Optional[str] = Form(None),  # Changed from date to str
    met_with: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    pros: Optional[str] = Form(None),
    cons: Optional[str] = Form(None),
    salary: Optional[str] = Form(None),
    follow_up_required: Optional[bool] = Form(None),
    resume_file: Optional[UploadFile] = File(None),
    cover_letter_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Check if application exists
    db_app = demo_crud.get_demo_application(db, app_id)
    if db_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Process file uploads
    resume_filename = db_app.resume_file
    cover_letter_filename = db_app.cover_letter_file
    
    if resume_file:
        resume_filename = demo_crud.save_demo_upload_file(resume_file, "resume")
    
    if cover_letter_file:
        cover_letter_filename = demo_crud.save_demo_upload_file(cover_letter_file, "cover_letter")
    
    # Create update data with only provided fields
    update_data = {}
    form_data = {
        "company": company,
        "role": role,
        "status": status,
        "url": url,
        "met_with": met_with,
        "notes": notes,
        "pros": pros,
        "cons": cons,
        "salary": salary,
        "follow_up_required": follow_up_required,
        "resume_file": resume_filename,
        "cover_letter_file": cover_letter_filename,
        "updated_at": datetime.now()
    }
    
    # Handle application_date separately with more robust validation
    if application_date is not None:
        if application_date.strip():
            try:
                update_data["application_date"] = datetime.strptime(application_date, "%Y-%m-%d").date()
                logger.info(f"Parsed update application_date: {update_data['application_date']}")
            except ValueError as e:
                logger.error(f"Error parsing update application_date '{application_date}': {str(e)}")
                # Keep as None if we can't parse it
        else:
            # Empty string becomes None
            update_data["application_date"] = None
    
    # Only include non-None values from form_data
    for key, value in form_data.items():
        if value is not None:
            update_data[key] = value
    
    # Update status_change_date if status is changed
    if status and status != db_app.status:
        update_data["status_change_date"] = datetime.now()
    
    logger.info(f"Updating demo application: {app_id}")
    return demo_crud.update_demo_application(db, app_id, update_data)

# Debug endpoint for JSON submission (for testing)
@router.post("/applications/debug/", response_model=schemas.Application)
async def create_demo_application_json(
    application: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):
    logger.info(f"Debug JSON application creation: {application}")
    
    # Create application data with required fields
    application_data = {
        "company": application.get("company", "Debug Company"),
        "role": application.get("role", "Debug Role"),
        "status": application.get("status", "Applied"),
        "url": application.get("url"),
        "met_with": application.get("met_with"),
        "notes": application.get("notes"),
        "pros": application.get("pros"),
        "cons": application.get("cons"),
        "salary": application.get("salary"),
        "follow_up_required": application.get("follow_up_required", False),
        "resume_file": application.get("resume_file"),
        "cover_letter_file": application.get("cover_letter_file"),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "status_change_date": datetime.now()
    }
    
    # Handle application date
    app_date = application.get("application_date")
    if app_date and isinstance(app_date, str) and app_date.strip():
        try:
            application_data["application_date"] = datetime.strptime(app_date, "%Y-%m-%d").date()
        except ValueError:
            application_data["application_date"] = None
    else:
        application_data["application_date"] = None
    
    return demo_crud.create_demo_application(db, application_data)

# Delete application
@router.delete("/applications/{app_id}", response_model=schemas.Application)
def delete_demo_application(app_id: int, db: Session = Depends(get_db)):
    db_app = demo_crud.get_demo_application(db, app_id)
    if db_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return demo_crud.delete_demo_application(db, app_id)

# Get visualizations for demo data
@router.get("/visualizations/")
def get_demo_visualizations(db: Session = Depends(get_db)):
    logger.info("Generating demo visualizations")
    # Get all applications
    applications = demo_crud.get_demo_applications(db)
    
    # Count applications by month
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    month_counts = [0] * 12
    
    # Count applications by status
    status_counts = {}
    
    for app in applications:
        if app.application_date:
            month_idx = app.application_date.month - 1
            month_counts[month_idx] += 1
        
        if app.status:
            if app.status in status_counts:
                status_counts[app.status] += 1
            else:
                status_counts[app.status] = 1
    
    # Prepare data for charts
    status_labels = list(status_counts.keys())
    status_data = list(status_counts.values())
    
    # Colors for status distribution
    status_colors = {
        "Not Yet Applied": "#FFFFFF",        # White
        "Applied": "#FFCE56",                # Yellow
        "Interviewing": "#FF9F40",           # Orange
        "Offer": "#4BC0C0",                  # Green
        "Rejected": "#FF6384",               # Red
        "No Longer Listed": "#9E9E9E",       # Gray
        "Decided not to apply": "#8D6E63",   # Brown
        "Declined Offer": "#000000",         # Black
        "Accepted": "#FF5722",               # Dark Orange
        "Applied / No Longer Listed": "#E0E0E0" # Light Gray
    }
    
    status_background_colors = [status_colors.get(status, "#9966FF") for status in status_labels]
    
    # Only return months from March to June
    relevant_months = months[2:7]  # March to July (0-based, so 2-6)
    relevant_counts = month_counts[2:7]
    
    return {
        "overTime": {
            "labels": relevant_months,
            "datasets": [
                {
                    "label": "Applications",
                    "data": relevant_counts,
                    "backgroundColor": "#36A2EB"
                }
            ]
        },
        "statusDistribution": {
            "labels": status_labels,
            "datasets": [
                {
                    "data": status_data,
                    "backgroundColor": status_background_colors
                }
            ]
        },
        "calendar": {
            # Sample calendar data based on real applications
            "events": [
                {
                    "date": app.application_date.strftime("%Y-%m-%d") if app.application_date else None,
                    "title": f"{app.company} - {app.role}",
                    "status": app.status,
                    "id": app.id
                } for app in applications if app.application_date
            ]
        }
    }

# File upload endpoints
@router.post("/applications/{app_id}/files/{file_type}", response_model=schemas.Application)
async def upload_demo_file(
    app_id: int, 
    file_type: str, 
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Check if application exists
    db_app = demo_crud.get_demo_application(db, app_id)
    if db_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Validate file_type
    if file_type not in ["resume", "cover_letter"]:
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Must be 'resume' or 'cover_letter'"
        )
    
    # Save the file
    filename = demo_crud.save_demo_upload_file(file, file_type)
    
    # Update application with file reference
    update_data = {
        f"{file_type}_file": filename,
        "updated_at": datetime.now()
    }
    
    logger.info(f"Uploading {file_type} for demo application: {app_id}")
    return demo_crud.update_demo_application(db, app_id, update_data)
