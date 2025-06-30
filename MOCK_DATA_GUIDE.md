# Mock Data Setup & Configuration

This document explains how the mock data system works in the Job Tracker application and how to modify it for testing or development purposes.

## Overview

The application uses a test API server (`test_api.py`) that provides mock data for both regular and demo modes. This allows for development and testing without needing a real database.

## How Mock Data Works

1. The `test_api.py` file contains a FastAPI server that:
   - Generates realistic application data
   - Provides endpoints for both regular and demo modes
   - Generates visualization data based on the mock applications
   - Provides CRUD endpoints for manipulating the data

2. Data generation happens in the `generate_application_data()` function, which:
   - Creates a specified number of job applications
   - Assigns random values for company names, roles, statuses, etc.
   - Uses different prefixes for demo vs. regular data

## Modifying Mock Data

### Changing the Amount of Data

In `test_api.py`, find these lines:

```python
# Cache the generated data
REAL_APPLICATIONS = generate_application_data(40, is_demo=False)
DEMO_APPLICATIONS = generate_application_data(30, is_demo=True)
```

Adjust the numbers (40 and 30) to change how many mock applications are generated.

### Customizing Data Types

To modify the types of data generated, edit the lists in the `generate_application_data()` function:

```python
companies = [
    f"{prefix}Tech", f"{prefix}Corp", f"{prefix}Global", f"{prefix}Innovations", 
    # Add your custom company names here
]
    
roles = [
    "Software Engineer", "Frontend Developer", "Backend Developer", 
    # Add your custom role names here
]
    
statuses = [
    "Not Yet Applied", "Applied", "Phone Screen", "Technical Interview", 
    # Add your custom statuses here
]
```

### Changing Data Structure

If you need to modify the structure of each application object, edit the dictionary creation:

```python
application = {
    "id": i,
    "company": f"{company} {i}",
    # Add or modify fields here
}
```

## Visualization Data

The mock visualization data is generated dynamically based on the application data:

1. **Status counts**: Calculated by counting applications in each status
2. **Timeline data**: Generated for the past 12 weeks based on application dates

To modify visualization data generation, edit the `/visualizations/` and `/demo/visualizations/` endpoint handlers.

## Switching to Real Data

When you're ready to switch from mock data to a real database:

1. Replace the endpoints in `test_api.py` with ones that connect to a real database
2. OR modify the `start-backend.sh` script to use a different Python file

## Testing Mock Endpoints

Use curl to test if the mock endpoints are working:

```bash
# Test applications endpoint
curl http://localhost:8006/applications/

# Test demo applications endpoint
curl http://localhost:8006/demo/applications/

# Test visualizations endpoint
curl http://localhost:8006/visualizations/

# Test demo visualizations endpoint
curl http://localhost:8006/demo/visualizations/
```

## Troubleshooting

If mock data isn't loading properly:

1. Verify the server is running: `curl http://localhost:8006/`
2. Check for errors in the server logs: `npx pm2 logs job-tracker-backend`
3. Ensure the frontend is configured to use the correct API base URL
4. Run the diagnostic script: `./diagnostic.sh`
