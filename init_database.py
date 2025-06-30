#!/usr/bin/env python3
"""
Initialize the database with sample data
"""
import sqlite3
import os
import random
from datetime import datetime, timedelta

# Define the database files
REAL_DB_FILE = "jobtracker.db"
DEMO_DB_FILE = "demo_jobtracker.db"

def create_tables(conn):
    """Create the applications table if it doesn't exist."""
    cursor = conn.cursor()
    
    # Create applications table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        role TEXT NOT NULL,
        status TEXT NOT NULL,
        url TEXT,
        application_date DATE,
        met_with TEXT,
        notes TEXT,
        resume_file TEXT,
        cover_letter_file TEXT,
        order_number INTEGER,
        follow_up_required BOOLEAN DEFAULT 0,
        pros TEXT,
        cons TEXT,
        salary TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    print(f"Tables created successfully")

def generate_sample_data(is_demo=False, count=40):
    """Generate realistic application data."""
    prefix = "Demo" if is_demo else ""
    companies = [
        f"{prefix}Tech", f"{prefix}Corp", f"{prefix}Global", f"{prefix}Innovations", 
        f"{prefix}Software", f"{prefix}Systems", f"{prefix}Digital", f"{prefix}Cloud",
        f"{prefix}Works", f"{prefix}Solutions", f"{prefix}AI", f"{prefix}ML"
    ]
    
    roles = [
        "Software Engineer", "Frontend Developer", "Backend Developer", 
        "Data Scientist", "DevOps Engineer", "Product Manager", "UX Designer"
    ]
    
    statuses = [
        "Not Yet Applied", "Applied", "Phone Screen", "Technical Interview", 
        "Onsite Interview", "Offer Received", "Rejected", "Accepted"
    ]
    
    applications = []
    for i in range(1, count + 1):
        today = datetime.now()
        company = random.choice(companies)
        role = random.choice(roles)
        status = random.choice(statuses)
        days_ago = random.randint(1, 90)
        app_date = (today - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        application = {
            "company": f"{company} {i}",
            "role": role,
            "status": status,
            "url": f"https://example.com/jobs/{i}",
            "application_date": app_date,
            "met_with": f"{'Jane' if i % 2 == 0 else 'John'} Recruiter",
            "notes": f"{'Demo' if is_demo else ''} application with ID {i}",
            "follow_up_required": i % 3 == 0,  # Every third application needs follow-up
            "pros": "Good benefits, interesting work",
            "cons": "Long commute, high workload",
            "salary": f"{random.randint(80, 150)}000",
            "created_at": (today - timedelta(days=days_ago)).isoformat(),
            "updated_at": (today - timedelta(days=random.randint(0, days_ago))).isoformat()
        }
        applications.append(application)
    
    return applications

def populate_database(db_file, is_demo=False, count=40):
    """Populate the database with sample data."""
    # Connect to the database
    conn = sqlite3.connect(db_file)
    
    # Create tables if they don't exist
    create_tables(conn)
    
    # Generate sample data
    applications = generate_sample_data(is_demo, count)
    
    # Clear existing data
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications")
    conn.commit()
    
    # Insert sample data
    for app in applications:
        cursor.execute('''
        INSERT INTO applications (
            company, role, status, url, application_date, met_with, notes,
            follow_up_required, pros, cons, salary, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            app["company"], app["role"], app["status"], app["url"], app["application_date"],
            app["met_with"], app["notes"], app["follow_up_required"], app["pros"],
            app["cons"], app["salary"], app["created_at"], app["updated_at"]
        ))
    
    conn.commit()
    print(f"Inserted {len(applications)} applications into {db_file}")
    
    # Close the connection
    conn.close()

def main():
    """Main function to initialize databases."""
    print("Initializing databases with sample data...")
    
    # We don't need to create directories as the files are in the root
    # Initialize real database
    populate_database(REAL_DB_FILE, is_demo=False, count=40)
    
    # Initialize demo database
    populate_database(DEMO_DB_FILE, is_demo=True, count=30)
    
    print("Database initialization complete!")

if __name__ == "__main__":
    main()
