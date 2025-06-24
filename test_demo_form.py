import requests
import json
from datetime import datetime

# Get today's date in the required format
today = datetime.now().strftime("%Y-%m-%d")

# Test basic form data submission to demo endpoint
def test_demo_form_submission():
    url = "http://localhost:8005/demo/applications/"
    
    # Very minimal form data with only required fields
    form_data = {
        "company": "Test Form Submission",
        "role": "Form Tester",
        "status": "Applied"
    }
    
    # Empty files dictionary for multipart/form-data
    files = {}
    
    print(f"Submitting to {url} with data: {form_data}")
    
    response = requests.post(url, data=form_data, files=files)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Success!")
        try:
            print(f"Response data: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Raw response: {response.text}")
    else:
        print(f"Error: {response.text}")

# Run the test
test_demo_form_submission()
