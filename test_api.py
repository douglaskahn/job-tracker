#!/usr/bin/env python3
"""
A simple FastAPI application to test the environment.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import logging
from datetime import datetime, timedelta
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(debug=True)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Root endpoint."""
    logger.info("Root endpoint called")
    return {"message": "Job Tracker API is running", "version": "Test Server 1.0"}

@app.get("/test")
def test_endpoint():
    """Test endpoint."""
    logger.info("Test endpoint called")
    return {"message": "Test endpoint working!"}

# Generate some realistic sample data
def generate_application_data(count=60, is_demo=False):
    """Generate realistic application data."""
    prefix = "Demo" if is_demo else ""
    companies = [
        f"{prefix}Tech", f"{prefix}Corp", f"{prefix}Global", f"{prefix}Innovations", 
        f"{prefix}Software", f"{prefix}Systems", f"{prefix}Digital", f"{prefix}Cloud",
        f"{prefix}Works", f"{prefix}Solutions", f"{prefix}AI", f"{prefix}ML"
    ]
    
    roles = [
        "Software Engineer", "Frontend Developer", "Backend Developer", 
        "Data Scientist", "DevOps Engineer", "Product Manager", "UX Designer"
    ]
    
    statuses = [
        "Not Yet Applied", "Applied", "Phone Screen", "Technical Interview", 
        "Onsite Interview", "Offer Received", "Rejected", "Accepted"
    ]
    
    applications = []
    for i in range(1, count + 1):
        today = datetime.now()
        company = random.choice(companies)
        role = random.choice(roles)
        status = random.choice(statuses)
        days_ago = random.randint(1, 90)
        app_date = (today - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        application = {
            "id": i,
            "company": f"{company} {i}",
            "role": role,
            "status": status,
            "url": f"https://example.com/jobs/{i}",
            "application_date": app_date,
            "met_with": f"{'Jane' if i % 2 == 0 else 'John'} Recruiter",
            "notes": f"{'Demo' if is_demo else ''} application with ID {i}",
            "follow_up_required": i % 3 == 0,  # Every third application needs follow-up
            "pros": "Good benefits, interesting work",
            "cons": "Long commute, high workload",
            "salary": f"{random.randint(80, 150)}000",
            "created_at": (today - timedelta(days=days_ago)).isoformat(),
            "updated_at": (today - timedelta(days=random.randint(0, days_ago))).isoformat()
        }
        applications.append(application)
    
    return applications

# Cache the generated data
REAL_APPLICATIONS = generate_application_data(40, is_demo=False)
DEMO_APPLICATIONS = generate_application_data(30, is_demo=True)

@app.get("/applications/")
def get_applications():
    """Real applications endpoint."""
    logger.info("Applications endpoint called")
    return REAL_APPLICATIONS

@app.get("/demo/applications/")
def get_demo_applications():
    """Demo applications endpoint."""
    logger.info("Demo applications endpoint called")
    return DEMO_APPLICATIONS
    return [
        {"id": 1, "company": "Demo Company", "role": "Demo Role", "status": "Applied"},
        {"id": 2, "company": "Another Demo", "role": "Demo Job", "status": "Interview"}
    ]

@app.get("/visualizations/")
def get_visualizations():
    """Visualizations endpoint."""
    logger.info("Visualizations endpoint called")
    
    # Count applications by status
    status_counts = {}
    for app in REAL_APPLICATIONS:
        status = app["status"]
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts[status] = 1
    
    # Convert to format expected by frontend
    status_data = [{"status": status, "count": count} for status, count in status_counts.items()]
    
    # Generate timeline data - applications per week for the last 12 weeks
    today = datetime.now()
    timeline_data = []
    
    for i in range(12):
        week_start = today - timedelta(days=7*i)
        week_end = week_start + timedelta(days=7)
        week_start_str = week_start.strftime("%Y-%m-%d")
        
        count = sum(1 for app in REAL_APPLICATIONS 
                   if app["application_date"] and app["application_date"] >= week_start_str 
                      and app["application_date"] < week_end.strftime("%Y-%m-%d"))
        
        timeline_data.append({
            "date": week_start_str,
            "count": count
        })
    
    # Reverse to get chronological order
    timeline_data.reverse()
    
    return {
        "status_counts": status_data,
        "timeline_data": timeline_data
    }

@app.get("/demo/visualizations/")
def get_demo_visualizations():
    """Demo visualizations endpoint."""
    logger.info("Demo visualizations endpoint called")
    
    # Count applications by status
    status_counts = {}
    for app in DEMO_APPLICATIONS:
        status = app["status"]
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts[status] = 1
    
    # Convert to format expected by frontend
    status_data = [{"status": status, "count": count} for status, count in status_counts.items()]
    
    # Generate timeline data - applications per week for the last 12 weeks
    today = datetime.now()
    timeline_data = []
    
    for i in range(12):
        week_start = today - timedelta(days=7*i)
        week_end = week_start + timedelta(days=7)
        week_start_str = week_start.strftime("%Y-%m-%d")
        
        count = sum(1 for app in DEMO_APPLICATIONS 
                   if app["application_date"] and app["application_date"] >= week_start_str 
                      and app["application_date"] < week_end.strftime("%Y-%m-%d"))
        
        timeline_data.append({
            "date": week_start_str,
            "count": count
        })
    
    # Reverse to get chronological order
    timeline_data.reverse()
    
    return {
        "status_counts": status_data,
        "timeline_data": timeline_data
    }

# Add endpoints for CRUD operations
@app.get("/applications/{app_id}")
def get_application(app_id: int):
    """Get a specific application by ID."""
    logger.info(f"Get application {app_id} called")
    for app in REAL_APPLICATIONS:
        if app["id"] == app_id:
            return app
    return {"detail": "Application not found"}

@app.get("/demo/applications/{app_id}")
def get_demo_application(app_id: int):
    """Get a specific demo application by ID."""
    logger.info(f"Get demo application {app_id} called")
    for app in DEMO_APPLICATIONS:
        if app["id"] == app_id:
            return app
    return {"detail": "Demo application not found"}

# Additional endpoints for debugging
@app.get("/debug/info")
def debug_info():
    """Return debug information about the server."""
    return {
        "server_time": datetime.now().isoformat(),
        "environment": dict(os.environ),
        "api_base": os.environ.get("VITE_API_BASE", "http://localhost:8006"),
        "data_counts": {
            "real_applications": len(REAL_APPLICATIONS),
            "demo_applications": len(DEMO_APPLICATIONS)
        }
    }

@app.get("/debug/config")
def debug_config():
    """Debug endpoint to show environment configuration."""
    return {
        "environment": dict(os.environ),
        "api_base": os.environ.get("VITE_API_BASE", "http://localhost:8006")
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8006))
    logger.info(f"Starting test server on port {port}")
    uvicorn.run(app, host="127.0.0.1", port=port)
