from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id             = db.Column(db.Integer, primary_key=True)
    username       = db.Column(db.String(80), unique=True, nullable=False)
    email          = db.Column(db.String(120), unique=True, nullable=False)
    password       = db.Column(db.String(200), nullable=False)
    role           = db.Column(db.String(20), nullable=False)
    is_active      = db.Column(db.Boolean, default=True)
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)

class StudentProfile(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    name        = db.Column(db.String(100))
    dob         = db.Column(db.String(20))
    college     = db.Column(db.String(200))
    branch      = db.Column(db.String(100))
    gpa         = db.Column(db.Float)
    year        = db.Column(db.Integer)
    address     = db.Column(db.String(300))
    resume_path = db.Column(db.String(300))
    user        = db.relationship('User', backref='student_profile')

class CompanyProfile(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    name            = db.Column(db.String(200))
    hr_contact      = db.Column(db.String(200))
    website         = db.Column(db.String(200))
    established_in  = db.Column(db.String(20))
    sector          = db.Column(db.String(100))
    approval_status = db.Column(db.String(20), default='pending')
    user            = db.relationship('User', backref='company_profile')

class PlacementDrive(db.Model):
    id                 = db.Column(db.Integer, primary_key=True)
    company_id         = db.Column(db.Integer, db.ForeignKey('user.id'))
    job_title          = db.Column(db.String(200))
    job_description    = db.Column(db.Text)
    eligibility_branch = db.Column(db.String(100))
    eligibility_gpa    = db.Column(db.Float)
    eligibility_year   = db.Column(db.Integer)
    deadline           = db.Column(db.DateTime)
    status             = db.Column(db.String(20), default='pending')
    created_at         = db.Column(db.DateTime, default=datetime.utcnow)
    company            = db.relationship('User', backref='drives')

class Application(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    student_id  = db.Column(db.Integer, db.ForeignKey('user.id'))
    drive_id    = db.Column(db.Integer, db.ForeignKey('placement_drive.id'))
    applied_at  = db.Column(db.DateTime, default=datetime.utcnow)
    status      = db.Column(db.String(20), default='applied')
    result_date = db.Column(db.DateTime)
    student     = db.relationship('User', backref='applications')
    drive       = db.relationship('PlacementDrive', backref='applications')
    __table_args__ = (db.UniqueConstraint('student_id', 'drive_id'),)

class Interview(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    application_id  = db.Column(db.Integer, db.ForeignKey('application.id'), unique=True)
    student_id      = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_id      = db.Column(db.Integer, db.ForeignKey('user.id'))
    scheduled_date  = db.Column(db.String(20))
    scheduled_time  = db.Column(db.String(20))
    location        = db.Column(db.String(200))
    mode            = db.Column(db.String(20), default='online')
    result          = db.Column(db.String(20), default='pending')
    notes           = db.Column(db.Text)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at      = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    application     = db.relationship('Application', backref='interview')
    student         = db.relationship('User', foreign_keys=[student_id], backref='student_interviews')
    company         = db.relationship('User', foreign_keys=[company_id], backref='company_interviews')
