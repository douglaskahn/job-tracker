import requests
import json

# Test application data matching what's seen in the logs
test_data = {
    "company": "Testing 1223",
    "role": "Job Title",
    "status": "Offer",
    "url": "https://mui.com/store/items/soft-ui-pro-dashboard/",
    "application_date": "",  # Empty string - this might be causing issues
    "met_with": "",
    "notes": "Some notes here",
    "resume_file": "",
    "cover_letter_file": "",
    "follow_up_required": True,
    "pros": "Porset",
    "cons": "Conset",
    "salary": "8999999"
}

# Test direct JSON endpoint
response = requests.post(
    "http://localhost:8005/demo/applications/debug/",
    json=test_data
)

print(f"Status code: {response.status_code}")
print(f"Response headers: {response.headers}")
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
