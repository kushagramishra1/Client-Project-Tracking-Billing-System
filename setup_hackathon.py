#!/usr/bin/env python3
"""
Hackathon Setup Script for Client Project Tracking & Billing System
This script sets up everything needed for the hackathon presentation
"""

import os
import sys
import subprocess
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            return True
        else:
            print(f"❌ {description} failed!")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def check_python():
    """Check if Python is available"""
    print("🐍 Checking Python installation...")
    
    python_commands = ['python', 'python3', 'py']
    
    for cmd in python_commands:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Found Python: {result.stdout.strip()}")
                return cmd
        except:
            continue
    
    print("❌ Python not found!")
    print("Please install Python 3.7 or higher from https://www.python.org/downloads/")
    return None

def install_requirements(python_cmd):
    """Install required packages"""
    print("\n📦 Installing required packages...")
    
    # Try to install requirements
    if run_command(f"{python_cmd} -m pip install -r requirements.txt", "Installing requirements"):
        return True
    
    # If that fails, try installing packages individually
    packages = [
        'Flask==2.3.3',
        'Flask-Login==0.6.3', 
        'Flask-SQLAlchemy==3.0.5',
        'Flask-WTF==1.1.1',
        'WTForms==3.0.1',
        'Werkzeug==2.3.7',
        'python-dotenv==1.0.0',
        'email-validator==2.0.0'
    ]
    
    for package in packages:
        if not run_command(f"{python_cmd} -m pip install {package}", f"Installing {package}"):
            return False
    
    return True

def setup_database(python_cmd):
    """Set up the database"""
    print("\n🗄️ Setting up database...")
    
    # Import and run database setup
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from app import app, db, User
        from werkzeug.security import generate_password_hash
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Create admin user
            admin_user = User.query.filter_by(email='admin@company.com').first()
            if not admin_user:
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
                
                print("✅ Admin user created successfully!")
                print(f"Email: admin@company.com")
                print(f"Password: {admin_password}")
            else:
                print("✅ Admin user already exists!")
            
            return True
            
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def create_demo_data(python_cmd):
    """Create demo data"""
    print("\n🎭 Creating demo data...")
    
    if run_command(f"{python_cmd} demo_data.py", "Creating demo data"):
        return True
    
    print("⚠️ Demo data creation failed, but the system will still work!")
    return True

def main():
    """Main setup function"""
    print("🚀 Client Project Tracking & Billing System - Hackathon Setup")
    print("=" * 60)
    
    # Check Python
    python_cmd = check_python()
    if not python_cmd:
        print("\n❌ Setup failed: Python not found!")
        return False
    
    # Install requirements
    if not install_requirements(python_cmd):
        print("\n❌ Setup failed: Could not install requirements!")
        return False
    
    # Setup database
    if not setup_database(python_cmd):
        print("\n❌ Setup failed: Could not setup database!")
        return False
    
    # Create demo data
    create_demo_data(python_cmd)
    
    print("\n🎉 Setup completed successfully!")
    print("\n" + "=" * 60)
    print("🚀 READY FOR HACKATHON PRESENTATION!")
    print("=" * 60)
    
    print("\n📋 Quick Start:")
    print("1. Run the application:")
    print(f"   {python_cmd} start.py")
    print("   OR double-click run.bat")
    
    print("\n2. Open your browser and go to:")
    print("   http://localhost:5000")
    
    print("\n3. Login with:")
    print("   Admin: admin@company.com / admin123")
    print("   Employee: john@company.com / password123")
    print("   Employee: sarah@company.com / password123")
    print("   Employee: mike@company.com / password123")
    print("   Employee: lisa@company.com / password123")
    
    print("\n🎯 Features to demonstrate:")
    print("✅ Admin Dashboard with charts and statistics")
    print("✅ Project Management (Create/Edit/Delete)")
    print("✅ Employee Assignment system")
    print("✅ Timesheet logging and management")
    print("✅ Automated Billing calculation")
    print("✅ Search and filter functionality")
    print("✅ Responsive mobile-friendly design")
    
    print("\n💡 Tips for presentation:")
    print("- Show the admin dashboard first")
    print("- Create a new project")
    print("- Assign employees to projects")
    print("- Log some timesheet entries")
    print("- Generate billing records")
    print("- Show the employee dashboard")
    print("- Demonstrate search functionality")
    
    print("\n🎊 Good luck with your hackathon presentation!")
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)
