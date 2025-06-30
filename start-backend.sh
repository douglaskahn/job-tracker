#!/bin/bash
cd /Users/douglaskahn/Documents/job-tracker

# Activate the virtual environment
if [ -d "env/bin" ]; then
  source env/bin/activate
fi

# Load environment variables from .env file if it exists
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Use the environment variable or default to 8005
PORT=${PORT:-${BACKEND_PORT:-8005}}
export PORT

echo "Starting backend with real data on port $PORT..."

# Kill any existing processes on this port
lsof -i :$PORT | grep LISTEN | awk '{print $2}' | xargs kill -9 2>/dev/null || true
pkill -f "python real_data_api.py" || true
pkill -f "python direct_sqlite_api.py" || true
pkill -f "python test_api.py" || true
pkill -f "python app/main.py" || true
pkill -f "uvicorn.run.*port=$PORT" || true

# Wait a moment for the port to be released
sleep 2

# Run the app/main.py using FastAPI with SQLAlchemy ORM (original implementation)
cd /Users/douglaskahn/Documents/job-tracker
PYTHONPATH=/Users/douglaskahn/Documents/job-tracker python app/main.py
