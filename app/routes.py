from datetime import datetime
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, StudentProfile, AdminProfile, Job, Application, Company, JobInterview

from sqlalchemy.exc import IntegrityError
from flask_login import login_required, current_user
from sqlalchemy import text




main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            password = generate_password_hash(request.form['password'])
            role = request.form['role']

            user = User(name=name, email=email, password=password, role=role)
            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.user_id
            session['role'] = user.role
            flash('Account created successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating account: ' + str(e), 'danger')

    return render_template('signup.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.user_id
            session['role'] = user.role
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        
        flash('Invalid email or password', 'danger')

    return render_template('login.html')

@main.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    role = session.get('role')
    if role == 'student':
        return redirect(url_for('main.student_view'))
    elif role == 'admin':
        return redirect(url_for('main.admin_view'))  # Changed to use admin_view
    else:
        return redirect(url_for('main.login'))
@main.route('/admin/view')
def admin_view():
    if session.get('role') != 'admin':
        return redirect(url_for('main.login'))
    
    return render_template('admin_view.html')


@main.route('/student_view')
def student_view():
    if session.get('role') != 'student':
        return redirect(url_for('main.login'))

    search_query = request.args.get('search', '').strip()
    user_id = session.get('user_id')

    # Query jobs
    if search_query:
        jobs = Job.query.filter(
            Job.title.ilike(f'%{search_query}%') |
            Job.description.ilike(f'%{search_query}%')
        ).all()
    else:
        jobs = Job.query.all()

    # Query applications (joined with jobs for display)
    applications = Application.query.filter_by(student_id=user_id).join(Job).all()
    interviews = JobInterview.query.filter_by(student_id=user_id).join(Job).all()

    return render_template('student_view.html', jobs=jobs, applications=applications, interviews=interviews,search_query=search_query)

@main.route('/student_profile')
def student_profile():
    if session.get('role') != 'student':
        return redirect(url_for('main.login'))

    user_id = session.get('user_id')
    if not user_id:
        flash("No user ID in session. Please log in again.", "error")
        return redirect(url_for('main.login'))

    student = StudentProfile.query.filter_by(user_id=user_id).first()
    user = User.query.get(user_id)

    return render_template(
        'student_profile.html',
        name=user.name if user else None,
        email=user.email if user else None,
        major=student.major if student else None,
        graduation_year=student.graduation_year if student else None,
        bio=student.bio if student else None
    )

@main.route('/admin_profile')
def admin_profile():
    if session.get('role') != 'admin':
        return redirect(url_for('main.login'))

    user_id = session.get('user_id')
    if not user_id:
        flash("No user ID in session. Please log in again.", "error")
        return redirect(url_for('main.login'))

    admin = AdminProfile.query.filter_by(user_id=user_id).first()
    user = User.query.get(user_id)

    return render_template(
        'admin_profile.html',
        admin_user=user,  # <- this is the missing context
        admin_profile=admin  # optional: rename for clarity
    )


@main.route('/admin/create_job', methods=['GET', 'POST'])
def create_job():
    if session.get('role') != 'admin':
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        try:
            company_id = request.form['company_id']
            title = request.form['title']
            description = request.form['description']
            location = request.form['location']
            salary = request.form['salary']
            admin_id = session.get('user_id')

            job = Job(
                company_id=company_id,
                title=title,
                description=description,
                location=location,
                salary=salary,
                admin_id=admin_id
            )

            db.session.add(job)
            db.session.commit()
            flash('Job created successfully!', 'success')
            return redirect(url_for('main.admin_view'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating job: ' + str(e), 'danger')

    return render_template('add_job.html')
@main.route('/admin/jobs')
def admin_jobs():
    if session.get('role') != 'admin':
        return redirect(url_for('main.login'))

    # Fetch jobs added by the logged-in admin
    jobs = Job.query.filter_by(admin_id=session['user_id']).all()
    return render_template('admin_jobs.html', jobs=jobs)


@main.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if session.get('role') != 'admin':
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        try:
            # Retrieve form data
            company_id = request.form['company_id']
            title = request.form['title']
            description = request.form['description']
            location = request.form['location']
            salary = request.form['salary']
            admin_id = session['user_id']  # Use the logged-in admin's user_id

            # Create a new job instance
            new_job = Job(
                company_id=company_id,
                title=title,
                description=description,
                location=location,
                salary=salary,
                admin_id=admin_id
            )

            # Add the job to the database
            db.session.add(new_job)
            db.session.commit()

            flash('Job added successfully!', 'success')
            return redirect(url_for('main.admin_jobs'))  # Redirect to the jobs list page
        except Exception as e:
            db.session.rollback()
            flash('Error adding job: ' + str(e), 'danger')

    return render_template('add_job.html')

@main.route('/admin/jobs/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    if session.get('role') != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.login'))

    job = Job.query.get_or_404(job_id)

    try:
        db.session.delete(job)
        db.session.commit()
        flash('Job deleted successfully.', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Error occurred while deleting the job.', 'danger')

    return redirect(url_for('main.admin_jobs'))


@main.route('/admin/jobs/edit/<int:job_id>', methods=['GET', 'POST'])
def update_job(job_id):
    # Check if user is an admin using session
    if session.get('role') != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.login'))

    job = Job.query.get_or_404(job_id)

    if request.method == 'POST':
        try:
            # Update job fields from form data
            job.title = request.form['title']
            job.description = request.form['description']
            job.location = request.form['location']
            job.salary = request.form['salary']
            job.company_id = request.form['company_id']

            db.session.commit()
            flash('Job updated successfully.', 'success')
            return redirect(url_for('main.admin_jobs'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating job: {str(e)}', 'danger')

    return render_template('edit_job.html', job=job)


@main.route('/student/apply/<int:job_id>', methods=['GET', 'POST'])
def student_apply(job_id):
    if session.get('role') != 'student':
        return redirect(url_for('main.login'))

    job = Job.query.get_or_404(job_id)

    if request.method == 'POST':
        student_id = session.get('user_id')
        cover_letter = request.form.get('cover_letter')

        existing_application = Application.query.filter_by(student_id=student_id, job_id=job_id).first()
        if existing_application:
            flash('You have already applied for this job.', 'warning')
        else:
            application = Application(student_id=student_id, job_id=job_id, cover_letter=cover_letter)
            db.session.add(application)
            db.session.commit()
            flash('Application submitted successfully!', 'success')
            return redirect(url_for('main.student_view'))

    return render_template('student_apply.html', job=job)




@main.route('/view_applications')
def view_applications():
    # Fetch applications along with related student and job information
    applications = Application.query.join(User, User.user_id == Application.student_id) \
                                     .join(Job, Job.job_id == Application.job_id) \
                                     .all()

    return render_template('view_applications.html', applications=applications)

@main.route('/update_application_status/<int:student_id>/<int:job_id>/<action>', methods=['POST'])
def update_application_status(student_id, job_id, action):
    # Check the action (accept or decline)
    if action not in ['accept', 'decline']:
        flash('Invalid action', 'danger')
        return redirect(url_for('main.view_applications'))

    # Find the application based on student_id and job_id
    application = Application.query.filter_by(student_id=student_id, job_id=job_id).first()

    if not application:
        flash('Application not found', 'danger')
        return redirect(url_for('main.view_applications'))

    # Update the status based on the action
    if action == 'accept':
        application.status = 'approved'
    elif action == 'decline':
        application.status = 'rejected'

    # Commit the changes to the database
    db.session.commit()
    flash(f'Application {action}ed successfully', 'success')

    # Redirect back to the applications page
    return redirect(url_for('main.view_applications'))


@main.route('/update_student_profile', methods=['GET', 'POST'])
def update_student_profile():
    if session.get('role') != 'student':
        return redirect(url_for('main.login'))

    user_id = session.get('user_id')
    student = StudentProfile.query.filter_by(user_id=user_id).first()

    if not student:
        # Create a new StudentProfile for the user if it doesn't exist
        student = StudentProfile(user_id=user_id, major=None, graduation_year=None, bio=None)
        db.session.add(student)
        db.session.commit()

    if request.method == 'POST':
        student.major = request.form.get('major')
        student.graduation_year = request.form.get('graduation_year')
        student.bio = request.form.get('bio')

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for('main.student_profile'))

    return render_template('update_student_profile.html', student=student)


@main.route('/update_admin_profile', methods=['GET', 'POST'])
def update_admin_profile():
    if session.get('role') != 'admin':
        return redirect(url_for('main.login'))

    user_id = session.get('user_id')
    admin = AdminProfile.query.filter_by(user_id=user_id).first()

    if not admin:
        # Create profile if it doesn't exist yet
        admin = AdminProfile(user_id=user_id, department=None, phone_number=None)
        db.session.add(admin)
        db.session.commit()

    if request.method == 'POST':
        admin.department = request.form.get('department')
        admin.phone_number = request.form.get('phone_number')

        db.session.commit()
        flash("Admin profile updated successfully.", "success")
        return redirect(url_for('main.admin_profile'))

    return render_template('update_admin_profile.html', admin=admin)

@main.route('/aboutus')
def about_us():
    return render_template('aboutus.html')


@main.route('/admin/schedule_interview', methods=['GET', 'POST'])
def schedule_interview():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        job_id = request.form.get('job_id')
        scheduled_time = request.form.get('scheduled_time')

        interview = JobInterview(
            student_id=student_id,
            job_id=job_id,
            scheduled_time=datetime.strptime(scheduled_time, '%Y-%m-%dT%H:%M')
        )
        db.session.add(interview)
        db.session.commit()
        flash('Interview scheduled successfully!', 'success')
        return redirect(url_for('main.schedule_interview'))

    # Get accepted applications
    approved_applications = Application.query.filter_by(status='approved').all()
    return render_template('job_interview.html', applications=approved_applications)

@main.route('/admin/interviews')
def admin_view_interviews():
    interviews = JobInterview.query.all()
    return render_template('admin_view_interviews.html', interviews=interviews)

@main.route('/view_companies')
def view_companies():
    if session.get('role') != 'student':
        return redirect(url_for('main.login'))

    companies = Company.query.all()
    return render_template('view_companies.html', companies=companies)
