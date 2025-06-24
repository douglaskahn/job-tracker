import requests
import json

# Test application data
test_data = {
    "company": "Test Company",
    "role": "Test Role",
    "status": "Applied",
    "url": "https://example.com",
    "application_date": "2025-06-24",
    "met_with": "Test Person",
    "notes": "Test notes",
    "pros": "Test pros",
    "cons": "Test cons",
    "salary": "100000",
    "follow_up_required": False
}

# Test direct JSON endpoint
response = requests.post(
    "http://localhost:8005/demo/applications/debug/",
    json=test_data
)

print(f"Status code: {response.status_code}")
print(f"Response body: {response.text}")

if response.status_code == 200:
    print("Success! The application was created.")
else:
    print(f"Error: {response.status_code}")
    try:
        error_detail = response.json()
        print(f"Error detail: {json.dumps(error_detail, indent=2)}")
    except:
        print("Could not parse error response as JSON")
