import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import Base
from app.models.user import User
from app.core.security import get_password_hash

# Database connection
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ticketdb")

def init_db():
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    # Check if admin user exists
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        # Create admin user
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            is_active=True,
            is_superuser=True
        )
        db.add(admin)
        db.commit()
        print("Admin user created successfully!")
    else:
        print("Admin user already exists.")
    
    # Check if regular user exists
    user = db.query(User).filter(User.email == "user@example.com").first()
    if not user:
        # Create regular user
        user = User(
            email="user@example.com",
            hashed_password=get_password_hash("user123"),
            full_name="Regular User",
            is_active=True,
            is_superuser=False
        )
        db.add(user)
        db.commit()
        print("Regular user created successfully!")
    else:
        print("Regular user already exists.")
    
    db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialization completed!") 