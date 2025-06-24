from backend.database import Base, engine
from backend.models import JobApplication

def initialize_database():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()