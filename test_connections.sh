#!/bin/bash
# test_connections.sh - Test connectivity between frontend and backend

echo "=== Testing API Endpoints ==="
echo "Testing root endpoint..."
curl -s http://localhost:8006/ | jq .

echo "Testing applications endpoint..."
curl -s http://localhost:8006/applications/ | jq '. | length'

echo "Testing demo applications endpoint..."
curl -s http://localhost:8006/demo/applications/ | jq '. | length'

echo "Testing visualizations endpoint..."
curl -s http://localhost:8006/visualizations/ | jq .status_counts

echo "Testing demo visualizations endpoint..."
curl -s http://localhost:8006/demo/visualizations/ | jq .status_counts

echo ""
echo "=== Environment Variables ==="
echo "BACKEND_PORT: $BACKEND_PORT"
echo "VITE_API_BASE: $VITE_API_BASE"
echo "VITE_PORT: $VITE_PORT"

echo ""
echo "=== Frontend Config ==="
echo "Frontend .env file:"
cat frontend/.env

echo ""
echo "=== Running Processes ==="
ps aux | grep -i "test_api\|uvicorn\|python\|npm run dev" | grep -v grep
