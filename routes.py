from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from app import app, db, User, Project, Assignment, Timesheet, Billing

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
            flash('Login successful!', 'success')
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
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('signup.html')
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
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
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    # Get dashboard statistics
    total_projects = Project.query.count()
    active_projects = Project.query.filter_by(status='active').count()
    completed_projects = Project.query.filter_by(status='completed').count()
    
    # Calculate total billed amount
    total_billed = db.session.query(db.func.sum(Billing.total_amount)).scalar() or 0
    
    # Get project status data for chart
    status_counts = db.session.query(
        Project.status, 
        db.func.count(Project.id)
    ).group_by(Project.status).all()
    
    # Get recent projects
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
    
    return render_template('admin_dashboard.html',
                         total_projects=total_projects,
                         active_projects=active_projects,
                         completed_projects=completed_projects,
                         total_billed=total_billed,
                         status_counts=status_counts,
                         recent_projects=recent_projects)

@app.route('/employee/dashboard')
@login_required
def employee_dashboard():
    if current_user.role != 'employee':
        flash('Access denied. Employee privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    # Get assigned projects
    assigned_projects = db.session.query(Project).join(Assignment).filter(
        Assignment.user_id == current_user.id
    ).all()
    
    # Get hours logged this week
    week_start = date.today() - timedelta(days=date.today().weekday())
    week_end = week_start + timedelta(days=6)
    
    weekly_hours = db.session.query(db.func.sum(Timesheet.hours_worked)).filter(
        Timesheet.user_id == current_user.id,
        Timesheet.date >= week_start,
        Timesheet.date <= week_end
    ).scalar() or 0
    
    # Get hours logged this month
    month_start = date.today().replace(day=1)
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
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    projects = Project.query.all()
    return render_template('admin_projects.html', projects=projects)

@app.route('/admin/projects/create', methods=['GET', 'POST'])
@login_required
def create_project():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        name = request.form['name']
        client = request.form['client']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date() if request.form['end_date'] else None
        hourly_rate = float(request.form['hourly_rate'])
        
        new_project = Project(
            name=name,
            client=client,
            start_date=start_date,
            end_date=end_date,
            hourly_rate=hourly_rate
        )
        db.session.add(new_project)
        db.session.commit()
        
        flash('Project created successfully!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('create_project.html')

@app.route('/admin/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        project.name = request.form['name']
        project.client = request.form['client']
        project.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        project.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date() if request.form['end_date'] else None
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
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin_projects'))

@app.route('/admin/assignments')
@login_required
def admin_assignments():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    assignments = db.session.query(Assignment, Project, User).join(
        Project, Assignment.project_id == Project.id
    ).join(
        User, Assignment.user_id == User.id
    ).all()
    
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
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    project_id = int(request.form['project_id'])
    user_id = int(request.form['user_id'])
    
    # Check if assignment already exists
    existing = Assignment.query.filter_by(project_id=project_id, user_id=user_id).first()
    if existing:
        flash('Assignment already exists!', 'error')
    else:
        new_assignment = Assignment(project_id=project_id, user_id=user_id)
        db.session.add(new_assignment)
        db.session.commit()
        flash('Assignment created successfully!', 'success')
    
    return redirect(url_for('admin_assignments'))

@app.route('/admin/assignments/<int:assignment_id>/delete', methods=['POST'])
@login_required
def delete_assignment(assignment_id):
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    db.session.delete(assignment)
    db.session.commit()
    
    flash('Assignment deleted successfully!', 'success')
    return redirect(url_for('admin_assignments'))

@app.route('/timesheet')
@login_required
def timesheet():
    # Get assigned projects for current user
    assigned_projects = db.session.query(Project).join(Assignment).filter(
        Assignment.user_id == current_user.id
    ).all()
    
    # Get timesheet entries for current user
    timesheets = Timesheet.query.filter_by(user_id=current_user.id).order_by(Timesheet.date.desc()).all()
    
    return render_template('timesheet.html', 
                         assigned_projects=assigned_projects,
                         timesheets=timesheets)

@app.route('/timesheet/log', methods=['POST'])
@login_required
def log_hours():
    project_id = int(request.form['project_id'])
    date_str = request.form['date']
    hours_worked = float(request.form['hours_worked'])
    description = request.form.get('description', '')
    
    # Check if user is assigned to this project
    assignment = Assignment.query.filter_by(
        project_id=project_id, 
        user_id=current_user.id
    ).first()
    
    if not assignment:
        flash('You are not assigned to this project!', 'error')
        return redirect(url_for('timesheet'))
    
    # Check if timesheet entry already exists for this date and project
    existing = Timesheet.query.filter_by(
        project_id=project_id,
        user_id=current_user.id,
        date=datetime.strptime(date_str, '%Y-%m-%d').date()
    ).first()
    
    if existing:
        flash('Timesheet entry already exists for this date and project!', 'error')
    else:
        new_timesheet = Timesheet(
            project_id=project_id,
            user_id=current_user.id,
            date=datetime.strptime(date_str, '%Y-%m-%d').date(),
            hours_worked=hours_worked,
            description=description
        )
        db.session.add(new_timesheet)
        db.session.commit()
        flash('Hours logged successfully!', 'success')
    
    return redirect(url_for('timesheet'))

@app.route('/admin/billing')
@login_required
def admin_billing():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    # Get all projects with billing information
    projects_billing = db.session.query(
        Project,
        db.func.sum(Timesheet.hours_worked).label('total_hours'),
        db.func.sum(Timesheet.hours_worked * Project.hourly_rate).label('total_amount')
    ).outerjoin(Timesheet, Project.id == Timesheet.project_id).group_by(Project.id).all()
    
    # Calculate totals for summary cards
    total_all_hours = 0
    total_all_amount = 0
    
    for project, total_hours, total_amount in projects_billing:
        if total_hours:
            total_all_hours += total_hours
        if total_amount:
            total_all_amount += total_amount
    
    # Calculate average rate
    average_rate = total_all_amount / total_all_hours if total_all_hours > 0 else 0
    
    return render_template('admin_billing.html', 
                         projects_billing=projects_billing,
                         total_all_hours=total_all_hours,
                         total_all_amount=total_all_amount,
                         average_rate=average_rate)

@app.route('/admin/billing/generate', methods=['POST'])
@login_required
def generate_billing():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    project_id = int(request.form['project_id'])
    
    # Calculate total hours and amount for the project
    result = db.session.query(
        db.func.sum(Timesheet.hours_worked).label('total_hours'),
        db.func.sum(Timesheet.hours_worked * Project.hourly_rate).label('total_amount')
    ).join(Project, Timesheet.project_id == Project.id).filter(
        Timesheet.project_id == project_id
    ).first()
    
    if result.total_hours:
        # Create billing record
        billing_record = Billing(
            project_id=project_id,
            total_hours=result.total_hours,
            total_amount=result.total_amount,
            billing_date=date.today()
        )
        db.session.add(billing_record)
        db.session.commit()
        flash('Billing record generated successfully!', 'success')
    else:
        flash('No hours logged for this project!', 'error')
    
    return redirect(url_for('admin_billing'))

@app.route('/api/search_projects')
@login_required
def search_projects():
    query = request.args.get('q', '').lower()
    status_filter = request.args.get('status', '')
    
    projects_query = Project.query
    
    if query:
        projects_query = projects_query.filter(
            db.or_(
                Project.name.ilike(f'%{query}%'),
                Project.client.ilike(f'%{query}%')
            )
        )
    
    if status_filter:
        projects_query = projects_query.filter(Project.status == status_filter)
    
    projects = projects_query.all()
    
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'client': p.client,
        'status': p.status,
        'start_date': p.start_date.strftime('%Y-%m-%d'),
        'end_date': p.end_date.strftime('%Y-%m-%d') if p.end_date else None,
        'hourly_rate': float(p.hourly_rate)
    } for p in projects])


