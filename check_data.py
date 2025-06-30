#!/usr/bin/env python3
import sys
import os
import logging
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database paths
DB_PATH = "jobtracker.db"
DEMO_DB_PATH = "demo_jobtracker.db"

def check_database(db_path, name):
    """Check if the database exists and has data."""
    if not os.path.exists(db_path):
        logger.error(f"{name} database file not found at: {db_path}")
        return False

    # Connect to the database
    db_url = f"sqlite:///{db_path}"
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        logger.info(f"Connected to {name} database at {db_path}")
        
        # Check for tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Tables in {name} database: {tables}")
        
        # Look for applications or jobs table
        if "applications" in tables:
            # Count records in applications table
            result = db.execute(text("SELECT COUNT(*) FROM applications")).scalar()
            logger.info(f"Found {result} records in applications table in {name} database")
            
            # Get a sample record if available
            if result > 0:
                sample = db.execute(text("SELECT * FROM applications LIMIT 1")).fetchone()
                logger.info(f"Sample record from {name} database: {sample}")
                return True
            else:
                logger.warning(f"No records found in applications table in {name} database")
                return False
        elif "jobs" in tables:
            # Count records in jobs table
            result = db.execute(text("SELECT COUNT(*) FROM jobs")).scalar()
            logger.info(f"Found {result} records in jobs table in {name} database")
            
            # Get a sample record if available
            if result > 0:
                sample = db.execute(text("SELECT * FROM jobs LIMIT 1")).fetchone()
                logger.info(f"Sample record from {name} database: {sample}")
                return True
            else:
                logger.warning(f"No records found in jobs table in {name} database")
                return False
        else:
            logger.error(f"No applications or jobs table found in {name} database")
            return False
    except Exception as e:
        logger.error(f"Error checking {name} database: {str(e)}")
        return False
    finally:
        db.close()

def main():
    """Main function to check database status."""
    logger.info("Checking database setup...")
    
    # Check main database
    main_db_ok = check_database(DB_PATH, "Main")
    
    # Check demo database
    demo_db_ok = check_database(DEMO_DB_PATH, "Demo")
    
    # Report overall status
    if main_db_ok and demo_db_ok:
        logger.info("✅ Database check passed: Both databases exist and have data")
        return 0
    elif main_db_ok:
        logger.warning("⚠️ Main database is OK but demo database has issues")
        return 1
    elif demo_db_ok:
        logger.warning("⚠️ Demo database is OK but main database has issues")
        return 1
    else:
        logger.error("❌ Database check failed: Both databases have issues")
        return 2

if __name__ == "__main__":
    sys.exit(main())
