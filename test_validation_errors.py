import requests
import json

# Test data for a minimal application
test_data = {
    "company": "Test Company Minimal",
    "role": "Test Role Minimal",
    "status": "Applied",
    "application_date": "2025-06-24"
}

# Test with form data
print("\n=== Testing with Form Data ===")
files = {}  # Empty files dict
response = requests.post(
    "http://localhost:8005/applications/",
    data=test_data,
    files=files
)
print(f"Status code: {response.status_code}")
print(f"Response: {response.text}")

# Test the demo endpoint with form data
print("\n=== Testing Demo Endpoint with Form Data ===")
response = requests.post(
    "http://localhost:8005/demo/applications/",
    data=test_data,
    files=files
)
print(f"Status code: {response.status_code}")
print(f"Response: {response.text}")

# Test the debug endpoint with JSON
print("\n=== Testing Debug Endpoint with JSON ===")
response = requests.post(
    "http://localhost:8005/demo/applications/debug/",
    json=test_data
)
print(f"Status code: {response.status_code}")
print(f"Response: {response.text}")

# Print any validation errors
if response.status_code == 422:
    try:
        error_data = response.json()
        print("\nValidation errors:")
        print(json.dumps(error_data, indent=2))
    except:
        print("Could not parse error response as JSON")
