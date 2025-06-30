# Troubleshooting Guide

This document provides detailed steps for diagnosing and fixing common issues with the Job Tracker application.

## Startup Issues

### Application Won't Start

**Symptoms:** Running `./start-dev.sh` fails or doesn't start the components correctly.

**Steps to diagnose:**
1. Check for port conflicts:
   ```bash
   lsof -i :8006  # Check if backend port is in use
   lsof -i :4000  # Check if frontend port is in use
   ```

2. Check if PM2 is already running:
   ```bash
   npx pm2 list
   ```

3. Check for error messages in the startup logs:
   ```bash
   cat ~/.pm2/logs/job-tracker-backend-error.log
   cat ~/.pm2/logs/job-tracker-frontend-error.log
   ```

**Fixes:**
1. Kill processes using the required ports:
   ```bash
   lsof -i :8006 | grep LISTEN | awk '{print $2}' | xargs kill -9
   lsof -i :4000 | grep LISTEN | awk '{print $2}' | xargs kill -9
   ```

2. Reset PM2:
   ```bash
   npx pm2 stop all
   npx pm2 kill
   ```

3. Ensure environment files are correct:
   ```bash
   # Root .env should contain:
   echo "BACKEND_PORT=8006
   VITE_PORT=4000
   VITE_API_BASE=http://localhost:8006" > .env
   
   # Frontend .env should contain:
   echo "VITE_API_BASE=http://localhost:8006" > frontend/.env
   ```

## Data Loading Issues

### No Data Appears in the Application

**Symptoms:** UI loads but shows no job applications data or shows errors in the console.

**Steps to diagnose:**
1. Check if backend API is responding:
   ```bash
   curl http://localhost:8006/applications/
   curl http://localhost:8006/demo/applications/
   ```

2. Check browser network tab for API errors (404, CORS, etc.)

3. Check if frontend is using the correct API URL:
   ```bash
   grep -r "VITE_API_BASE" frontend/
   ```

**Fixes:**
1. Ensure backend is running and serving data:
   ```bash
   ./start-backend.sh
   ```

2. Update frontend configuration if needed:
   ```bash
   echo "VITE_API_BASE=http://localhost:8006" > frontend/.env
   ```

3. Restart frontend:
   ```bash
   cd frontend && npm run dev
   ```

### Visualizations Not Loading

**Symptoms:** Application data loads but charts/visualizations are missing or show errors.

**Steps to diagnose:**
1. Check if visualization endpoints are working:
   ```bash
   curl http://localhost:8006/visualizations/
   curl http://localhost:8006/demo/visualizations/
   ```

2. Check browser console for specific error messages

**Fixes:**
1. If endpoints return 404, check if they're defined in `test_api.py`
2. Ensure frontend is using the correct API URL

## CORS Issues

**Symptoms:** Browser console shows CORS errors when making API requests.

**Steps to diagnose:**
1. Check if CORS headers are set correctly:
   ```bash
   curl -I -X OPTIONS -H "Origin: http://localhost:4000" \
     -H "Access-Control-Request-Method: GET" \
     http://localhost:8006/applications/
   ```

2. Check if frontend is using the correct protocol (http vs https)

**Fixes:**
1. Ensure CORS middleware is configured in the backend:
   ```python
   # In test_api.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # For development only
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. Make sure frontend is using the correct URL format

## Port Conflicts

**Symptoms:** Server fails to start with "address already in use" errors.

**Steps to diagnose:**
1. Identify which processes are using the ports:
   ```bash
   lsof -i :8006
   lsof -i :4000
   ```

**Fixes:**
1. Kill the conflicting processes:
   ```bash
   # By PID
   kill -9 <PID>
   
   # Or by pattern
   pkill -f "python test_api.py"
   pkill -f "node.*vite"
   ```

2. Change ports if necessary:
   - Update `.env` file with different ports
   - Update `ecosystem.config.json` to match

## Database Issues

**Symptoms:** API returns database errors or empty data.

**Steps to diagnose:**
1. Check if database files exist:
   ```bash
   ls -la jobtracker.db demo_jobtracker.db
   ```

2. Check database content (if using SQLite):
   ```bash
   sqlite3 jobtracker.db "SELECT count(*) FROM applications;"
   ```

**Fixes:**
1. Initialize/reset database if needed:
   ```bash
   python init_database.py
   ```

2. Restore from backup if available:
   ```bash
   cp jobtracker.db.bak jobtracker.db
   ```

## Complete Reset

If all else fails, here's how to completely reset the application:

```bash
# Stop all processes
npx pm2 stop all
npx pm2 kill
pkill -f "python test_api.py"
pkill -f "node.*vite"

# Reset configuration
echo "BACKEND_PORT=8006
VITE_PORT=4000
VITE_API_BASE=http://localhost:8006" > .env
echo "VITE_API_BASE=http://localhost:8006" > frontend/.env

# Start fresh
./start-dev.sh
```

## Running Diagnostics

A comprehensive diagnostic script is available:

```bash
chmod +x diagnostic.sh
./diagnostic.sh
```

This will check:
- Environment variables
- Port usage
- Running processes
- API endpoints
- CORS configuration
- Application logs

## Getting Help

If you're still having issues:
1. Check the restoration logs in the `restoration-logs/` directory
2. Review the mockup data configuration in `MOCK_DATA_GUIDE.md`
3. Check the application architecture in `ARCHITECTURE.md`
