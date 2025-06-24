from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.models import DemoApplication, DemoStatusHistory
import random

# Companies with realistic job titles and salary ranges
COMPANIES = [
    {
        "name": "TechVision AI",
        "roles": [
            ("Senior Machine Learning Engineer", "160000-200000"),
            ("Full Stack Developer", "130000-160000"),
            ("Product Manager, AI/ML", "150000-180000")
        ],
        "domain": "techvision.ai"
    },
    {
        "name": "FinanceStream",
        "roles": [
            ("Software Engineer, Trading Systems", "140000-180000"),
            ("DevOps Engineer", "130000-170000"),
            ("Quantitative Developer", "160000-200000")
        ],
        "domain": "financestream.com"
    },
    {
        "name": "HealthTech Solutions",
        "roles": [
            ("Backend Engineer", "120000-150000"),
            ("Frontend Developer", "115000-145000"),
            ("Data Engineer", "130000-160000")
        ],
        "domain": "healthtechsolutions.com"
    },
    {
        "name": "CloudScale Systems",
        "roles": [
            ("Cloud Infrastructure Engineer", "140000-170000"),
            ("Site Reliability Engineer", "150000-180000"),
            ("Systems Architect", "160000-190000")
        ],
        "domain": "cloudscale.tech"
    },
    {
        "name": "DataFlow Analytics",
        "roles": [
            ("Data Scientist", "130000-160000"),
            ("ML Operations Engineer", "140000-170000"),
            ("Analytics Engineer", "120000-150000")
        ],
        "domain": "dataflow.io"
    }
]

# Status progression patterns
STATUS_PATTERNS = [
    # Quick rejection pattern
    ["Applied", "Rejected"],
    
    # Standard interview process
    ["Applied", "Interviewing", "Rejected"],
    ["Applied", "Interviewing", "Offer", "Accepted"],
    
    # Extended interview process
    ["Applied", "Interviewing", "Interviewing", "Interviewing", "Offer", "Accepted"],
    ["Applied", "Interviewing", "Interviewing", "Rejected"],
    
    # Not pursued
    ["Not Yet Applied", "Decided not to apply"],
    
    # Current active processes
    ["Applied", "Interviewing"],
    ["Not Yet Applied"],
    
    # Complete process with rejection
    ["Applied", "Interviewing", "Interviewing", "Offer", "Declined Offer"]
]

def generate_demo_data(db: Session):
    # Clear existing demo data
    db.query(DemoStatusHistory).delete()
    db.query(DemoApplication).delete()
    db.commit()
    
    # Current date for reference
    current_date = datetime(2025, 6, 23)
    
    applications = []
    
    # Generate 15-20 applications
    for i in range(random.randint(15, 20)):
        # Select company and role
        company = random.choice(COMPANIES)
        role, salary_range = random.choice(company["roles"])
        
        # Determine start date (between 90 days ago and today)
        days_ago = random.randint(0, 90)
        start_date = current_date - timedelta(days=days_ago)
        
        # Select status pattern
        pattern = random.choice(STATUS_PATTERNS)
        
        # Create application
        app = DemoApplication(
            company=company["name"],
            role=role,
            status=pattern[-1],  # Current status is last in pattern
            url=f"https://jobs.{company['domain']}/role/{i}",
            application_date=start_date.date() if pattern[0] != "Not Yet Applied" else None,
            met_with=None,  # Will be filled based on status
            notes="",  # Will be accumulated based on status changes
            salary=salary_range,
            follow_up_required=random.choice([True, False]) if pattern[-1] in ["Applied", "Interviewing"] else False
        )
        db.add(app)
        db.flush()  # Get ID for relationships
        
        # Generate status history
        current_time = start_date
        accumulated_notes = []
        met_with_people = set()
        
        for status in pattern:
            # Add some randomization to timing between status changes
            if status == pattern[0]:  # First status
                status_time = current_time
            else:
                days_forward = random.randint(3, 14)  # 3-14 days between changes
                current_time += timedelta(days=days_forward)
                status_time = current_time
            
            # Generate appropriate notes and contacts based on status
            notes = ""
            if status == "Applied":
                notes = "Submitted application online."
            elif status == "Interviewing":
                interviewer = random.choice(["Alex Thompson", "Sarah Chen", "Michael Rodriguez", "Emily Wong", "James Miller"])
                met_with_people.add(interviewer)
                interview_type = random.choice(["Phone screen", "Technical interview", "System design discussion", "Behavioral interview", "Team fit interview"])
                notes = f"{interview_type} with {interviewer}. "
                if random.random() < 0.3:  # 30% chance of follow-up note
                    notes += random.choice([
                        "Good conversation, followed up with thank you email.",
                        "Need to prepare more system design examples.",
                        "Team seems to have good culture.",
                        "Interesting technical challenges discussed.",
                        "Follow up in a week if no response."
                    ])
            elif status in ["Offer", "Accepted"]:
                notes = f"Offer received: {salary_range}. "
                if status == "Accepted":
                    notes += "Accepted offer, start date TBD."
            elif status == "Rejected":
                notes = random.choice([
                    "Position filled by another candidate.",
                    "Team decided to go with someone with more specific experience.",
                    "Good conversation but not the right fit at this time.",
                    "They're looking for someone more senior."
                ])
            
            # Create status history entry
            history = DemoStatusHistory(
                application_id=app.id,
                status=status,
                changed_at=status_time,
                notes=notes
            )
            db.add(history)
            
            # Accumulate notes and update application
            if notes:
                accumulated_notes.append(f"{status_time.strftime('%Y-%m-%d')}: {notes}")
        
        # Update application with accumulated data
        app.notes = "\n\n".join(accumulated_notes)
        app.met_with = ", ".join(met_with_people) if met_with_people else None
        
        # Add some random pros/cons for applications that progressed
        if len(pattern) > 2:
            app.pros = random.choice([
                "Great tech stack",
                "Strong team culture",
                "Good benefits",
                "Remote work option",
                "Interesting projects",
                "Growing company",
                "Good location"
            ])
            app.cons = random.choice([
                "Long commute",
                "Lower salary than expected",
                "Limited remote work",
                "High pressure environment",
                "Early stage startup risks",
                "Limited growth opportunities",
                "Lots of meetings"
            ])
        
        applications.append(app)
    
    db.commit()
    return applications

def clear_demo_data(db: Session):
    """Clear all demo data from the database."""
    db.query(DemoStatusHistory).delete()
    db.query(DemoApplication).delete()
    db.commit()
