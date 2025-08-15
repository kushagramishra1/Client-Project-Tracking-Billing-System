#!/usr/bin/env python3
"""
Database Setup Script for Client Project Tracking & Billing System

This script helps set up the database and create a default admin user.
Run this script after installing the requirements and configuring your database connection.
"""

import os
import sys
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_default_admin():
    """Create a default admin user with proper password hash"""
    from app import app, db, User
    
    with app.app_context():
        # Check if admin user already exists
        admin_user = User.query.filter_by(email='admin@company.com').first()
        
        if admin_user:
            print("Admin user already exists!")
            return
        
        # Create admin user with proper password hash
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

def setup_database():
    """Set up the database tables"""
    from app import app, db
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Create default admin user
            create_default_admin()
            
        except Exception as e:
            print(f"❌ Error setting up database: {e}")
            print("\nPlease check your database connection settings in .env file")
            return False
    
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'flask',
        'flask_login',
        'flask_sqlalchemy',
        'pymysql',
        'python-dotenv',
        'werkzeug'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nPlease install missing packages with:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed!")
    return True

def check_env_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("\nPlease create a .env file with the following content:")
        print("SECRET_KEY=your-secret-key-here")
        print("DATABASE_URL=mysql+pymysql://username:password@localhost/client_billing_system")
        return False
    
    # Load and check environment variables
    load_dotenv()
    
    required_vars = ['SECRET_KEY', 'DATABASE_URL']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please add them to your .env file")
        return False
    
    print("✅ Environment variables configured!")
    return True

def main():
    """Main setup function"""
    print("🚀 Client Project Tracking & Billing System - Database Setup")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment configuration
    if not check_env_file():
        sys.exit(1)
    
    print("\n📊 Setting up database...")
    
    # Setup database
    if setup_database():
        print("\n🎉 Setup completed successfully!")
        print("\nYou can now run the application with:")
        print("python app.py")
        print("\nDefault admin credentials:")
        print("Email: admin@company.com")
        print("Password: admin123")
        print("\n⚠️  Remember to change the default password!")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
