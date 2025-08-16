#!/usr/bin/env python3
"""
Demo Data Script for Client Project Tracking & Billing System
Populates the database with sample data for demonstration
"""

import os
import sys
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Project, Assignment, Timesheet

def create_demo_data():
    """Create demo data for the system"""
    with app.app_context():
        print("🎭 Creating demo data...")
        
        # Create demo users
        users_data = [
            {'name': 'John Smith', 'email': 'john@company.com', 'role': 'employee'},
            {'name': 'Sarah Johnson', 'email': 'sarah@company.com', 'role': 'employee'},
            {'name': 'Mike Davis', 'email': 'mike@company.com', 'role': 'employee'},
            {'name': 'Lisa Wilson', 'email': 'lisa@company.com', 'role': 'employee'},
        ]
        
        users = []
        for user_data in users_data:
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                password=generate_password_hash('password123'),
                role=user_data['role']
            )
            db.session.add(user)
            users.append(user)
        
        # Create demo projects
        projects_data = [
            {
                'name': 'E-commerce Website Redesign',
                'client': 'TechCorp Inc.',
                'start_date': date(2024, 1, 15),
                'end_date': date(2024, 3, 30),
                'hourly_rate': 75.00,
                'status': 'active'
            },
            {
                'name': 'Mobile App Development',
                'client': 'StartupXYZ',
                'start_date': date(2024, 2, 1),
                'end_date': date(2024, 5, 15),
                'hourly_rate': 85.00,
                'status': 'active'
            },
            {
                'name': 'Database Migration Project',
                'client': 'Enterprise Solutions',
                'start_date': date(2024, 1, 1),
                'end_date': date(2024, 2, 28),
                'hourly_rate': 65.00,
                'status': 'completed'
            },
            {
                'name': 'UI/UX Design System',
                'client': 'Design Studio Pro',
                'start_date': date(2024, 3, 1),
                'end_date': date(2024, 4, 30),
                'hourly_rate': 70.00,
                'status': 'active'
            }
        ]
        
        projects = []
        for project_data in projects_data:
            project = Project(**project_data)
            db.session.add(project)
            projects.append(project)
        
        db.session.commit()
        print("✅ Users and projects created!")
        
        # Create assignments
        assignments_data = [
            (0, 0), (0, 1),  # John assigned to E-commerce and Mobile App
            (1, 1), (1, 2),  # Sarah assigned to Mobile App and Database
            (2, 0), (2, 3),  # Mike assigned to E-commerce and UI/UX
            (3, 2), (3, 3),  # Lisa assigned to Database and UI/UX
        ]
        
        for user_idx, project_idx in assignments_data:
            assignment = Assignment(
                project_id=projects[project_idx].id,
                user_id=users[user_idx].id
            )
            db.session.add(assignment)
        
        db.session.commit()
        print("✅ Assignments created!")
        
        # Create timesheet entries for the last 30 days
        print("📅 Creating timesheet entries...")
        
        for i in range(30):
            current_date = date.today() - timedelta(days=i)
            
            # Skip weekends
            if current_date.weekday() >= 5:
                continue
            
            # Create timesheet entries for each user
            for user in users:
                # Get user's assigned projects
                user_assignments = Assignment.query.filter_by(user_id=user.id).all()
                
                for assignment in user_assignments:
                    project = Project.query.get(assignment.project_id)
                    
                    # Random hours between 4-8 hours per day
                    import random
                    hours = random.uniform(4.0, 8.0)
                    
                    # Only log hours for active projects
                    if project.status == 'active':
                        timesheet = Timesheet(
                            project_id=project.id,
                            user_id=user.id,
                            date=current_date,
                            hours_worked=round(hours, 2),
                            description=f"Work on {project.name} - {['Development', 'Testing', 'Design', 'Planning'][random.randint(0, 3)]}"
                        )
                        db.session.add(timesheet)
        
        db.session.commit()
        print("✅ Timesheet entries created!")
        
        print("\n🎉 Demo data created successfully!")
        print("\nDemo Users:")
        for user in users:
            print(f"  - {user.name} ({user.email}) - Password: password123")
        print(f"\nDemo Projects: {len(projects)} projects created")
        print(f"Demo Assignments: {len(assignments_data)} assignments created")
        print(f"Demo Timesheets: ~{len(users) * 20} entries created")
        
        print("\nYou can now login with any of the demo users or the admin account!")

if __name__ == '__main__':
    create_demo_data()
