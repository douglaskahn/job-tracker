import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from demo_models import DemoApplication
from database import SessionLocal, engine
import demo_models
import logging

logger = logging.getLogger(__name__)

# Create tables if they don't exist
def initialize_demo_db():
    # Force recreate the demo tables
    demo_models.DemoApplication.__table__.drop(engine, checkfirst=True)
    demo_models.DemoStatusHistory.__table__.drop(engine, checkfirst=True)
    
    # Create tables
    demo_models.Base.metadata.create_all(bind=engine)
    logger.info("Demo database tables created")

# Generate realistic demo data
def generate_demo_data(db: Session, count=50):
    # Only generate if the table is empty
    if db.query(DemoApplication).count() == 0:
        logger.info("Generating demo data...")
        
        companies = ["Google", "Microsoft", "Apple", "Amazon", "Meta", "Netflix", 
                    "Adobe", "Salesforce", "IBM", "Oracle", "Intel", "Cisco", 
                    "Twitter", "Slack", "Zoom", "Uber", "Lyft", "Airbnb", 
                    "Dropbox", "Square", "Stripe", "Shopify", "Twilio", "Atlassian"]
        
        roles = ["Software Engineer", "Data Scientist", "Product Manager", 
                "UX Designer", "Frontend Developer", "Backend Engineer", 
                "DevOps Engineer", "QA Engineer", "Technical Writer", 
                "Project Manager", "Systems Architect", "Mobile Developer", 
                "Cloud Engineer", "Machine Learning Engineer", "Security Engineer"]
        
        statuses = ["Not Yet Applied", "Applied", "Interviewing", "Offer", 
                   "Rejected", "No Longer Listed", "Decided not to apply", 
                   "Declined Offer", "Accepted", "Applied / No Longer Listed"]
        
        # Generate applications between March 1, 2025 and today
        start_date = datetime(2025, 3, 1)
        end_date = datetime(2025, 6, 23)  # Today
        
        demo_apps = []
        for i in range(count):
            # Generate random date within range
            days_range = (end_date - start_date).days
            random_days = random.randint(0, days_range)
            app_date = start_date + timedelta(days=random_days)
            
            # Create application with random data
            app = DemoApplication(
                company=random.choice(companies),
                role=random.choice(roles),
                status=random.choice(statuses),
                url=f"https://careers.{random.choice(companies).lower().replace(' ', '')}.com/job-{random.randint(1000, 9999)}",
                application_date=app_date,
                met_with=f"{random.choice(['John', 'Sarah', 'Michael', 'Emily', 'David', 'Jennifer'])} {random.choice(['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis'])}" if random.random() > 0.3 else None,
                notes=f"Applied for {random.choice(['remote', 'hybrid', 'in-office'])} position. {random.choice(['Good fit', 'Interesting role', 'Competitive salary', 'Great benefits'])}" if random.random() > 0.2 else None,
                pros=f"{random.choice(['Great culture', 'Good pay', 'Remote work', 'Interesting project', 'Career growth'])}" if random.random() > 0.3 else None,
                cons=f"{random.choice(['Long commute', 'Lower salary', 'Limited benefits', 'Unclear expectations', 'High pressure'])}" if random.random() > 0.3 else None,
                salary=f"${random.randint(80, 200)}k" if random.random() > 0.4 else None,
                follow_up_required=random.random() > 0.7,
                created_at=app_date,
                updated_at=app_date + timedelta(days=random.randint(0, 14)),
                status_change_date=app_date + timedelta(days=random.randint(0, 7)) if random.random() > 0.5 else None
            )
            
            # Randomly add resume and cover letter files (30% chance each)
            if random.random() > 0.7:
                app.resume_file = f"demo_resume_{i+1}.pdf"
            if random.random() > 0.7:
                app.cover_letter_file = f"demo_cover_letter_{i+1}.pdf"
                
            demo_apps.append(app)
        
        # Add all applications to the database
        db.add_all(demo_apps)
        db.commit()
        logger.info(f"Generated {count} demo applications")
    else:
        logger.info("Demo data already exists, skipping generation")

# Function to call during app startup
def initialize_demo_data():
    db = SessionLocal()
    try:
        initialize_demo_db()
        generate_demo_data(db)
    finally:
        db.close()
