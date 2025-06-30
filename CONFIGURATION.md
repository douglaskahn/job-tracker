# Job Tracker Configuration Reference

This document lists all configuration files and locations where ports, URLs, and environment settings are defined to ensure consistency across the application.

## Port Configuration Summary

**Current Standard Ports:**
- Backend: **8005**
- Frontend: **4000**

## Configuration Files (in order of precedence)

### 1. Root Environment File
**File:** `/.env`
```properties
VITE_PORT=4000
BACKEND_PORT=8005
VITE_API_BASE=http://localhost:8005
```
**Purpose:** Main environment configuration for the entire project
**Used by:** PM2, shell scripts, and frontend build process

### 2. Frontend Environment File
**File:** `/frontend/.env`
```properties
VITE_API_BASE=http://localhost:8005
```
**Purpose:** Frontend-specific environment variables
**Used by:** Vite development server
**Note:** Overridden by root .env file if both exist

### 3. Frontend Config Module
**File:** `/frontend/src/config.js`
```javascript
const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8005';
```
**Purpose:** Centralized application configuration with fallback defaults
**Used by:** All frontend API calls and components

### 4. PM2 Configuration
**File:** `/ecosystem.config.json`
```json
{
  "apps": [
    {
      "name": "job-tracker-backend",
      "env": { "PORT": "8005" }
    },
    {
      "name": "job-tracker-frontend", 
      "env": { "VITE_API_BASE": "http://localhost:8005" }
    }
  ]
}
```
**Purpose:** Process management configuration
**Used by:** PM2 when starting services

### 5. Backend Start Script
**File:** `/start-backend.sh`
```bash
PORT=${PORT:-${BACKEND_PORT:-8005}}
```
**Purpose:** Backend startup with port configuration
**Used by:** Direct script execution and PM2

### 6. Frontend Start Script
**File:** `/start-frontend.sh`
```bash
API_BASE=${VITE_API_BASE:-http://localhost:8005}
```
**Purpose:** Frontend startup with API configuration
**Used by:** Direct script execution and PM2

### 7. Backend Main Application
**File:** `/app/main.py`
```python
port = int(os.environ.get("PORT", 8005))
```
**Purpose:** Backend application default port
**Used by:** FastAPI application when run directly

### 8. Backend CORS Configuration
**File:** `/app/main.py`
```python
allow_origins=["http://localhost:5173", "http://localhost:4000", ...]
```
**Purpose:** Allowed frontend origins for API access
**Used by:** FastAPI CORS middleware

## Configuration Precedence

When multiple configuration sources exist, the precedence order is:

1. **PM2 environment variables** (highest precedence)
2. **Root .env file** (`/.env`)
3. **Frontend .env file** (`/frontend/.env`) 
4. **Shell script defaults**
5. **Application code defaults** (lowest precedence)

## Common Configuration Issues

### Issue: Frontend still connecting to wrong port
**Cause:** Multiple .env files with conflicting values
**Solution:** Check both `/.env` and `/frontend/.env` files

### Issue: PM2 not picking up environment changes
**Cause:** PM2 caches environment variables
**Solution:** Use `pm2 restart all --update-env`

### Issue: Browser showing cached API calls
**Cause:** Browser/Vite caching old configuration
**Solution:** Hard refresh (Ctrl+F5) or restart frontend service

### Issue: Port conflicts on startup
**Cause:** Previous processes not properly terminated
**Solution:** Check with `lsof -i :PORT` and kill if needed

## Changing Ports (Checklist)

To change the backend port from 8005 to a new port:

- [ ] Update `/.env` - `BACKEND_PORT` and `VITE_API_BASE`
- [ ] Update `/frontend/.env` - `VITE_API_BASE`
- [ ] Update `/ecosystem.config.json` - both backend `PORT` and frontend `VITE_API_BASE`
- [ ] Update `/app/main.py` - default port in `if __name__ == "__main__"` section
- [ ] Update `/app/main.py` - CORS allowed origins list
- [ ] Restart both services with `pm2 restart all --update-env`
- [ ] Hard refresh browser to clear cache

