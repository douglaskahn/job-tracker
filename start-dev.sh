#!/bin/bash

# Set the backend port
export PORT=8006

# Stop any existing PM2 processes first
echo "Stopping any existing PM2 processes..."
npx pm2 stop all 2>/dev/null || true

# Use local PM2 installation
PM2="npx pm2"

# Start the services using PM2
echo "Starting services with PM2..."
$PM2 start ecosystem.config.json

# Show running processes
echo "Running processes:"
$PM2 list

echo "Services started. To monitor: npx pm2 monit"
echo "To stop all services: npx pm2 stop all"
echo "To view logs: npx pm2 logs"
