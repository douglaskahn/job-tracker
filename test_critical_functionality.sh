#!/bin/bash
# test_critical_functionality.sh
# This script checks critical functionality in the job tracker application

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting critical functionality tests for Job Tracker...${NC}"

# Check if the backend is running
echo -e "\n${YELLOW}Checking if backend is running...${NC}"
curl -s http://localhost:8005/api/config > /dev/null
if [ $? -eq 0 ]; then
  echo -e "${GREEN}✓ Backend is running${NC}"
else
  echo -e "${RED}✗ Backend is not running. Please start it with ./start-backend.sh${NC}"
  exit 1
fi

# Check if the frontend is running
echo -e "\n${YELLOW}Checking if frontend is running...${NC}"
curl -s http://localhost:5173 > /dev/null
if [ $? -eq 0 ]; then
  echo -e "${GREEN}✓ Frontend is running${NC}"
else
  echo -e "${RED}✗ Frontend is not running. Please start it with ./start-dev.sh${NC}"
  exit 1
fi

# Check critical backend endpoints
echo -e "\n${YELLOW}Testing critical backend endpoints...${NC}"

# Test pagination endpoint
echo -e "\n${YELLOW}Testing pagination...${NC}"
PAGINATION_TEST=$(curl -s "http://localhost:8005/applications/?page=1&page_size=10")
if [[ $PAGINATION_TEST == *"data"* && $PAGINATION_TEST == *"total"* ]]; then
  echo -e "${GREEN}✓ Pagination endpoint is working${NC}"
else
  echo -e "${RED}✗ Pagination endpoint is not working properly${NC}"
  echo "$PAGINATION_TEST"
fi

# Test sorting endpoint
echo -e "\n${YELLOW}Testing sorting...${NC}"
SORT_TEST=$(curl -s "http://localhost:8005/applications/?sort_by=company&sort_order=asc")
if [[ $SORT_TEST == *"data"* ]]; then
  echo -e "${GREEN}✓ Sorting endpoint is working${NC}"
else
  echo -e "${RED}✗ Sorting endpoint is not working properly${NC}"
fi

# Test filtering endpoint
echo -e "\n${YELLOW}Testing filtering...${NC}"
FILTER_TEST=$(curl -s "http://localhost:8005/applications/?status=Applied")
if [[ $FILTER_TEST == *"data"* ]]; then
  echo -e "${GREEN}✓ Filtering endpoint is working${NC}"
else
  echo -e "${RED}✗ Filtering endpoint is not working properly${NC}"
fi

# Test demo endpoints
echo -e "\n${YELLOW}Testing demo endpoints...${NC}"
DEMO_TEST=$(curl -s "http://localhost:8005/demo/applications/?page=1&page_size=10")
if [[ $DEMO_TEST == *"data"* && $DEMO_TEST == *"total"* ]]; then
  echo -e "${GREEN}✓ Demo endpoints are working${NC}"
else
  echo -e "${RED}✗ Demo endpoints are not working properly${NC}"
fi

# Check for large dataset handling
echo -e "\n${YELLOW}Testing large dataset handling...${NC}"
LARGE_TEST=$(curl -s "http://localhost:8005/applications/?page_size=1000")
if [[ $LARGE_TEST == *"data"* && $LARGE_TEST == *"total"* ]]; then
  echo -e "${GREEN}✓ Large dataset handling is working${NC}"
else
  echo -e "${RED}✗ Large dataset handling is not working properly${NC}"
fi

echo -e "\n${YELLOW}Testing frontend code for critical functionality...${NC}"

# Check for pagination controls in JobTable.jsx
echo -e "\n${YELLOW}Checking for pagination controls...${NC}"
if grep -q "First\|Prev\|Next\|Last" /Users/douglaskahn/Documents/job-tracker/frontend/src/JobTable.jsx; then
  echo -e "${GREEN}✓ Pagination controls are present${NC}"
else
  echo -e "${RED}✗ Pagination controls are missing or incomplete${NC}"
fi

# Check for hideFooter in DataGrid
echo -e "\n${YELLOW}Checking for hideFooter in DataGrid...${NC}"
if grep -q "hideFooter={true}" /Users/douglaskahn/Documents/job-tracker/frontend/src/JobTable.jsx; then
  echo -e "${GREEN}✓ hideFooter is properly set${NC}"
else
  echo -e "${RED}✗ hideFooter is missing in DataGrid${NC}"
fi

# Check for "Show All" implementation
echo -e "\n${YELLOW}Checking for proper Show All implementation...${NC}"
if grep -q "page_size: 1000" /Users/douglaskahn/Documents/job-tracker/frontend/src/App.jsx; then
  echo -e "${GREEN}✓ Show All implementation looks correct${NC}"
else
  echo -e "${RED}✗ Show All might not be fetching all records${NC}"
fi

echo -e "\n${YELLOW}All tests completed!${NC}"
echo -e "For a full manual verification, please check:"
echo -e "1. Pagination buttons work correctly"
echo -e "2. Show All shows all records"
echo -e "3. Sorting works on all columns"
echo -e "4. Filtering works for status and follow-up"
echo -e "5. DataGrid footer is hidden"
