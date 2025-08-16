# Client Project Tracking & Billing System

A comprehensive web-based system for tracking client projects, managing employee assignments, logging work hours, and generating automated billing reports.

## 🚀 Features

### User Roles
- **Admin**: Create/edit/delete projects, assign employees, set hourly rates, generate billing reports
- **Employee**: Log daily work hours for assigned projects, view personal dashboard

### Core Features
- ✅ **Authentication System**: Secure login/signup with session management
- ✅ **Project Management**: Create, edit, delete projects with client details
- ✅ **Employee Assignment**: Assign multiple employees to projects (many-to-many)
- ✅ **Timesheet Management**: Log daily work hours with descriptions
- ✅ **Automated Billing**: Calculate total hours × hourly rate with MySQL aggregate queries
- ✅ **Admin Dashboard**: 
  - Total projects, active projects, completed projects
  - Total billed amount with charts
  - Project status overview with Chart.js
- ✅ **Employee Dashboard**: 
  - List of assigned projects
  - Hours logged this week/month
- ✅ **Search & Filter**: Dynamic project search with JavaScript
- ✅ **Responsive Design**: Mobile-friendly interface with Bootstrap

### Technical Stack
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
- **Backend**: Python Flask with Flask-Login authentication
- **Database**: SQLite (default) / MySQL support
- **ORM**: SQLAlchemy with prepared statements
- **Security**: Password hashing, session management, SQL injection prevention

## 📋 Database Schema

```sql
-- Users table for authentication and role management
users(id, name, email, password, role, created_at, updated_at)

-- Projects table for project management  
projects(id, name, client, start_date, end_date, hourly_rate, status, created_at, updated_at)

-- Assignments table for many-to-many relationship
assignments(id, project_id, user_id, assigned_date)

-- Timesheets table for tracking work hours
timesheets(id, project_id, user_id, date, hours_worked, description, created_at, updated_at)

-- Billing table for storing calculated billing information
billing(id, project_id, total_hours, total_amount, billing_date, created_at)
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Start (Recommended)

1. **Clone or download the project**
   ```bash
   # If using git
   git clone <repository-url>
   cd "Client Project Tracking & Billing System"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python start.py
   ```

4. **Access the application**
   - Open your browser and go to: `http://localhost:5000`
   - Login with default admin credentials:
     - Email: `admin@company.com`
     - Password: `admin123`

### Manual Setup (Alternative)

1. **Create virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize database**
   ```bash
   python init_db.py
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-super-secret-key-change-this-in-production
DATABASE_URL=sqlite:///instance/client_billing.db
```

### Database Options
- **SQLite (Default)**: `sqlite:///instance/client_billing.db`
- **MySQL**: `mysql+pymysql://username:password@localhost/client_billing_system`

## 📱 Usage Guide

### Admin Functions

1. **Dashboard**
   - View project statistics and billing overview
   - See charts for project status distribution
   - Monitor total billed amount

2. **Project Management**
   - Create new projects with client details
   - Set hourly rates and project timelines
   - Update project status (active/completed/on_hold/cancelled)

3. **Employee Assignment**
   - Assign employees to projects
   - Manage project teams
   - Remove assignments as needed

4. **Billing Management**
   - View all projects with calculated billing
   - Generate billing records for completed work
   - Export billing reports

### Employee Functions

1. **Dashboard**
   - View assigned projects
   - See weekly and monthly hours logged
   - Track personal productivity

2. **Timesheet**
   - Log daily work hours for assigned projects
   - Add descriptions for work completed
   - View timesheet history

## 🎨 UI Features

- **Modern Design**: Professional corporate look with gradient backgrounds
- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Interactive Charts**: Chart.js integration for data visualization
- **Real-time Search**: JavaScript-powered project search and filtering
- **Form Validation**: Client-side and server-side validation
- **Bootstrap Components**: Cards, tables, modals, and navigation

## 🔒 Security Features

- **Password Hashing**: Secure password storage using Werkzeug
- **Session Management**: Flask-Login for secure user sessions
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **Access Control**: Role-based access to admin functions
- **Input Validation**: Form validation and sanitization

## 📊 Billing System

The billing system automatically calculates:
- **Total Hours**: Sum of all timesheet entries for a project
- **Total Amount**: Total hours × project hourly rate
- **Billing Records**: Stored in database for reporting
- **Charts**: Visual representation of billing data

## 🚀 Deployment

### Local Development
```bash
python start.py
```

### Production Deployment
1. Set `FLASK_ENV=production` in environment
2. Use a production WSGI server like Gunicorn
3. Configure a reverse proxy (Nginx/Apache)
4. Use a production database (MySQL/PostgreSQL)

## 📝 API Endpoints

- `GET /` - Home page (redirects to dashboard)
- `GET /login` - Login page
- `POST /login` - Login authentication
- `GET /signup` - Registration page
- `POST /signup` - User registration
- `GET /dashboard` - User dashboard (role-based)
- `GET /admin/dashboard` - Admin dashboard
- `GET /employee/dashboard` - Employee dashboard
- `GET /admin/projects` - Project management
- `GET /admin/assignments` - Employee assignments
- `GET /admin/billing` - Billing management
- `GET /timesheet` - Timesheet management
- `GET /api/search_projects` - Project search API

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

2. **Database Errors**
   - Delete `instance/client_billing.db` and run `python start.py` again

3. **Port Already in Use**
   - Change port in `start.py` or kill existing process

4. **Permission Errors**
   - Ensure write permissions for the project directory

### Getting Help
- Check the console output for error messages
- Verify all dependencies are installed
- Ensure database file has proper permissions

## 📄 License

This project is created for educational and demonstration purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Ready for Hackathon! 🎉**

The system is fully functional and ready for presentation. All core features are implemented with a professional UI and robust backend.
