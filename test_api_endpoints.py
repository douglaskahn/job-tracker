import requests
import json

# Test API endpoints
def test_api_endpoint(url, method="GET", data=None):
    print(f"\nTesting {method} {url}")
    
    if method == "GET":
        response = requests.get(url)
    elif method == "POST" and data:
        response = requests.post(url, json=data)
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        try:
            result = response.json()
            if isinstance(result, list):
                print(f"Received {len(result)} items")
            else:
                print("Received data successfully")
            return True
        except:
            print("Could not parse response as JSON")
            return False
    else:
        print(f"Error response: {response.text}")
        return False

# Base URL
base_url = "http://localhost:8005"

# Test regular applications endpoint
real_success = test_api_endpoint(f"{base_url}/applications/")

# Test demo applications endpoint
demo_success = test_api_endpoint(f"{base_url}/demo/applications/")

# Create a test application in demo mode
test_data = {
    "company": "API Test Company",
    "role": "API Test Role",
    "status": "Applied",
    "application_date": "2025-06-24"
}

create_success = test_api_endpoint(
    f"{base_url}/demo/applications/debug/", 
    method="POST", 
    data=test_data
)

# Print summary
print("\n=== Test Summary ===")
print(f"Real applications API: {'✅ Working' if real_success else '❌ Failed'}")
print(f"Demo applications API: {'✅ Working' if demo_success else '❌ Failed'}")
print(f"Create demo application: {'✅ Working' if create_success else '❌ Failed'}")
