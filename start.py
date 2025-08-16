#!/usr/bin/env python3
"""
Startup Script for Client Project Tracking & Billing System
This script initializes the database and starts the application
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, db, User
    from werkzeug.security import generate_password_hash
    print("✅ All imports successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required packages: pip install -r requirements.txt")
    sys.exit(1)

def init_database():
    """Initialize the database and create default admin user"""
    with app.app_context():
        try:
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
            
            return True
            
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
            return False

def main():
    """Main function to start the application"""
    print("🚀 Client Project Tracking & Billing System")
    print("=" * 50)
    
    # Initialize database
    if init_database():
        print("\n🎉 System ready!")
        print("Starting the application...")
        print("Access the application at: http://localhost:5000")
        print("Admin login: admin@company.com / admin123")
        print("\nPress Ctrl+C to stop the server")
        
        # Start the application
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to initialize database. Please check the error messages above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
