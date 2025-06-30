#!/usr/bin/env python3
"""
Test script to debug the resume upload modal bug.
This script will test the file upload functionality for both normal and demo modes.
"""

import requests
import json
import os

API_BASE = "http://localhost:8005"

def test_file_upload():
    """Test file upload functionality"""
    print("Testing file upload functionality...")
    
    # Test with a real application
    app_id = 55  # From the response above, this app has files
    
    # Create a small test file
    test_file_content = b"This is a test file content for resume upload testing."
    test_file_name = "test_resume.txt"
    
    # Test normal mode
    print(f"\n1. Testing normal mode file upload for application {app_id}")
    try:
        files = {'file': (test_file_name, test_file_content, 'text/plain')}
        response = requests.post(
            f"{API_BASE}/applications/{app_id}/files/resume",
            files=files,
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Normal mode file upload successful")
        else:
            print(f"❌ Normal mode file upload failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Normal mode file upload error: {str(e)}")
    
    # Test demo mode
    print(f"\n2. Testing demo mode file upload")
    demo_apps_response = requests.get(f"{API_BASE}/demo/applications/")
    if demo_apps_response.status_code == 200:
        demo_apps = demo_apps_response.json()
        if demo_apps:
            demo_app_id = demo_apps[0]['id']
            print(f"Using demo application {demo_app_id}")
            
            try:
                files = {'file': (test_file_name, test_file_content, 'text/plain')}
                response = requests.post(
                    f"{API_BASE}/demo/applications/{demo_app_id}/files/resume",
                    files=files,
                    timeout=10
                )
                print(f"Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                
                if response.status_code == 200:
                    print("✅ Demo mode file upload successful")
                else:
                    print(f"❌ Demo mode file upload failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Demo mode file upload error: {str(e)}")
        else:
            print("No demo applications found")
    else:
        print(f"Failed to get demo applications: {demo_apps_response.status_code}")
    
    # Test file validation
    print(f"\n3. Testing file validation (large file)")
    try:
        large_content = b"x" * (6 * 1024 * 1024)  # 6MB file (should exceed limit)
        files = {'file': ('large_file.txt', large_content, 'text/plain')}
        response = requests.post(
            f"{API_BASE}/applications/{app_id}/files/resume",
            files=files,
            timeout=10
        )
        print(f"Large file status: {response.status_code}")
        print(f"Large file response: {response.text[:200]}...")
        
        if response.status_code == 400:
            print("✅ File size validation working correctly")
        else:
            print(f"⚠️  File size validation may not be working: {response.status_code}")
            
    except Exception as e:
        print(f"❌ File validation test error: {str(e)}")

def test_application_endpoints():
    """Test basic application endpoints"""
    print("\nTesting basic application endpoints...")
    
    # Test normal applications
    try:
        response = requests.get(f"{API_BASE}/applications/", timeout=5)
        if response.status_code == 200:
            apps = response.json()
            print(f"✅ Normal mode: Found {len(apps)} applications")
        else:
            print(f"❌ Normal mode endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Normal mode endpoint error: {str(e)}")
    
    # Test demo applications
    try:
        response = requests.get(f"{API_BASE}/demo/applications/", timeout=5)
        if response.status_code == 200:
            demo_apps = response.json()
            print(f"✅ Demo mode: Found {len(demo_apps)} applications")
        else:
            print(f"❌ Demo mode endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Demo mode endpoint error: {str(e)}")

if __name__ == "__main__":
    print("🔍 Debugging Resume Upload Modal Bug")
    print("=" * 50)
    
    test_application_endpoints()
    test_file_upload()
    
    print("\n" + "=" * 50)
    print("Test completed. Check the results above for any issues.")
