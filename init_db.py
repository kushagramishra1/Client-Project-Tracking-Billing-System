#!/usr/bin/env python3
"""
Simple Database Initialization Script
Creates the database and default admin user
"""

from app import app, db, User
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize the database and create default admin user"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Check if admin user exists
        admin_user = User.query.filter_by(email='admin@company.com').first()
        
        if not admin_user:
            # Create default admin user
            admin_password = 'admin123'
            hashed_password = generate_password_hash(admin_password)
            
            admin_user = User(
                name='Admin User',
                email='admin@company.com',
                password=hashed_password,
                role='admin'
            )
            
            db.session.add(admin_user)
            db.session.commit()
            
            print("✅ Default admin user created successfully!")
            print(f"Email: admin@company.com")
            print(f"Password: {admin_password}")
            print("\n⚠️  IMPORTANT: Change this password after first login!")
        else:
            print("✅ Admin user already exists!")
        
        print("\n🎉 Database initialization completed!")
        print("You can now run the application with: python app.py")

if __name__ == '__main__':
    init_database()