To change the frontend port from 4000 to a new port:

- [ ] Update `/.env` - `VITE_PORT`
- [ ] Update `/ecosystem.config.json` - frontend environment if specified
- [ ] Update `/app/main.py` - add new port to CORS allowed origins
- [ ] Restart both services
- [ ] Access application at new URL

## Verification Commands

```bash
# Check what ports are in use
lsof -i :8005 -i :4000

# Check PM2 process status
pm2 status

# Check environment variables in browser console
import.meta.env.VITE_API_BASE

# Check PM2 logs for startup messages
pm2 logs --lines 20

# Test API connectivity
curl http://localhost:8005/applications/
```

## Notes

- Always use `pm2 restart all --update-env` after changing environment variables
- Frontend environment variables must be prefixed with `VITE_` to be accessible in the browser
- The browser console debug output in config.js shows the actual values being used
- PM2 environment variables override shell script defaults
- Hard refresh the browser after configuration changes to avoid cached values

## Scripts

### Main Scripts
| Script | Purpose |
|--------|---------|
| `start-dev.sh` | Starts both backend and frontend using PM2 |
| `start-backend.sh` | Starts only the backend API server |
| `start-frontend.sh` | Starts only the frontend development server |
| `diagnostic.sh` | Runs diagnostics on the entire application |

### Utility Scripts
| Script | Purpose |
|--------|---------|
| `init_database.py` | Initializes/resets the database |
| `test_api.py` | Mock API server for development |
| `test_connections.sh` | Tests connectivity between components |

## Port Configuration

Default ports:
- Backend API: 8006
- Frontend server: 4000

To change ports:
1. Update the `.env` file in the root directory
2. Update `frontend/.env` if changing the backend port
3. Update `ecosystem.config.json` to match

Example `.env` with custom ports:
```
BACKEND_PORT=8007
VITE_PORT=3000
VITE_API_BASE=http://localhost:8006
```

## API Endpoints

### Regular Endpoints
- `GET /applications/` - List all applications
- `POST /applications/` - Create a new application
- `GET /applications/{id}` - Get a specific application
- `PATCH /applications/{id}` - Update an application
- `DELETE /applications/{id}` - Delete an application
- `GET /visualizations/` - Get visualization data

### Demo Endpoints
- `GET /demo/applications/` - List all demo applications
- `POST /demo/applications/` - Create a new demo application
- `GET /demo/applications/{id}` - Get a specific demo application
- `PATCH /demo/applications/{id}` - Update a demo application
- `DELETE /demo/applications/{id}` - Delete a demo application
- `GET /demo/visualizations/` - Get demo visualization data

### Debug Endpoints
- `GET /` - API root (health check)
- `GET /test` - Test endpoint
- `GET /debug/info` - Debug information
- `GET /debug/config` - Configuration information

## Frontend Configuration

The frontend connects to the backend using the URL specified in `VITE_API_BASE`. 

This can be set in:
1. The root `.env` file (recommended)
2. The `frontend/.env` file (overrides root)
3. The `ecosystem.config.json` file (when using PM2)

## Database Configuration

The application uses SQLite databases:
- `jobtracker.db` - Regular mode database
- `demo_jobtracker.db` - Demo mode database

In the mock API (`test_api.py`), data is generated in memory and not persisted between restarts.

## CORS Configuration

CORS is configured in `test_api.py` to allow requests from any origin (`*`), which is suitable for development. For production, this should be restricted to specific origins.

## PM2 Process Manager

The application uses PM2 to manage processes. The configuration is in `ecosystem.config.json`.

To manually manage PM2:
```bash
# List processes
npx pm2 list

# View logs
npx pm2 logs

# Monitor processes
npx pm2 monit

# Restart processes
npx pm2 restart all

# Stop processes
npx pm2 stop all

# Kill PM2 daemon
npx pm2 kill
```
