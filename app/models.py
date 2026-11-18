from . import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<User {self.name}>"



class StudentProfile(db.Model):
    __tablename__ = 'student_profile'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    major = db.Column(db.String(100))
    bio = db.Column(db.Text)
    graduation_year = db.Column(db.Integer)

class AdminProfile(db.Model):
    __tablename__ = 'admin_profile'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    department = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))

class Company(db.Model):
    __tablename__ = 'company'
    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100))
    location = db.Column(db.String(100))
    contact_email = db.Column(db.String(100))

class Job(db.Model):
    __tablename__ = 'job'
    job_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    salary = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    company = db.relationship('Company', backref='jobs')
    admin = db.relationship('User', backref='posted_jobs')

    # Define applications relationship without backref here
    applications = db.relationship(
        'Application',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy=True
    )



class Application(db.Model):
    __tablename__ = 'applications'

    student_id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.job_id', ondelete='CASCADE'), primary_key=True)
    cover_letter = db.Column(db.Text)
    status = db.Column(db.String(20), server_default='pending')
    applied_at = db.Column(db.DateTime, server_default=db.func.now())

    # Job relationship without backref (avoid naming conflict)
    job = db.relationship('Job', passive_deletes=True)

    student = db.relationship(
        'User',
        foreign_keys=[student_id],
        backref=db.backref('job_applications', lazy=True),
        primaryjoin="Application.student_id == User.user_id"
    )

class JobInterview(db.Model):
    __tablename__ = 'job_interview'

    interview_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)

    # Relationships
    student = db.relationship('User', foreign_keys=[student_id], backref='interviews')
    job = db.relationship('Job', backref='interviews')

    def __repr__(self):
        return f"<Interview {self.interview_id} | Student {self.student_id} | Job {self.job_id}>"
