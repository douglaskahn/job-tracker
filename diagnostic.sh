#!/bin/bash
# diagnostic.sh - Comprehensive diagnostic script for job-tracker application

# Color formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== JOB TRACKER DIAGNOSTIC REPORT ===${NC}"
echo "Date: $(date)"
echo "Hostname: $(hostname)"
echo "Username: $(whoami)"
echo

echo -e "${BLUE}=== SYSTEM INFORMATION ===${NC}"
echo "OS: $(uname -s)"
echo "Kernel: $(uname -r)"
echo "Architecture: $(uname -m)"
echo "CPU: $(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo 'N/A')"
echo "Memory: $(sysctl -n hw.memsize 2>/dev/null | awk '{print $0/1024/1024/1024 " GB"}' || echo 'N/A')"
echo "Disk space: $(df -h . | tail -1 | awk '{print $4}') available"
echo

echo -e "${BLUE}=== SOFTWARE VERSIONS ===${NC}"
echo "Node.js: $(node -v 2>/dev/null || echo 'Not installed')"
echo "npm: $(npm -v 2>/dev/null || echo 'Not installed')"
echo "Python: $(python --version 2>&1)"
echo "pip: $(pip --version 2>/dev/null || echo 'Not installed')"
echo "PM2: $(npx pm2 -v 2>/dev/null || echo 'Not installed')"
echo

echo -e "${BLUE}=== ENVIRONMENT VARIABLES ===${NC}"
echo "VITE_API_BASE: ${VITE_API_BASE:-Not set}"
echo "BACKEND_PORT: ${BACKEND_PORT:-Not set}"
echo "VITE_PORT: ${VITE_PORT:-Not set}"
echo "NODE_ENV: ${NODE_ENV:-Not set}"
echo

echo -e "${BLUE}=== ENVIRONMENT FILES ===${NC}"
echo "Root .env:"
if [[ -f .env ]]; then
    cat .env
    echo -e "${GREEN}✓ Root .env file found${NC}"
else 
    echo -e "${RED}✗ Root .env file not found${NC}"
fi
echo

echo "Frontend .env:"
if [[ -f frontend/.env ]]; then
    cat frontend/.env
    echo -e "${GREEN}✓ Frontend .env file found${NC}"
else
    echo -e "${RED}✗ Frontend .env file not found${NC}"
fi
echo

echo -e "${BLUE}=== DATABASE FILES ===${NC}"
if [[ -f jobtracker.db ]]; then
    echo -e "${GREEN}✓ Main database file exists${NC}"
    echo "  Size: $(ls -lh jobtracker.db | awk '{print $5}')"
    echo "  Modified: $(ls -la jobtracker.db | awk '{print $6, $7, $8}')"
else
    echo -e "${RED}✗ Main database file missing${NC}"
fi

if [[ -f demo_jobtracker.db ]]; then
    echo -e "${GREEN}✓ Demo database file exists${NC}"
    echo "  Size: $(ls -lh demo_jobtracker.db | awk '{print $5}')"
    echo "  Modified: $(ls -la demo_jobtracker.db | awk '{print $6, $7, $8}')"
else
    echo -e "${RED}✗ Demo database file missing${NC}"
fi
echo

echo -e "${BLUE}=== PORTS IN USE ===${NC}"
echo "Backend port (8006):"
if lsof -i :8006 > /dev/null; then
    lsof -i :8006
    echo -e "${GREEN}✓ Backend port is in use (application running)${NC}"
else
    echo -e "${RED}✗ Backend port is not in use (application not running)${NC}"
fi
echo

echo "Frontend port (4000):"
if lsof -i :4000 > /dev/null; then
    lsof -i :4000
    echo -e "${GREEN}✓ Frontend port is in use (application running)${NC}"
else
    echo -e "${RED}✗ Frontend port is not in use (application not running)${NC}"
fi
echo

echo -e "${BLUE}=== PROCESS STATUS ===${NC}"
echo "PM2 processes:"
if npx pm2 list | grep -q "job-tracker"; then
    npx pm2 list
    echo -e "${GREEN}✓ PM2 processes found${NC}"
else
    echo -e "${YELLOW}! No PM2 processes found for job-tracker${NC}"
fi
echo

