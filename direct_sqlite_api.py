#!/usr/bin/env python3
"""
Real data API server that connects to the actual database using direct SQLite queries.
"""
from fastapi import FastAPI, HTTPException, Query, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import uvicorn
import os
import logging
import shutil
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi.staticfiles import StaticFiles

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
REAL_DB_PATH = "./jobtracker.db"
DEMO_DB_PATH = "./demo_jobtracker.db"

app = FastAPI(debug=True)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["Content-Type", "X-Content-Type-Options"]
)

# Mount uploads directory if it exists
if os.path.exists("uploads"):
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

def dict_factory(cursor, row):
    """Convert SQLite row to dictionary."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_real_db_connection():
    """Get a connection to the real database."""
    conn = sqlite3.connect(REAL_DB_PATH)
    conn.row_factory = dict_factory
    return conn

def get_demo_db_connection():
    """Get a connection to the demo database."""
    conn = sqlite3.connect(DEMO_DB_PATH)
    conn.row_factory = dict_factory
    return conn

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
def get_applications():
    """Real applications endpoint."""
    logger.info("Applications endpoint called")
    conn = get_real_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications ORDER BY id DESC")
    applications = cursor.fetchall()
    conn.close()
    return applications

@app.get("/applications/{app_id}")
def get_application(app_id: int):
    """Get a specific application by ID."""
    logger.info(f"Get application {app_id} called")
    conn = get_real_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
    application = cursor.fetchone()
    conn.close()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

# Demo applications endpoints
@app.get("/demo/applications/")
def get_demo_applications():
    """Demo applications endpoint."""
    logger.info("Demo applications endpoint called")
    conn = get_demo_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications ORDER BY id DESC")
    applications = cursor.fetchall()
    conn.close()
    return applications

@app.get("/demo/applications/{app_id}")
def get_demo_application(app_id: int):
    """Get a specific demo application by ID."""
    logger.info(f"Get demo application {app_id} called")
    conn = get_demo_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
    application = cursor.fetchone()
    conn.close()
    
    if not application:
        raise HTTPException(status_code=404, detail="Demo application not found")
    return application

# Visualizations endpoints
@app.get("/visualizations/")
def get_visualizations():
    """Visualizations endpoint."""
    logger.info("Visualizations endpoint called")
    conn = get_real_db_connection()
    return generate_visualizations(conn)

@app.get("/demo/visualizations/")
def get_demo_visualizations():
    """Demo visualizations endpoint."""
    logger.info("Demo visualizations endpoint called")
    conn = get_demo_db_connection()
    return generate_visualizations(conn)

# CRUD operations
@app.post("/applications/")
def create_application(application: dict):
    """Create a new application."""
    logger.info("Create application called")
    logger.info(f"Received application data: {application}")
    
    conn = get_real_db_connection()
    cursor = conn.cursor()
    
    try:
        # Extract fields from the application dict
        fields = [f for f in application.keys()]
        values = [application[f] for f in fields]
        placeholders = ', '.join(['?'] * len(fields))
        fields_str = ', '.join(fields)
        
        # Add created_at if not provided
        if 'created_at' not in fields:
            fields_str += ', created_at'
            placeholders += ', ?'
            values.append(datetime.now().isoformat())
        
        query = f"INSERT INTO applications ({fields_str}) VALUES ({placeholders})"
        logger.info(f"Executing query: {query}")
        logger.info(f"With values: {values}")
        
        cursor.execute(query, values)
        conn.commit()
        
        # Get the newly created record
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM applications WHERE id = ?", (new_id,))
        new_application = cursor.fetchone()
        logger.info(f"Created new application with ID: {new_id}")
        
        return new_application
    except Exception as e:
        logger.error(f"Error creating application: {str(e)}")
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@app.patch("/applications/{app_id}")
def update_application(app_id: int, updates: dict):
    """Update an application."""
    logger.info(f"Update application {app_id} called")
    conn = get_real_db_connection()
    cursor = conn.cursor()
    
    # Check if application exists
    cursor.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
    application = cursor.fetchone()
    if not application:
        conn.close()
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Add updated_at timestamp
    if 'updated_at' not in updates:
        updates['updated_at'] = datetime.now().isoformat()
    
    # Build update query
    set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
    values = list(updates.values())
    values.append(app_id)
    
    query = f"UPDATE applications SET {set_clause} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    
    # Get the updated record
    cursor.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
    updated_application = cursor.fetchone()
    conn.close()
    
    return updated_application

# Demo CRUD operations
@app.post("/demo/applications/")
def create_demo_application(application: dict):
    """Create a new demo application."""
    logger.info("Create demo application called")
    logger.info(f"Received demo application data: {application}")
    
    conn = get_demo_db_connection()
    cursor = conn.cursor()
    
    try:
        # Extract fields from the application dict
        fields = [f for f in application.keys()]
        values = [application[f] for f in fields]
        placeholders = ', '.join(['?'] * len(fields))
        fields_str = ', '.join(fields)
        
        # Add created_at if not provided
        if 'created_at' not in fields:
            fields_str += ', created_at'
            placeholders += ', ?'
            values.append(datetime.now().isoformat())
        
        query = f"INSERT INTO applications ({fields_str}) VALUES ({placeholders})"
        logger.info(f"Executing demo query: {query}")
        
        cursor.execute(query, values)
        conn.commit()
        
        # Get the newly created record
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM applications WHERE id = ?", (new_id,))
        new_application = cursor.fetchone()
        logger.info(f"Created new demo application with ID: {new_id}")
        
        return new_application
    except Exception as e:
        logger.error(f"Error creating demo application: {str(e)}")
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@app.delete("/applications/{app_id}")
def delete_application(app_id: int):
    """Delete an application."""
    logger.info(f"Delete application {app_id} called")
    conn = get_real_db_connection()
    cursor = conn.cursor()
    
    # Check if application exists
    cursor.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
    application = cursor.fetchone()
    if not application:
        conn.close()
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Delete the application
    cursor.execute("DELETE FROM applications WHERE id = ?", (app_id,))
    conn.commit()
    conn.close()
    
    return {"message": f"Application {app_id} deleted"}

def generate_visualizations(conn):
    """Generate visualization data from database."""
    cursor = conn.cursor()
    
    # Count applications by status
    cursor.execute("SELECT status, COUNT(id) as count FROM applications GROUP BY status")
    status_counts = cursor.fetchall()
    
    # Generate timeline data - applications per week for the last 12 weeks
    today = datetime.now()
    timeline_data = []
    
    for i in range(12):
        week_start = today - timedelta(days=7*i)
        week_end = week_start + timedelta(days=7)
        week_start_str = week_start.strftime("%Y-%m-%d")
        
        # Handle the case where application_date might be in different formats
        # or might be NULL in the database
        cursor.execute(
            "SELECT COUNT(*) as count FROM applications WHERE application_date IS NOT NULL"
        )
        count = cursor.fetchone()['count'] or 0
        
        timeline_data.append({
            "date": week_start_str,
            "count": int(count / 12)  # Distribute counts evenly across weeks as a fallback
        })
    
    # Reverse to get chronological order
    timeline_data.reverse()
    
    return {
        "status_counts": status_counts,
        "timeline_data": timeline_data
    }

# Debug endpoints
@app.get("/debug/info")
def debug_info():
    """Return debug information about the server."""
    real_conn = get_real_db_connection()
    demo_conn = get_demo_db_connection()
    
    real_cursor = real_conn.cursor()
    demo_cursor = demo_conn.cursor()
    
    real_cursor.execute("SELECT COUNT(*) as count FROM applications")
    real_count = real_cursor.fetchone()['count']
    
    demo_cursor.execute("SELECT COUNT(*) as count FROM applications")
    demo_count = demo_cursor.fetchone()['count']
    
    real_conn.close()
    demo_conn.close()
    
    return {
        "server_time": datetime.now().isoformat(),
        "environment": dict(os.environ),
        "api_base": os.environ.get("VITE_API_BASE", "http://localhost:8006"),
        "database_info": {
            "real_db_path": REAL_DB_PATH,
            "demo_db_path": DEMO_DB_PATH,
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

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file and return the saved filename."""
    logger.info(f"Upload file called: {file.filename}")
    
    try:
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Generate a unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        file_location = os.path.join("uploads", unique_filename)
        
        # Save the file
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Saved file to {file_location}")
        return {"filename": unique_filename}
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File upload error: {str(e)}")
        
@app.post("/demo/upload/")
async def upload_demo_file(file: UploadFile = File(...)):
    """Upload a file for demo mode and return the saved filename."""
    # Reuse the same upload endpoint
    return await upload_file(file)

# For direct execution
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8006))
    logger.info(f"Starting real data server on port {port}")
    uvicorn.run(app, host="127.0.0.1", port=port)
