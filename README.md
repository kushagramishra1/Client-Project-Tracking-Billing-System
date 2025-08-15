# Client Project Tracking & Billing System

A comprehensive web-based system for tracking client projects, managing employee assignments, logging work hours, and generating billing records. Built with Flask, MySQL, and modern web technologies.

## 🚀 Features

### User Management
- **Role-based Authentication**: Admin and Employee roles with different permissions
- **Session-based Security**: Secure login/logout with Flask-Login
- **User Registration**: Self-registration with role selection

### Admin Features
- **Project Management**: Create, edit, delete, and view projects
- **Employee Assignment**: Assign employees to projects (many-to-many relationship)
- **Dashboard Analytics**: 
  - Total projects, active projects, completed projects
  - Total billed amount
  - Project status distribution chart (Chart.js)
  - Recent projects overview
- **Billing Management**: Generate billing records and view billing analytics
- **Search & Filter**: Dynamic project search and filtering

### Employee Features
- **Timesheet Management**: Log daily work hours for assigned projects
- **Project Overview**: View assigned projects and their details
- **Hours Tracking**: Weekly and monthly hours summary
- **Dashboard**: Personal statistics and project assignments

### Technical Features
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **Real-time Search**: JavaScript-powered project search
- **Data Visualization**: Chart.js integration for analytics
- **Form Validation**: Client-side and server-side validation
- **SQL Injection Protection**: ORM-based queries with SQLAlchemy

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask 2.3.3**: Web framework
- **Flask-Login**: User authentication
- **Flask-SQLAlchemy**: Database ORM
- **PyMySQL**: MySQL database connector
- **Werkzeug**: Password hashing and security

### Frontend
- **Bootstrap 5**: Responsive CSS framework
- **Font Awesome**: Icon library
- **Chart.js**: Data visualization
- **Vanilla JavaScript**: Interactive features

### Database
- **MySQL**: Primary database
- **SQLAlchemy ORM**: Database abstraction layer

## 📋 Prerequisites

Before running this application, ensure you have:

1. **Python 3.8 or higher**
2. **MySQL Server** (5.7 or higher)
3. **pip** (Python package manager)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd client-project-tracking-billing-system
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### Option A: Using the SQL Script
1. Open MySQL command line or MySQL Workbench
2. Run the database setup script:
```sql
source database_setup.sql
```

#### Option B: Using Python
```bash
python setup_database.py
```

### 5. Environment Configuration
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://username:password@localhost/client_billing_system
```

Replace `username` and `password` with your MySQL credentials.

### 6. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 👥 Default Users

After setup, you can log in with:

**Admin User:**
- Email: `admin@company.com`
- Password: `admin123`

**Note:** For production, change the default admin password immediately.

## 📊 Database Schema

### Tables Overview

1. **users** - User accounts and authentication
2. **projects** - Project information and details
3. **assignments** - Many-to-many relationship between users and projects
4. **timesheets** - Work hours logged by employees
5. **billing** - Generated billing records

### Key Relationships
- Users can be assigned to multiple projects
- Projects can have multiple employees assigned
- Timesheets link users to projects with date and hours
- Billing records are generated from timesheet data

## 🔧 Configuration

### Database Configuration
Edit the `DATABASE_URL` in your `.env` file:
```
DATABASE_URL=mysql+pymysql://username:password@host:port/database_name
```

### Application Settings
- **SECRET_KEY**: Used for session security (change in production)
- **DEBUG**: Set to `False` in production
- **SQLALCHEMY_TRACK_MODIFICATIONS**: Disabled for performance

## 📱 Usage Guide

### For Administrators

1. **Login** with admin credentials
2. **Create Projects**:
   - Navigate to Projects → Create New Project
   - Fill in project details (name, client, dates, hourly rate)
   - Set project status

3. **Assign Employees**:
   - Go to Assignments → Create Assignment
   - Select project and employee
   - Confirm assignment

4. **Monitor Progress**:
   - View dashboard for project statistics
   - Check billing page for revenue overview
   - Generate billing records for completed work

### For Employees

1. **Login** with employee credentials
2. **View Assigned Projects**:
   - Dashboard shows all assigned projects
   - Check project details and status

3. **Log Work Hours**:
   - Navigate to Timesheet
   - Select project and date
   - Enter hours worked and description
   - Submit timesheet entry

4. **Track Progress**:
   - View weekly/monthly hours summary
   - Check timesheet history
   - Monitor project assignments

## 🔒 Security Features

- **Password Hashing**: Secure password storage using Werkzeug
- **Session Management**: Flask-Login for secure sessions
- **SQL Injection Protection**: ORM-based queries prevent SQL injection
- **Role-based Access Control**: Different permissions for admin/employee
- **Input Validation**: Client-side and server-side form validation

## 📈 Analytics & Reporting

### Admin Dashboard
- Project status distribution (pie chart)
- Total projects and revenue statistics
- Recent projects overview
- Quick action buttons

### Employee Dashboard
- Assigned projects list
- Weekly/monthly hours tracking
- Progress indicators
- Quick access to timesheet

### Billing Analytics
- Project revenue overview
- Hourly rate analysis
- Top projects by revenue
- Billing chart visualization

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify MySQL is running
   - Check database credentials in `.env`
   - Ensure database exists

2. **Import Errors**
   - Activate virtual environment
   - Install requirements: `pip install -r requirements.txt`

3. **Permission Errors**
   - Check file permissions
   - Ensure write access to application directory

4. **Chart.js Not Loading**
   - Check internet connection (CDN)
   - Verify Chart.js script is included

### Debug Mode
For development, enable debug mode in `app.py`:
```python
app.run(debug=True)
```

## 🔄 API Endpoints

### Authentication
- `POST /login` - User login
- `POST /signup` - User registration
- `GET /logout` - User logout

### Projects (Admin)
- `GET /admin/projects` - List all projects
- `POST /admin/projects/create` - Create new project
- `GET /admin/projects/<id>/edit` - Edit project form
- `POST /admin/projects/<id>/edit` - Update project
- `POST /admin/projects/<id>/delete` - Delete project

### Assignments (Admin)
- `GET /admin/assignments` - List assignments
- `POST /admin/assignments/create` - Create assignment
- `POST /admin/assignments/<id>/delete` - Remove assignment

### Timesheet (Employee)
- `GET /timesheet` - View timesheet
- `POST /timesheet/log` - Log work hours

### Billing (Admin)
- `GET /admin/billing` - View billing overview
- `POST /admin/billing/generate` - Generate billing record

### API
- `GET /api/search_projects` - Search projects (JSON)

## 📝 Code Structure

```
client-project-tracking-billing-system/
├── app.py                 # Main Flask application
├── routes.py              # Route definitions
├── requirements.txt       # Python dependencies
├── database_setup.sql     # Database schema
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── login.html        # Login page
│   ├── signup.html       # Registration page
│   ├── admin_dashboard.html
│   ├── employee_dashboard.html
│   ├── admin_projects.html
│   ├── create_project.html
│   ├── edit_project.html
│   ├── admin_assignments.html
│   ├── timesheet.html
│   └── admin_billing.html
└── static/               # Static files (CSS, JS, images)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the documentation

## 🔮 Future Enhancements

- Email notifications for project updates
- PDF invoice generation
- Advanced reporting and analytics
- Mobile app development
- Integration with accounting software
- Time tracking with start/stop functionality
- Project templates and cloning
- Advanced user permissions and roles

---

**Built with ❤️ using Flask and modern web technologies**
