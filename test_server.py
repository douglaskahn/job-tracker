#!/usr/bin/env python3
"""
A simple FastAPI application to test the environment.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
import os
import sqlite3
from datetime import datetime
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_server")

app = FastAPI(debug=True, title="Job Tracker Test API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to log all requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    logger.info(f"Request: {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        process_time = datetime.now() - start_time
        logger.info(f"Response: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time.total_seconds():.4f}s")
        return response
    except Exception as e:
        logger.error(f"Error processing request: {request.method} {request.url.path} - Error: {str(e)}")
        raise

@app.get("/")
def read_root():
    """Root endpoint."""
    logger.info("Root endpoint called")
    return {"message": "Job Tracker API is running", "version": "Test Server 1.0"}

@app.get("/test")
def test_endpoint():
    """Test endpoint."""
    logger.info("Test endpoint called")
    return {"message": "Test endpoint working!", "timestamp": datetime.now().isoformat()}

@app.get("/applications/")
def get_applications():
    """Applications endpoint - fetches real data from database."""
    logger.info("Applications endpoint called")
    try:
        # Try to load from the real database
        applications = load_from_database("jobtracker.db", "applications")
        logger.info(f"Loaded {len(applications)} applications from real database")
        return applications
    except Exception as e:
        logger.error(f"Error loading applications from database: {str(e)}")
        # Fall back to mock data
        return [
            {"id": 1, "company": "Test Company", "role": "Test Role", "status": "Applied"},
            {"id": 2, "company": "Another Company", "role": "Another Role", "status": "Interview"}
        ]

@app.get("/demo/applications/")
def get_demo_applications():
    """Demo applications endpoint - fetches demo data from database."""
    logger.info("Demo applications endpoint called")
    try:
        # Try to load from the demo database
        applications = load_from_database("demo_jobtracker.db", "applications")
        if not applications:
            applications = load_from_database("jobtracker.db", "demo_applications")
        
        logger.info(f"Loaded {len(applications)} demo applications from database")
        return applications
    except Exception as e:
        logger.error(f"Error loading demo applications from database: {str(e)}")
        # Fall back to mock data
        return [
            {"id": 1, "company": "Demo Company", "role": "Demo Role", "status": "Applied"},
            {"id": 2, "company": "Another Demo", "role": "Demo Job", "status": "Interview"}
        ]

@app.get("/visualizations/")
def get_visualizations():
    """Visualizations endpoint."""
    logger.info("Visualizations endpoint called")
    return {
        "status_counts": [
            {"status": "Applied", "count": 10},
            {"status": "Interview", "count": 5},
            {"status": "Offer", "count": 2},
            {"status": "Rejected", "count": 3}
        ],
        "timeline_data": [
            {"date": "2025-05-01", "count": 2},
            {"date": "2025-05-15", "count": 5},
            {"date": "2025-06-01", "count": 8},
            {"date": "2025-06-15", "count": 5}
        ]
    }

@app.get("/demo/visualizations/")
def get_demo_visualizations():
    """Demo visualizations endpoint."""
    logger.info("Demo visualizations endpoint called")
    return {
        "status_counts": [
            {"status": "Applied", "count": 8},
            {"status": "Interview", "count": 4},
            {"status": "Offer", "count": 1},
            {"status": "Rejected", "count": 2}
        ],
        "timeline_data": [
            {"date": "2025-05-01", "count": 1},
            {"date": "2025-05-15", "count": 3},
            {"date": "2025-06-01", "count": 6},
            {"date": "2025-06-15", "count": 5}
        ]
    }

@app.get("/debug/config")
def debug_config():
    """Debug endpoint to show environment configuration."""
    logger.info("Debug config endpoint called")
    return {
        "environment": {k: v for k, v in os.environ.items() if not k.startswith("_")},
        "ports": {
            "backend": os.environ.get("PORT", "8006"),
            "frontend": os.environ.get("VITE_PORT", "4000")
        },
        "api_base": os.environ.get("VITE_API_BASE", "http://localhost:8006"),
        "database_files": {
            "main_exists": os.path.exists("jobtracker.db"),
            "demo_exists": os.path.exists("demo_jobtracker.db"),
            "main_size": os.path.getsize("jobtracker.db") if os.path.exists("jobtracker.db") else 0,
            "demo_size": os.path.getsize("demo_jobtracker.db") if os.path.exists("demo_jobtracker.db") else 0
        }
    }

@app.get("/debug/routes")
def debug_routes():
    """Debug endpoint to list all registered routes."""
    logger.info("Debug routes endpoint called")
    routes = []
    for route in app.routes:
        routes.append({
            "path": getattr(route, "path", "Unknown"),
            "name": getattr(route, "name", "Unknown"),
            "methods": list(getattr(route, "methods", ["Unknown"])),
            "endpoint": str(getattr(route, "endpoint", "Unknown"))
        })
    return {"routes": routes}

def load_from_database(db_path, table_name):
    """Load data from a SQLite database table."""
    if not os.path.exists(db_path):
        logger.warning(f"Database file not found: {db_path}")
        return []
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Get data
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Convert to list of dicts
        result = []
        for row in rows:
            item = {}
            for i, column in enumerate(columns):
                item[column] = row[i]
            result.append(item)
        
        return result
    except Exception as e:
        logger.error(f"Error querying database {db_path}: {str(e)}")
        return []
    finally:
        conn.close()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8006))
    logger.info(f"Starting test server on port {port}")
    uvicorn.run(app, host="127.0.0.1", port=port)
