#!/bin/bash
echo "Stopping any existing processes..."
pkill -f "python test_api.py" || true
pkill -f "uvicorn" || true
sleep 1

echo "Starting test API server on port 8006..."
source env/bin/activate
export PORT=8006
python test_api.py
