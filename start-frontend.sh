#!/bin/bash
cd /Users/douglaskahn/Documents/job-tracker/frontend

# Load environment variables from .env file if it exists
if [ -f "../.env" ]; then
  export $(grep -v '^#' ../.env | xargs)
fi

# Use PM2 environment variable or default to 8005
API_BASE=${VITE_API_BASE:-http://localhost:8005}
export VITE_API_BASE=$API_BASE

echo "Starting frontend on port ${VITE_PORT:-4000}, connecting to API at $API_BASE..."

# Force a specific host and port for consistency
# Use --strictPort to ensure Vite fails if the port is unavailable rather than trying another port
npm run dev -- --host localhost --port ${VITE_PORT:-4000} --strictPort
