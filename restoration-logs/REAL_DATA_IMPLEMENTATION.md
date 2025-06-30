# Real Data Implementation Guide

This document explains how the Job Tracker application was updated to use real data from the SQLite database instead of mock data.

## Overview

The Job Tracker application now uses:
- Real SQLite databases (`jobtracker.db` and `demo_jobtracker.db`)
- A FastAPI backend (`real_data_api.py`) that connects to these databases
- SQLAlchemy ORM for database operations

## Key Components

### Database Files
- `jobtracker.db`: Main database with real job application data
- `demo_jobtracker.db`: Demo database with sample job application data

### API Server
- `real_data_api.py`: FastAPI server that connects to both real and demo databases

### Database Initialization
- `init_database.py`: Script to reset and populate both databases with sample data
  - Uses sqlite3 directly for database operations
  - Creates realistic sample data for testing

## How It Works

1. **Database Connection**:
   - The API connects to two separate SQLite databases
   - Uses SQLAlchemy ORM for structured queries
   - Automatically switches between real and demo databases based on endpoints

2. **API Endpoints**:
   - Regular endpoints (`/applications/`, etc.) connect to the real database
   - Demo endpoints (`/demo/applications/`, etc.) connect to the demo database
   - Visualization endpoints generate data from the respective databases

3. **Data Flow**:
   - Frontend API calls specify whether to use real or demo mode
   - Backend automatically selects the correct database based on the endpoint
   - Data is served from the SQLite database, not generated on the fly

## Database Schema

The main database table (`applications`) includes:
- Basic job information (company, role, status)
- Application details (dates, notes, etc.)
- Follow-up flags and salary information
- Timestamps for record-keeping

## Setup and Reset

To initialize or reset the databases with fresh sample data:

```bash
python init_database.py
```

## Migration from Mock Data

The original implementation used mock data generated in-memory. The current implementation:
1. Uses real persistent SQLite databases
2. Connects using proper ORM (SQLAlchemy)
3. Supports proper CRUD operations with database persistence
4. Maintains the same API structure so frontend changes were minimal

## Technical Details

- SQLAlchemy session management ensures proper database connections
- Two separate session factories maintain isolation between real and demo data
- SQLite connect_args ensure thread safety for concurrent requests
- All endpoints return properly formatted JSON data
