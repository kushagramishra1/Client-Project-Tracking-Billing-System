from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-before-deployment')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///client_billing.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='employee')

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    client = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    hourly_rate = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='active')

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)

class Timesheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    hours_worked = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)

class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    total_hours = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    billing_date = db.Column(db.Date, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def initialize_database():
    with app.app_context():
        db.create_all()

        admin_email = os.getenv('ADMIN_EMAIL', 'admin@company.com')
        if not User.query.filter_by(email=admin_email).first():
            admin_user = User(
                name='Admin User',
                email=admin_email,
                password=generate_password_hash(os.getenv('ADMIN_PASSWORD', 'admin123')),
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()

initialize_database()

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = 'employee'
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
        else:
            hashed_password = generate_password_hash(password)
            user = User(name=name, email=email, password=hashed_password, role=role)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('employee_dashboard'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    total_projects = Project.query.count()
    active_projects = Project.query.filter_by(status='active').count()
    completed_projects = Project.query.filter_by(status='completed').count()
    
    # Calculate total billed amount
    total_billed = db.session.query(db.func.sum(Billing.total_amount)).scalar() or 0
    
    # Get recent projects
    recent_projects = Project.query.order_by(Project.id.desc()).limit(5).all()
    
    # Get status counts for chart - convert to dictionary format
    status_counts_raw = db.session.query(Project.status, db.func.count(Project.id)).group_by(Project.status).all()
    status_counts = {row[0]: row[1] for row in status_counts_raw}
    
    return render_template('admin_dashboard.html',
                         total_projects=total_projects,
                         active_projects=active_projects,
                         completed_projects=completed_projects,
                         total_billed=total_billed,
                         recent_projects=recent_projects,
                         status_counts=status_counts)

@app.route('/employee/dashboard')
@login_required
def employee_dashboard():
    if current_user.role != 'employee':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Get assigned projects
    assigned_projects = db.session.query(Project).join(Assignment).filter(Assignment.user_id == current_user.id).all()
    
    # Calculate weekly and monthly hours
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    
    weekly_hours = db.session.query(db.func.sum(Timesheet.hours_worked)).filter(
        Timesheet.user_id == current_user.id,
        Timesheet.date >= week_start
    ).scalar() or 0
    
    monthly_hours = db.session.query(db.func.sum(Timesheet.hours_worked)).filter(
        Timesheet.user_id == current_user.id,
        Timesheet.date >= month_start
    ).scalar() or 0
    
    return render_template('employee_dashboard.html',
                         assigned_projects=assigned_projects,
                         weekly_hours=weekly_hours,
                         monthly_hours=monthly_hours)

@app.route('/admin/projects')
@login_required
def admin_projects():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    projects = Project.query.all()
    return render_template('admin_projects.html', projects=projects)

@app.route('/admin/projects/create', methods=['GET', 'POST'])
@login_required
def create_project():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        name = request.form['name']
        client = request.form['client']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = request.form.get('end_date') or None
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        hourly_rate = float(request.form['hourly_rate'])
        status = request.form['status']
        
        project = Project(name=name, client=client, start_date=start_date, 
                         end_date=end_date, hourly_rate=hourly_rate, status=status)
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('create_project.html')

@app.route('/admin/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        project.name = request.form['name']
        project.client = request.form['client']
        project.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = request.form.get('end_date')
        if end_date:
            project.end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            project.end_date = None
        project.hourly_rate = float(request.form['hourly_rate'])
        project.status = request.form['status']
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('edit_project.html', project=project)

@app.route('/admin/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    project = Project.query.get_or_404(project_id)
    
    # Delete related records first
    Assignment.query.filter_by(project_id=project_id).delete()
    Timesheet.query.filter_by(project_id=project_id).delete()
    Billing.query.filter_by(project_id=project_id).delete()
    
    # Delete the project
    db.session.delete(project)
    db.session.commit()
    
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin_projects'))

@app.route('/admin/assignments/<int:assignment_id>/delete', methods=['POST'])
@login_required
def delete_assignment(assignment_id):
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    db.session.delete(assignment)
    db.session.commit()
    
    flash('Assignment removed successfully!', 'success')
    return redirect(url_for('admin_assignments'))

@app.route('/timesheet')
@login_required
def timesheet():
    if current_user.role != 'employee':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Get assigned projects
    assigned_projects = db.session.query(Project).join(Assignment).filter(Assignment.user_id == current_user.id).all()
    
    # Get timesheet entries
    timesheets = db.session.query(Timesheet).filter(Timesheet.user_id == current_user.id).order_by(Timesheet.date.desc()).all()
    
    # Calculate weekly and monthly hours
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    
    weekly_hours = db.session.query(db.func.sum(Timesheet.hours_worked)).filter(
        Timesheet.user_id == current_user.id,
        Timesheet.date >= week_start
    ).scalar() or 0
    
    monthly_hours = db.session.query(db.func.sum(Timesheet.hours_worked)).filter(
        Timesheet.user_id == current_user.id,
        Timesheet.date >= month_start
    ).scalar() or 0
    
    return render_template('timesheet.html',
                         assigned_projects=assigned_projects,
                         timesheets=timesheets,
                         weekly_hours=weekly_hours,
                         monthly_hours=monthly_hours)

@app.route('/timesheet/log', methods=['POST'])
@login_required
def log_hours():
    if current_user.role != 'employee':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    project_id = request.form['project_id']
    date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    hours_worked = float(request.form['hours_worked'])
    description = request.form.get('description', '')
    
    # Check if user is assigned to this project
    assignment = Assignment.query.filter_by(project_id=project_id, user_id=current_user.id).first()
    if not assignment:
        flash('You are not assigned to this project', 'error')
        return redirect(url_for('timesheet'))
    
    # Check if timesheet entry already exists for this date and project
    existing_entry = Timesheet.query.filter_by(
        project_id=project_id, user_id=current_user.id, date=date
    ).first()
    
    if existing_entry:
        flash('Timesheet entry already exists for this date and project', 'error')
    else:
        timesheet = Timesheet(project_id=project_id, user_id=current_user.id,
                             date=date, hours_worked=hours_worked, description=description)
        db.session.add(timesheet)
        db.session.commit()
        flash('Hours logged successfully!', 'success')
    
    return redirect(url_for('timesheet'))

@app.route('/admin/assignments')
@login_required
def admin_assignments():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    assignments = db.session.query(Assignment, Project, User).join(Project).join(User).all()
    projects = Project.query.all()
    employees = User.query.filter_by(role='employee').all()
    
    return render_template('admin_assignments.html',
                         assignments=assignments,
                         projects=projects,
                         employees=employees)

@app.route('/admin/assignments/create', methods=['POST'])
@login_required
def create_assignment():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    project_id = request.form['project_id']
    user_id = request.form['user_id']
    
    # Check if assignment already exists
    existing = Assignment.query.filter_by(project_id=project_id, user_id=user_id).first()
    if existing:
        flash('Assignment already exists', 'error')
    else:
        assignment = Assignment(project_id=project_id, user_id=user_id)
        db.session.add(assignment)
        db.session.commit()
        flash('Assignment created successfully!', 'success')
    
    return redirect(url_for('admin_assignments'))

@app.route('/admin/billing')
@login_required
def admin_billing():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Get projects with billing information
    projects_billing = []
    projects = Project.query.all()
    
    total_all_hours = 0
    total_all_amount = 0
    
    for project in projects:
        total_hours = db.session.query(db.func.sum(Timesheet.hours_worked)).filter(
            Timesheet.project_id == project.id
        ).scalar() or 0
        
        total_amount = total_hours * project.hourly_rate
        projects_billing.append((project, total_hours, total_amount))
        
        total_all_hours += total_hours
        total_all_amount += total_amount
    
    top_projects = sorted(
        (row for row in projects_billing if row[2] > 0),
        key=lambda row: row[2],
        reverse=True
    )[:5]
    billing_chart_data = [
        {'name': project.name, 'hours': total_hours, 'amount': total_amount}
        for project, total_hours, total_amount in projects_billing
    ]

    # Calculate average rate safely
    average_rate = total_all_amount / total_all_hours if total_all_hours > 0 else 0
    
    return render_template('admin_billing.html', 
                         projects_billing=projects_billing,
                         total_all_hours=total_all_hours,
                         total_all_amount=total_all_amount,
                         average_rate=average_rate,
                         top_projects=top_projects,
                         billing_chart_data=billing_chart_data)

@app.route('/admin/billing/generate', methods=['POST'])
@login_required
def generate_billing():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    project_id = request.form.get('project_id')
    if not project_id:
        flash('Project ID is required', 'error')
        return redirect(url_for('admin_billing'))
    
    project = Project.query.get(project_id)
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('admin_billing'))
    
    # Calculate total hours for the project
    total_hours = db.session.query(db.func.sum(Timesheet.hours_worked)).filter(
        Timesheet.project_id == project_id
    ).scalar() or 0
    
    if total_hours <= 0:
        flash('No hours logged for this project', 'error')
        return redirect(url_for('admin_billing'))
    
    # Calculate total amount
    total_amount = total_hours * project.hourly_rate
    
    # Check if billing record already exists
    existing_billing = Billing.query.filter_by(project_id=project_id).first()
    if existing_billing:
        flash('Billing record already exists for this project', 'error')
        return redirect(url_for('admin_billing'))
    
    # Create billing record
    billing = Billing(
        project_id=project_id,
        total_hours=total_hours,
        total_amount=total_amount,
        billing_date=datetime.now().date()
    )
    
    db.session.add(billing)
    db.session.commit()
    
    flash(f'Billing record generated successfully! Total: ${total_amount:.2f}', 'success')
    return redirect(url_for('admin_billing'))

@app.route('/api/search_projects')
@login_required
def search_projects():
    if current_user.role != 'admin':
        return jsonify([])
    
    query = request.args.get('q', '')
    status = request.args.get('status', '')
    
    projects_query = Project.query
    
    if query:
        projects_query = projects_query.filter(
            db.or_(
                Project.name.contains(query),
                Project.client.contains(query)
            )
        )
    
    if status:
        projects_query = projects_query.filter(Project.status == status)
    
    projects = projects_query.all()
    
    result = []
    for project in projects:
        result.append({
            'id': project.id,
            'name': project.name,
            'client': project.client,
            'status': project.status,
            'start_date': project.start_date.strftime('%Y-%m-%d'),
            'end_date': project.end_date.strftime('%Y-%m-%d') if project.end_date else None,
            'hourly_rate': project.hourly_rate
        })
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
