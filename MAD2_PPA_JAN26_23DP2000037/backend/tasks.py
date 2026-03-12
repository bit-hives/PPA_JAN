from celery_worker import celery
from celery.schedules import crontab
from flask_mail import Message
from datetime import datetime, timedelta
import csv, io

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=8, minute=0), send_deadline_reminders.s())
    sender.add_periodic_task(crontab(hour=9, minute=0, day_of_month=1), send_monthly_report.s())

@celery.task
def send_deadline_reminders():
    from app import mail
    from models import PlacementDrive, Application, User
    tomorrow = datetime.utcnow() + timedelta(days=1)
    for drive in PlacementDrive.query.filter(PlacementDrive.deadline <= tomorrow, PlacementDrive.status == 'approved').all():
        for app in Application.query.filter_by(drive_id=drive.id, status='applied').all():
            student = User.query.get(app.student_id)
            mail.send(Message(
                subject=f"Reminder: {drive.job_title} deadline is tomorrow!",
                recipients=[student.email],
                body=f"Hi {student.username}, the deadline for '{drive.job_title}' is tomorrow."))

@celery.task
def send_monthly_report():
    from app import mail
    from models import User, PlacementDrive, Application
    admin = User.query.filter_by(role='admin').first()
    now = datetime.utcnow()
    start = now.replace(day=1, hour=0, minute=0, second=0)
    drives = PlacementDrive.query.filter(PlacementDrive.created_at >= start).count()
    applied = Application.query.filter(Application.applied_at >= start).count()
    selected = Application.query.filter(Application.applied_at >= start, Application.status == 'selected').count()
    mail.send(Message(subject=f"Monthly Report — {now.strftime('%B %Y')}", recipients=[admin.email], html=html))

@celery.task
def export_student_csv(student_id):
    from app import mail
    from models import User, Application, PlacementDrive, CompanyProfile
    student = User.query.get(student_id)
    apps = Application.query.filter_by(student_id=student_id).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Company', 'Drive', 'Applied', 'Result Date', 'Status'])
    for a in apps:
        drive = PlacementDrive.query.get(a.drive_id)
        company = CompanyProfile.query.filter_by(user_id=drive.company_id).first() if drive else None
        writer.writerow([a.id, company.name if company else 'N/A', drive.job_title if drive else 'N/A',
                         a.applied_at.strftime('%Y-%m-%d') if a.applied_at else '',
                         a.result_date.strftime('%Y-%m-%d') if a.result_date else '', a.status])
    msg = Message(subject="Your Placement History CSV", recipients=[student.email], body="CSV attached.")
    msg.attach("placement_history.csv", "text/csv", output.getvalue())
    mail.send(msg)


@celery.task
def export_admin_data_csv():
    from app import mail
    from models import User, StudentProfile, CompanyProfile, PlacementDrive, Application
    admin = User.query.filter_by(role='admin').first()
    
    output = io.StringIO()
    writer = csv.writer(output)
    

    writer.writerow(['===== STUDENTS ====='])
    writer.writerow(['ID', 'Username', 'Email', 'Name', 'College', 'Branch', 'GPA', 'Year'])
    students = User.query.filter_by(role='student').all()
    for student in students:
        profile = StudentProfile.query.filter_by(user_id=student.id).first()
        writer.writerow([
            student.id,
            student.username,
            student.email,
            profile.name if profile else '',
            profile.college if profile else '',
            profile.branch if profile else '',
            profile.gpa if profile else '',
            profile.year if profile else ''
        ])
    
    writer.writerow([])
    writer.writerow(['===== COMPANIES ====='])
    writer.writerow(['ID', 'Username', 'Email', 'Name', 'HR Contact', 'Website', 'Sector', 'Status'])
    companies = User.query.filter_by(role='company').all()
    for company in companies:
        profile = CompanyProfile.query.filter_by(user_id=company.id).first()
        writer.writerow([
            company.id,
            company.username,
            company.email,
            profile.name if profile else '',
            profile.hr_contact if profile else '',
            profile.website if profile else '',
            profile.sector if profile else '',
            profile.approval_status if profile else ''
        ])
    
    writer.writerow([])
    writer.writerow(['===== PLACEMENT DRIVES ====='])
    writer.writerow(['ID', 'Company', 'Job Title', 'Deadline', 'Status', 'Created At'])
    drives = PlacementDrive.query.all()
    for drive in drives:
        company = CompanyProfile.query.filter_by(user_id=drive.company_id).first()
        writer.writerow([
            drive.id,
            company.name if company else 'N/A',
            drive.job_title,
            drive.deadline.strftime('%Y-%m-%d') if drive.deadline else '',
            drive.status,
            drive.created_at.strftime('%Y-%m-%d') if drive.created_at else ''
        ])
    
    writer.writerow([])
    writer.writerow(['===== APPLICATIONS ====='])
    writer.writerow(['ID', 'Student', 'Drive', 'Company', 'Applied At', 'Status', 'Result Date'])
    applications = Application.query.all()
    for app in applications:
        student = User.query.get(app.student_id)
        drive = PlacementDrive.query.get(app.drive_id)
        company = CompanyProfile.query.filter_by(user_id=drive.company_id).first() if drive else None
        writer.writerow([
            app.id,
            student.username if student else 'N/A',
            drive.job_title if drive else 'N/A',
            company.name if company else 'N/A',
            app.applied_at.strftime('%Y-%m-%d') if app.applied_at else '',
            app.status,
            app.result_date.strftime('%Y-%m-%d') if app.result_date else ''
        ])
    
    msg = Message(subject="Placement Portal - Complete Data Export", recipients=[admin.email], body="CSV export attached.")
    msg.attach("placement_data_export.csv", "text/csv", output.getvalue())
    mail.send(msg)
