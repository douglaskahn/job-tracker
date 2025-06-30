#!/usr/bin/env python3
"""
Script to populate the demo database with sample data.
"""
import sqlite3
import datetime
import random

DEMO_DB_PATH = "./demo_jobtracker.db"

def create_demo_application(id):
    """Create a sample demo application."""
    today = datetime.datetime.now()
    days_ago = random.randint(1, 90)
    app_date = (today - datetime.timedelta(days=days_ago)).strftime("%Y-%m-%d")
    updated_days_ago = random.randint(0, days_ago)
    updated_date = (today - datetime.timedelta(days=updated_days_ago)).strftime("%Y-%m-%d %H:%M:%S")
    
    statuses = [
        "Not Yet Applied", "Applied", "Phone Screen", "Technical Interview", 
        "Onsite Interview", "Offer Received", "Rejected", "Accepted"
    ]
    
    roles = [
        "Software Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer",
        "Data Scientist", "Machine Learning Engineer", "DevOps Engineer", "Site Reliability Engineer",
        "Product Manager", "UX Designer", "UI Designer", "Project Manager", "QA Engineer",
        "Security Engineer", "Mobile Developer", "iOS Developer", "Android Developer",
        "Data Engineer", "Business Analyst", "Technical Writer"
    ]
    
    companies = [
        "Amazon", "Google", "Microsoft", "Apple", "Meta", "Netflix", "Spotify", 
        "Slack", "Airbnb", "Dropbox", "Twitter", "Salesforce", "Adobe", "Zoom",
        "LinkedIn", "Square", "Stripe", "Shopify", "IBM", "Intel", "Oracle", 
        "Nvidia", "PayPal", "Twilio", "Atlassian", "DocuSign", "GitHub", "GitLab",
        "Uber", "Lyft", "DoorDash", "Instacart", "Coinbase", "Robinhood", "Palantir"
    ]
    
    return {
        "id": id,
        "company": random.choice(companies),
        "role": random.choice(roles),
        "status": random.choice(statuses),
        "url": f"https://example.com/jobs/{id}",
        "application_date": app_date,
        "met_with": f"{random.choice(['Sarah', 'Michael', 'Emily', 'David', 'Rachel', 'James', 'Sophia', 'Thomas', 'Olivia', 'Daniel'])} {random.choice(['Johnson', 'Chen', 'Rodriguez', 'Kim', 'Taylor', 'Wilson', 'Martinez', 'Lee', 'Brown', 'Garcia'])}",
        "notes": f"Application for {random.choice(['entry level', 'mid-level', 'senior', 'lead', 'principal'])} position. {random.choice(['Referred by colleague.', 'Found on LinkedIn.', 'Company recruiter reached out.', 'Applied through company website.', 'Saw posting on Indeed.', ''])}",
        "follow_up_required": id % 3 == 0,  # Every third application needs follow-up
        "pros": random.choice([
            "Great team culture, good benefits", 
            "Remote work option, competitive salary",
            "Strong engineering culture, learning opportunities",
            "Good work-life balance, exciting projects",
            "Career growth, modern tech stack",
            "Excellent healthcare, stock options",
            "Flexible hours, collaborative environment",
            "Industry leader, innovative projects"
        ]),
        "cons": random.choice([
            "Long commute, intense workload",
            "Limited remote options, slow promotion track",
            "Smaller company, less stability",
            "High pressure environment, long hours",
            "Lower salary than competitors",
            "Older tech stack, bureaucratic processes",
            "Limited growth opportunities",
            "Competitive environment, high turnover"
        ]),
        "salary": random.choice([
            f"${random.randint(80, 150)}k",
            f"${random.randint(80, 150)},000",
            f"${random.randint(80, 150)}k-${random.randint(150, 200)}k",
            f"${random.randint(80, 120)}k base + bonus",
            f"${random.randint(100, 180)}k + benefits",
            f"${random.randint(90, 160)}k DOE",
            ""
        ]),
        "created_at": app_date + " 00:00:00", 
        "updated_at": updated_date,
        "order_number": id
    }

def populate_demo_database():
    """Populate the demo database with sample data."""
    conn = sqlite3.connect(DEMO_DB_PATH)
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM applications")
    conn.commit()
    
    # Generate and insert sample data
    for i in range(1, 51):
        app = create_demo_application(i)
        
        # Create the insert statement
        columns = ", ".join(app.keys())
        placeholders = ", ".join(["?"] * len(app))
        values = list(app.values())
        
        cursor.execute(f"INSERT INTO applications ({columns}) VALUES ({placeholders})", values)
    
    # Commit the changes
    conn.commit()
    
    # Verify the data
    cursor.execute("SELECT COUNT(*) FROM applications")
    count = cursor.fetchone()[0]
    print(f"Added {count} demo applications to the database")
    
    # Close the connection
    conn.close()

if __name__ == "__main__":
    populate_demo_database()
