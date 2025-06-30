# Job Tracker Application

A full-stack application for tracking job applications with a FastAPI backend and React frontend.

## Quick Start

1. **Set up environment variables**:
   ```bash
   # Create or update .env file in the root directory
   echo "BACKEND_PORT=8006
   VITE_PORT=4000
   VITE_API_BASE=http://localhost:8006" > .env
   ```

2. **Start the application**:
   ```bash
   # Run the full application (backend and frontend)
   ./start-dev.sh
   
   # Or start components individually:
   # Backend only
   ./start-backend.sh
   # Frontend only
   ./start-frontend.sh
   ```

3. **Access the application**:
   - Frontend: http://localhost:4000
   - Backend API: http://localhost:8006
   - API Documentation: http://localhost:8006/docs

## Demo Mode

The application supports a demo mode that displays sample data instead of real job application data.

1. **Toggle Demo Mode**:
   - Click the "Demo Mode" toggle in the top-right corner of the application
   - This will switch between real data (`jobtracker.db`) and demo data (`demo_jobtracker.db`)

2. **Repopulate Demo Database**:
   - If you need to reset the demo database with fresh sample data:
   ```bash
   # Repopulate the demo database with sample data
   ./populate_demo_db.py
   ```
   - See [DEMO_MAINTENANCE.md](./DEMO_MAINTENANCE.md) for more information

## Environment Configuration

### Port Configuration
- Backend: 8006 (configurable via BACKEND_PORT in .env)
- Frontend: 4000 (configurable via VITE_PORT in .env)

### Configuration Files
- `.env`: Root environment variables
- `frontend/.env`: Frontend-specific variables
- `ecosystem.config.json`: PM2 process configuration
- `start-backend.sh`: Backend startup script
- `start-frontend.sh`: Frontend startup script
- `start-dev.sh`: Combined startup script using PM2

### Database
- `jobtracker.db`: Main SQLite database
- `demo_jobtracker.db`: Demo SQLite database
- `init_database.py`: Script to reset and populate databases with sample data

To initialize or reset the databases with sample data:
```bash
python init_database.py
```

## Architecture

- **Backend**: FastAPI application in `app/` and `backend/` directories
  - **Main API**: `real_data_api.py` serves data from the SQLite database
  - **Database**: SQLite database (jobtracker.db, demo_jobtracker.db)
- **Frontend**: React application in `frontend/` directory

## Uploading a Spreadsheet

To upload a spreadsheet and populate the database:

1. Place your `.xlsx` file in a known location.
2. Update the `file_path` variable in `app/upload_spreadsheet.py` with the path to your file.
3. Run the script:
   ```bash
   python app/upload_spreadsheet.py
   ```
4. Ensure the spreadsheet columns match the database model fields.

## Troubleshooting Guide

### Common Issues

1. **Port conflicts**:
   ```bash
   # Check if ports are already in use
   lsof -i :8006  # Check backend port
   lsof -i :4000  # Check frontend port
   
   # Kill processes using those ports
   lsof -i :8006 | grep LISTEN | awk '{print $2}' | xargs kill -9
   lsof -i :4000 | grep LISTEN | awk '{print $2}' | xargs kill -9
   ```

2. **404 Errors on API endpoints**:
   - Verify backend is running: `curl http://localhost:8006/`
   - Check endpoint exists: `curl http://localhost:8006/applications/`
   - Verify frontend configuration: Check VITE_API_BASE in frontend/.env

3. **CORS errors**:
   - Ensure backend CORS middleware is configured correctly in test_api.py
   - Verify frontend is making requests to the correct URL

4. **Application not loading data**:
   - Check backend logs: `npx pm2 logs job-tracker-backend`
   - Check frontend logs: `npx pm2 logs job-tracker-frontend`
   - Run diagnostic script: `./diagnostic.sh`

### Diagnostic Tools

A comprehensive diagnostic script is available to check the health of all components:

```bash
# Run the diagnostic script
chmod +x diagnostic.sh
./diagnostic.sh
```

This script checks:
- Environment variables
- Port usage
- Running processes
- API endpoints
- CORS configuration
- Application logs

### Reset Process

If you need to completely reset the application:

```bash
# Stop all processes
npx pm2 stop all
npx pm2 kill

# Kill any remaining processes
pkill -f "python real_data_api.py"
pkill -f "node.*vite"

# Reset database with sample data
python init_database.py

# Restart with clean state
./start-dev.sh
```

## Restoration Logs

For detailed information about fixes applied to the system, see the restoration logs:
- `restoration-logs/JOB_TRACKER_RESTORATION.md`: Initial restoration process
- `restoration-logs/DATA_LOADING_FIX.md`: Data loading issues fixed
- `restoration-logs/VISUALIZATION_DATA_FIX.md`: Visualization rendering fixed
- `restoration-logs/REAL_DATA_IMPLEMENTATION.md`: Migration from mock to real data

## Further Documentation

- `functional-requirements.md`: Functional and technical requirements
- `ARCHITECTURE.md`: System architecture
- `CONFIGURATION.md`: Detailed configuration guide
- `TROUBLESHOOTING.md`: Comprehensive troubleshooting guide
- `MOCK_DATA_GUIDE.md`: Documentation on the mock data system
- `diagnostic.sh`: Interactive diagnostic tool for system health checks
- `DEMO_MAINTENANCE.md`: Instructions for maintaining and restoring the demo database
