#!/usr/bin/env python3
"""
Real data API server that connects to the actual database.
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, DateTime, func, text, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import uvicorn
import os
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi.staticfiles import StaticFiles

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
REAL_DB_URL = "sqlite:///./jobtracker.db"
DEMO_DB_URL = "sqlite:///./demo_jobtracker.db"

# Create engines for both databases
real_engine = create_engine(REAL_DB_URL, connect_args={"check_same_thread": False})
demo_engine = create_engine(DEMO_DB_URL, connect_args={"check_same_thread": False})

# Create session factories
RealSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=real_engine)
DemoSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=demo_engine)

Base = declarative_base()

# Define models
class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    status = Column(String, nullable=False)
    url = Column(String, nullable=True)
    application_date = Column(String, nullable=True)  # Changed from Date to String to match real DB
    met_with = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    follow_up_required = Column(Boolean, default=False)
    pros = Column(String, nullable=True)
    cons = Column(String, nullable=True)
    salary = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

app = FastAPI(debug=True)

# Create the tables if they don't exist
Base.metadata.create_all(bind=real_engine)
Base.metadata.create_all(bind=demo_engine)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory if it exists
if os.path.exists("uploads"):
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Dependency to get real DB session
def get_real_db():
    db = RealSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get demo DB session
def get_demo_db():
    db = DemoSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
def read_root():
    """Root endpoint."""
    logger.info("Root endpoint called")
    return {"message": "Job Tracker API is running with real data", "version": "1.0"}

# Test endpoint
@app.get("/test")
def test_endpoint():
    """Test endpoint."""
    logger.info("Test endpoint called")
    return {"message": "Test endpoint working!"}

# Real applications endpoints
@app.get("/applications/")
def get_applications(db: Session = Depends(get_real_db)):
    """Real applications endpoint."""
    logger.info("Applications endpoint called")
    applications = db.query(Application).all()
    return [format_application(app) for app in applications]

@app.get("/applications/{app_id}")
def get_application(app_id: int, db: Session = Depends(get_real_db)):
    """Get a specific application by ID."""
    logger.info(f"Get application {app_id} called")
    application = db.query(Application).filter(Application.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return format_application(application)

# Demo applications endpoints
@app.get("/demo/applications/")
def get_demo_applications(db: Session = Depends(get_demo_db)):
    """Demo applications endpoint."""
    logger.info("Demo applications endpoint called")
    applications = db.query(Application).all()
    return [format_application(app) for app in applications]

@app.get("/demo/applications/{app_id}")
def get_demo_application(app_id: int, db: Session = Depends(get_demo_db)):
    """Get a specific demo application by ID."""
    logger.info(f"Get demo application {app_id} called")
    application = db.query(Application).filter(Application.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Demo application not found")
    return format_application(application)

# Visualizations endpoints
@app.get("/visualizations/")
def get_visualizations(db: Session = Depends(get_real_db)):
    """Visualizations endpoint."""
    logger.info("Visualizations endpoint called")
    return generate_visualizations(db)

@app.get("/demo/visualizations/")
def get_demo_visualizations(db: Session = Depends(get_demo_db)):
    """Demo visualizations endpoint."""
    logger.info("Demo visualizations endpoint called")
    return generate_visualizations(db)

# CRUD operations
@app.post("/applications/")
def create_application(application: dict, db: Session = Depends(get_real_db)):
    """Create a new application."""
    logger.info("Create application called")
    new_app = Application(**application)
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return format_application(new_app)

@app.patch("/applications/{app_id}")
def update_application(app_id: int, updates: dict, db: Session = Depends(get_real_db)):
    """Update an application."""
    logger.info(f"Update application {app_id} called")
    application = db.query(Application).filter(Application.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    for key, value in updates.items():
        if hasattr(application, key):
            setattr(application, key, value)
    
    db.commit()
    db.refresh(application)
    return format_application(application)

@app.delete("/applications/{app_id}")
def delete_application(app_id: int, db: Session = Depends(get_real_db)):
    """Delete an application."""
    logger.info(f"Delete application {app_id} called")
    application = db.query(Application).filter(Application.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    db.delete(application)
    db.commit()
    return {"message": f"Application {app_id} deleted"}

# Helper function to format application objects for JSON response
def format_application(app):
    """Convert SQLAlchemy model to dict."""
    result = {c.name: getattr(app, c.name) for c in app.__table__.columns}
    
    # Convert date objects to strings
    if result.get('application_date') and not isinstance(result['application_date'], str):
        result['application_date'] = result['application_date'].isoformat() if result['application_date'] else None
    
    # Convert datetime objects to strings
    for date_field in ['created_at', 'updated_at']:
        if result.get(date_field) and not isinstance(result[date_field], str):
            result[date_field] = result[date_field].isoformat() if result[date_field] else None
    
    return result

# Helper function to generate visualization data
def generate_visualizations(db: Session):
    """Generate visualization data from database."""
    # Count applications by status
    status_counts_query = db.query(
        Application.status, 
        func.count(Application.id).label('count')
    ).group_by(Application.status).all()
    
    status_data = [{"status": status, "count": count} for status, count in status_counts_query]
    
    # Generate timeline data - applications per week for the last 12 weeks
    today = datetime.now()
    timeline_data = []
    
    for i in range(12):
        week_start = today - timedelta(days=7*i)
        week_end = week_start + timedelta(days=7)
        week_start_str = week_start.strftime("%Y-%m-%d")
        
        # SQL query to count applications within the date range
        count_query = db.query(func.count(Application.id)).filter(
            Application.application_date >= week_start.date(),
            Application.application_date < week_end.date()
        ).scalar()
        
        timeline_data.append({
            "date": week_start_str,
            "count": count_query or 0  # Use 0 if None
        })
    
    # Reverse to get chronological order
    timeline_data.reverse()
    
    return {
        "status_counts": status_data,
        "timeline_data": timeline_data
    }

# Debug endpoints
@app.get("/debug/info")
def debug_info(real_db: Session = Depends(get_real_db), demo_db: Session = Depends(get_demo_db)):
    """Return debug information about the server."""
    real_count = real_db.query(func.count(Application.id)).scalar() or 0
    demo_count = demo_db.query(func.count(Application.id)).scalar() or 0
    
    return {
        "server_time": datetime.now().isoformat(),
        "environment": dict(os.environ),
        "api_base": os.environ.get("VITE_API_BASE", "http://localhost:8006"),
        "database_info": {
            "real_db_url": REAL_DB_URL,
            "demo_db_url": DEMO_DB_URL,
            "real_application_count": real_count,
            "demo_application_count": demo_count
        }
    }

@app.get("/debug/config")
def debug_config():
    """Debug endpoint to show environment configuration."""
    return {
        "environment": dict(os.environ),
        "api_base": os.environ.get("VITE_API_BASE", "http://localhost:8006")
    }

# For direct execution
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8006))
    logger.info(f"Starting real data server on port {port}")
    uvicorn.run(app, host="127.0.0.1", port=port)
