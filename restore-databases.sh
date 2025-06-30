#!/bin/bash
# Script to restore real and demo databases to their known good states

echo "===== Job Tracker Database Restoration Tool ====="
echo "This script will restore the real and demo databases from backups or generate new data."

# Function to handle errors
function handle_error {
  echo "ERROR: $1"
  exit 1
}

# Check if files exist
if [ ! -f "jobtracker 2.db" ]; then
  handle_error "Backup file 'jobtracker 2.db' not found. Cannot restore real data."
fi

# Prompt for confirmation
echo ""
echo "WARNING: This will replace your current databases with backup data or generate new demo data."
read -p "Do you want to continue? (y/n): " confirm
if [[ $confirm != [yY] ]]; then
  echo "Operation cancelled."
  exit 0
fi

# Kill any running backend processes
echo ""
echo "Stopping backend services..."
pkill -f direct_sqlite_api.py
pkill -f uvicorn
sleep 2

# Backup current databases
echo ""
echo "Creating backup of current databases..."
if [ -f "jobtracker.db" ]; then
  cp jobtracker.db jobtracker.db.bak.$(date +%Y%m%d%H%M%S)
  echo "Backed up jobtracker.db"
fi

if [ -f "demo_jobtracker.db" ]; then
  cp demo_jobtracker.db demo_jobtracker.db.bak.$(date +%Y%m%d%H%M%S)
  echo "Backed up demo_jobtracker.db"
fi

# Restore real data
echo ""
echo "Restoring real data from 'jobtracker 2.db'..."
cp "jobtracker 2.db" jobtracker.db
echo "Real data restored."

# Regenerate demo data
echo ""
echo "Regenerating demo data..."
if [ -x "./populate_demo_db.py" ]; then
  ./populate_demo_db.py
else
  chmod +x ./populate_demo_db.py
  ./populate_demo_db.py
fi

# Restart backend
echo ""
echo "Restarting backend services..."
./start-backend.sh &
sleep 3

# Verify databases
echo ""
echo "Verifying databases..."
curl -s http://localhost:8006/debug/info | grep -A 4 database_info
echo ""
echo "Restoration complete!"
echo "- Real data restored from 'jobtracker 2.db'"
echo "- Demo data regenerated with 50 sample applications"
echo ""
echo "You can now access the application at:"
echo "- Frontend: http://localhost:4000"
echo "- Backend API: http://localhost:8006"
