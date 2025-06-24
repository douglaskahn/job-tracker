import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_demo_applications_endpoint():
    """Test that the demo applications endpoint returns a list of applications"""
    response = client.get("/demo/applications/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    # Check that we have demo data
    assert len(response.json()) > 0
    
    # Check that the first application has the expected structure
    app = response.json()[0]
    assert "id" in app
    assert "company" in app
    assert "role" in app
    assert "status" in app

def test_demo_visualizations_endpoint():
    """Test that the demo visualizations endpoint returns visualization data"""
    response = client.get("/demo/visualizations/")
    assert response.status_code == 200
    
    # Check the structure of the response
    data = response.json()
    assert "overTime" in data
    assert "statusDistribution" in data
    assert "calendar" in data
    
    # Check that overTime has the expected structure
    assert "labels" in data["overTime"]
    assert "datasets" in data["overTime"]
    
    # Check that statusDistribution has the expected structure
    assert "labels" in data["statusDistribution"]
    assert "datasets" in data["statusDistribution"]

def test_demo_create_application():
    """Test creating a demo application"""
    test_data = {
        "company": "Test Company",
        "role": "Test Role",
        "status": "Applied",
        "url": "https://example.com",
        "application_date": "2025-06-01",
        "follow_up_required": False
    }
    
    response = client.post("/demo/applications/", data=test_data)
    assert response.status_code == 200
    
    # Check that the created application has the expected data
    created_app = response.json()
    assert created_app["company"] == "Test Company"
    assert created_app["role"] == "Test Role"
    assert created_app["status"] == "Applied"
    
    # Clean up - delete the created application
    app_id = created_app["id"]
    delete_response = client.delete(f"/demo/applications/{app_id}")
    assert delete_response.status_code == 200
