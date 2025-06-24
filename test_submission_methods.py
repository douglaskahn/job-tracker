import requests
import json

# Function to test different submission methods
def test_submission(endpoint, data, is_form=False):
    print(f"\n\nTesting endpoint: {endpoint}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    if is_form:
        # Submit as form data
        print("Submitting as form data")
        response = requests.post(endpoint, data=data)
    else:
        # Submit as JSON
        print("Submitting as JSON")
        response = requests.post(endpoint, json=data)
    
    print(f"Status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    
    try:
        response_json = response.json()
        print(f"Response body: {json.dumps(response_json, indent=2)}")
    except:
        print(f"Raw response: {response.text}")
    
    return response

# Test data matching what's seen in the logs
test_data = {
    "company": "Testing API Fix",
    "role": "Developer",
    "status": "Applied",
    "url": "https://example.com",
    "application_date": "",  # Empty string - problematic
    "met_with": "",
    "notes": "Test notes",
    "follow_up_required": "true",  # String for form data
    "pros": "Test pros",
    "cons": "Test cons",
    "salary": "100000"
}

# Test endpoints
base_url = "http://localhost:8005"

# 1. Test JSON endpoint with JSON data
test_submission(f"{base_url}/demo/applications/debug/", test_data)

# 2. Test form endpoint with form data
test_submission(f"{base_url}/demo/applications/", test_data, is_form=True)

# Let's try with a non-empty date to see if that works
test_data["application_date"] = "2025-06-24"
test_submission(f"{base_url}/demo/applications/", test_data, is_form=True)
