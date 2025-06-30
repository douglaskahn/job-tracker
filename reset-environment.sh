#!/bin/bash
# reset-environment.sh - Script to reset the development environment

echo "=== Checking for processes using port 4000 (frontend) ==="
FRONTEND_PID=$(lsof -ti:4000)
if [ -n "$FRONTEND_PID" ]; then
  echo "Killing process $FRONTEND_PID using port 4000"
  kill -9 $FRONTEND_PID
else
  echo "No process found using port 4000"
fi

echo "=== Checking for processes using port 8005 (backend) ==="
BACKEND_PID=$(lsof -ti:8005)
if [ -n "$BACKEND_PID" ]; then
  echo "Killing process $BACKEND_PID using port 8005"
  kill -9 $BACKEND_PID
else
  echo "No process found using port 8005"
fi

echo "=== Clearing environment variables ==="
unset FRONTEND_URL
unset BACKEND_URL
unset VITE_API_BASE

echo "=== Installing dependencies ==="
cd /Users/douglaskahn/Documents/job-tracker
# Check if Python virtual environment exists and activate it
if [ -d "env" ]; then
  echo "Activating Python virtual environment"
  source env/bin/activate
  echo "Installing Python dependencies"
  pip install -r requirements.txt
fi

# Check if there's a frontend directory with package.json
if [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
  echo "Installing frontend dependencies"
  cd frontend
  npm install
  cd ..
fi

echo "=== Environment reset complete ==="
echo "You can now start the backend with: ./start-backend.sh"
echo "And the frontend with: ./start-frontend.sh"