echo "Python processes:"
if ps aux | grep -i python | grep -v grep | grep -q "test_api"; then
    ps aux | grep -i python | grep -v grep | grep "test_api"
    echo -e "${GREEN}✓ Backend Python process running${NC}"
else
    ps aux | grep -i python | grep -v grep
    echo -e "${YELLOW}! No backend Python process found${NC}"
fi
echo

echo "Node processes:"
if ps aux | grep -i node | grep -v grep | grep -q "vite"; then
    ps aux | grep -i node | grep -v grep | grep "vite"
    echo -e "${GREEN}✓ Frontend Node process running${NC}"
else
    ps aux | grep -i node | grep -v grep
    echo -e "${YELLOW}! No frontend Node process found${NC}"
fi
echo

echo -e "${BLUE}=== API ENDPOINT TESTS ===${NC}"
echo "Testing backend root endpoint..."
if curl -s http://localhost:8006/ | jq . > /dev/null; then
    curl -s http://localhost:8006/ | jq .
    echo -e "${GREEN}✓ Root endpoint working${NC}"
else
    echo -e "${RED}✗ Failed to connect to root endpoint${NC}"
fi
echo

echo "Testing applications endpoint..."
if curl -s http://localhost:8006/applications/ | jq '. | length' > /dev/null; then
    count=$(curl -s http://localhost:8006/applications/ | jq '. | length')
    echo "$count applications found"
    echo -e "${GREEN}✓ Applications endpoint working${NC}"
else
    echo -e "${RED}✗ Failed to connect to applications endpoint${NC}"
fi
echo

echo "Testing demo applications endpoint..."
if curl -s http://localhost:8006/demo/applications/ | jq '. | length' > /dev/null; then
    count=$(curl -s http://localhost:8006/demo/applications/ | jq '. | length')
    echo "$count demo applications found"
    echo -e "${GREEN}✓ Demo applications endpoint working${NC}"
else
    echo -e "${RED}✗ Failed to connect to demo applications endpoint${NC}"
fi
echo

echo "Testing visualizations endpoint..."
if curl -s http://localhost:8006/visualizations/ | jq 'keys' > /dev/null; then
    curl -s http://localhost:8006/visualizations/ | jq 'keys'
    echo -e "${GREEN}✓ Visualizations endpoint working${NC}"
else
    echo -e "${RED}✗ Failed to connect to visualizations endpoint${NC}"
fi
echo

echo "Testing demo visualizations endpoint..."
if curl -s http://localhost:8006/demo/visualizations/ | jq 'keys' > /dev/null; then
    curl -s http://localhost:8006/demo/visualizations/ | jq 'keys'
    echo -e "${GREEN}✓ Demo visualizations endpoint working${NC}"
else
    echo -e "${RED}✗ Failed to connect to demo visualizations endpoint${NC}"
fi
echo

echo -e "${BLUE}=== FRONTEND STATUS ===${NC}"
if curl -s http://localhost:4000/ | grep -q "<title>"; then
    title=$(curl -s http://localhost:4000/ | grep -o "<title>.*</title>")
    echo "$title"
    echo -e "${GREEN}✓ Frontend is running${NC}"
else
    echo -e "${RED}✗ Frontend not running or accessible${NC}"
fi
echo

echo -e "${BLUE}=== CORS TEST ===${NC}"
echo "Testing CORS preflight request to backend..."
if curl -s -I -X OPTIONS -H "Origin: http://localhost:4000" -H "Access-Control-Request-Method: GET" http://localhost:8006/applications/ | grep -i "Access-Control" > /dev/null; then
    curl -s -I -X OPTIONS -H "Origin: http://localhost:4000" -H "Access-Control-Request-Method: GET" http://localhost:8006/applications/ | grep -i "Access-Control"
    echo -e "${GREEN}✓ CORS properly configured${NC}"
else
    echo -e "${RED}✗ CORS headers not found${NC}"
fi
echo

echo -e "${BLUE}=== LOGS ===${NC}"
echo "Backend logs (last 10 lines):"
if [[ -f ~/.pm2/logs/job-tracker-backend-out.log ]]; then
    cat ~/.pm2/logs/job-tracker-backend-out.log 2>/dev/null | tail -10
    echo -e "${GREEN}✓ Backend logs available${NC}"
else
    echo -e "${YELLOW}! No backend logs found${NC}"
fi
echo

echo "Frontend logs (last 10 lines):"
if [[ -f ~/.pm2/logs/job-tracker-frontend-out.log ]]; then
    cat ~/.pm2/logs/job-tracker-frontend-out.log 2>/dev/null | tail -10
    echo -e "${GREEN}✓ Frontend logs available${NC}"
else
    echo -e "${YELLOW}! No frontend logs found${NC}"
fi
echo

echo "Backend error logs (last 10 lines):"
if [[ -f ~/.pm2/logs/job-tracker-backend-error.log ]]; then
    error_content=$(cat ~/.pm2/logs/job-tracker-backend-error.log 2>/dev/null | tail -10)
    echo "$error_content"
    if [[ -z "$error_content" || "$error_content" =~ "INFO:" ]]; then
        echo -e "${GREEN}✓ No significant errors in backend logs${NC}"
    else
        echo -e "${YELLOW}! Errors found in backend logs${NC}"
    fi
else
    echo -e "${YELLOW}! No backend error logs found${NC}"
fi
echo

echo -e "${BLUE}=== NETWORK DIAGNOSTICS ===${NC}"
echo "Network connections for backend:"
if netstat -an | grep 8006 > /dev/null; then
    netstat -an | grep 8006
    echo -e "${GREEN}✓ Network connections found for backend${NC}"
else
    echo -e "${YELLOW}! No network connections found for backend${NC}"
fi
echo

echo "Network connections for frontend:"
if netstat -an | grep 4000 > /dev/null; then
    netstat -an | grep 4000
    echo -e "${GREEN}✓ Network connections found for frontend${NC}"
else
    echo -e "${YELLOW}! No network connections found for frontend${NC}"
fi
echo

echo -e "${BLUE}=== CONFIG FILES ===${NC}"
echo "ecosystem.config.json:"
if [[ -f ecosystem.config.json ]]; then
    cat ecosystem.config.json
    echo -e "${GREEN}✓ PM2 ecosystem file found${NC}"
else
    echo -e "${RED}✗ PM2 ecosystem file not found${NC}"
fi
echo

echo "start-backend.sh:"
if [[ -f start-backend.sh ]]; then
    cat start-backend.sh
    echo -e "${GREEN}✓ Backend start script found${NC}"
else
    echo -e "${RED}✗ Backend start script not found${NC}"
fi
echo

echo "start-frontend.sh:"
if [[ -f start-frontend.sh ]]; then
    cat start-frontend.sh
    echo -e "${GREEN}✓ Frontend start script found${NC}"
else
    echo -e "${RED}✗ Frontend start script not found${NC}"
fi
echo

echo "start-dev.sh:"
if [[ -f start-dev.sh ]]; then
    cat start-dev.sh
    echo -e "${GREEN}✓ Dev start script found${NC}"
else
    echo -e "${RED}✗ Dev start script not found${NC}"
fi
echo

echo -e "${BLUE}=== SUMMARY ===${NC}"
# Count successful and failed checks
success_count=$(grep -c "${GREEN}✓" "$0")
error_count=$(grep -c "${RED}✗" "$0")
warning_count=$(grep -c "${YELLOW}!" "$0")

echo -e "${GREEN}✓ Successful checks: $success_count${NC}"
echo -e "${RED}✗ Failed checks: $error_count${NC}"
echo -e "${YELLOW}! Warnings: $warning_count${NC}"

if [[ $error_count -eq 0 ]]; then
    echo -e "\n${GREEN}ALL CHECKS PASSED! The application appears to be properly configured.${NC}"
elif [[ $error_count -le 2 ]]; then
    echo -e "\n${YELLOW}MINOR ISSUES DETECTED: There are a few issues that should be addressed.${NC}"
    echo "See the TROUBLESHOOTING.md file for guidance."
else
    echo -e "\n${RED}CRITICAL ISSUES DETECTED: There are several issues that need to be fixed.${NC}"
    echo "Run the following to reset the application:"
    echo "1. npx pm2 stop all && npx pm2 kill"
    echo "2. pkill -f \"python test_api.py\" || true"
    echo "3. pkill -f \"node.*vite\" || true"
    echo "4. ./start-dev.sh"
    echo "For more detailed troubleshooting, see TROUBLESHOOTING.md"
fi

echo -e "\n${BLUE}=== END OF DIAGNOSTIC REPORT ===${NC}"
