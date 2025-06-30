# Demo Database Maintenance Guide

This document provides instructions for maintaining, resetting, and restoring the demo database for the Job Tracker application.

## Overview

The Job Tracker application supports two modes:
1. **Real Mode**: Uses `jobtracker.db` to store actual job application data
2. **Demo Mode**: Uses `demo_jobtracker.db` to display sample data for demonstration purposes

## Demo Database Files

- **Main Demo DB**: `demo_jobtracker.db`
- **Backup Demo DB**: `demo_jobtracker.db.bak`

## Repopulating the Demo Database

If the demo database becomes corrupted or you need to reset it with fresh sample data, follow these steps:

### Option 1: Use the populate_demo_db.py Script (Recommended)

The `populate_demo_db.py` script will generate realistic sample data and populate the demo database:

```bash
# Make the script executable if needed
chmod +x ./populate_demo_db.py

# Run the script
./populate_demo_db.py
```

This will:
1. Clear all existing data in the demo database
2. Generate 50 sample job applications with varied statuses, dates, and details
3. Insert the sample data into the demo database

### Option 2: Restore from Backup

If you need to restore from the backup:

```bash
# Make a backup of the current demo database (optional)
cp demo_jobtracker.db demo_jobtracker.db.old

# Restore from backup
cp demo_jobtracker.db.bak demo_jobtracker.db
```

## Verifying Demo Data

After repopulating the demo database, verify that it's working correctly:

1. Ensure the backend server is running:
   ```bash
   ./start-backend.sh
   ```

2. Test the demo endpoints:
   ```bash
   # Test demo applications endpoint
   curl http://localhost:8006/demo/applications/1

   # Test demo visualizations endpoint
   curl http://localhost:8006/demo/visualizations/
   ```

3. Open the frontend in a browser and toggle to Demo Mode to verify the data is displayed correctly.

## Customizing Demo Data

To customize the demo data, you can modify the `populate_demo_db.py` script:

1. Edit the `create_demo_application()` function to change the data structure
2. Add more variety to company names, roles, statuses, etc.
3. Adjust the number of demo applications by changing the range in the `populate_demo_database()` function

## Creating Backup of Demo Database

It's good practice to create regular backups of the demo database:

```bash
cp demo_jobtracker.db demo_jobtracker.db.bak
```

## Troubleshooting

If you encounter issues with the demo database:

1. **Database Lock Error**: If you get a database lock error, make sure no other process is using the database:
   ```bash
   lsof | grep demo_jobtracker.db
   ```

2. **Empty Demo Data**: If the demo mode shows no data, run the populate script again:
   ```bash
   ./populate_demo_db.py
   ```

3. **Server Errors**: If the server returns errors when accessing demo endpoints, check the backend logs and ensure the database schema is correct.

## Backend API Endpoints for Demo Mode

The following API endpoints are available for demo mode:

- **List Demo Applications**: GET `http://localhost:8006/demo/applications/`
- **Get Demo Application**: GET `http://localhost:8006/demo/applications/{id}`
- **Demo Visualizations**: GET `http://localhost:8006/demo/visualizations/`
