from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User, StudentProfile, CompanyProfile, PlacementDrive, Application, Interview
from functools import wraps
from datetime import datetime
import os

bp = Blueprint('api', __name__)

def cached(timeout=300, query_string=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                cache_obj = current_app.extensions.get('cache')
                if not cache_obj:
                    return f(*args, **kwargs)
                cache_key = f.__name__
                if query_string:
                    query_params = request.args.to_dict(flat=False)
                    if query_params:
                        query_string_key = '_'.join([f"{k}_{v[0]}" for k, v in sorted(query_params.items())])
                        cache_key = f"{cache_key}_{query_string_key}"
                result = cache_obj.get(cache_key)
                if result is not None:
                    return result
                result = f(*args, **kwargs)
                cache_obj.set(cache_key, result, timeout=timeout)
                return result
            except Exception as e:
                print(f"Cache error: {e}")
                return f(*args, **kwargs)
        return decorated_function
    return decorator

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            if get_jwt().get('role') != role:
                return jsonify({'error': 'Unauthorized'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

admin_required = role_required('admin')
student_required = role_required('student')
company_required = role_required('company')

def invalidate_admin_caches():
    try:
        cache_obj = current_app.extensions.get('cache')
        if cache_obj:
            cache_obj.delete('admin_stats')
            cache_obj.delete('admin_chart_data')
            cache_obj.delete('admin_monthly_chart_data')
    except Exception as e:
        print(f"Cache invalidation error: {e}")

def invalidate_student_drives_cache():
    try:
        cache_obj = current_app.extensions.get('cache')
        if cache_obj:
            cache_obj.delete('student_drives')
    except Exception as e:
        print(f"Cache invalidation error: {e}")

def invalidate_company_caches(company_id=None):
    try:
        cache_obj = current_app.extensions.get('cache')
        if cache_obj:
            if company_id:
                cache_obj.delete(f'company_stats_{company_id}')
                cache_obj.delete(f'company_drives_{company_id}')
            cache_obj.delete('admin_companies')
    except Exception as e:
        print(f"Cache invalidation error: {e}")



@bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    identifier = data.get('username') or data.get('email')
    user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()
    if not user or not check_password_hash(user.password, data.get('password', '')):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if user.role == 'company':
        c_prof = CompanyProfile.query.filter_by(user_id=user.id).first()
    if not user.is_active or user.is_blacklisted:
        return jsonify({'error': 'Account suspended'}), 403
        
    token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
    return jsonify({'token': token, 'role': user.role, 'username': user.username})

@bp.route('/auth/register/student', methods=['POST'])
def register_student():
    data = request.form if request.form else request.get_json()
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Email already exists'}), 400
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'error': 'Username already exists'}), 400
        
    user = User(username=data.get('username'), email=data.get('email'),
                password=generate_password_hash(data.get('password')), role='student')
    db.session.add(user)
    db.session.flush()
    
    resume_path = ''
    if 'resume' in request.files:
        f = request.files['resume']
        if f.filename:
            upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            path = os.path.join(upload_dir, f'{user.id}_{f.filename}')
            f.save(path)
            resume_path = path

    db.session.add(StudentProfile(user_id=user.id, name=data.get('name'),
        dob=data.get('dob'), college=data.get('college'), gpa=data.get('gpa'),
        branch=data.get('branch'), year=data.get('year'), address=data.get('address'),
        resume_path=resume_path))
    db.session.commit()
    invalidate_admin_caches()
    return jsonify({'message': 'Student registered'}), 201

@bp.route('/auth/register/company', methods=['POST'])
def register_company():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    user = User(username=data['username'], email=data['email'],
                password=generate_password_hash(data['password']), role='company')
    db.session.add(user)
    db.session.flush()
    db.session.add(CompanyProfile(user_id=user.id, name=data.get('name'),
        hr_contact=data.get('hr_contact'), website=data.get('website'),
        established_in=data.get('established_in'), sector=data.get('sector'),
        approval_status='pending'))
    db.session.commit()
    invalidate_admin_caches()
    return jsonify({'message': 'Company registered successfully. You can now login.'}), 201



@bp.route('/admin/stats', methods=['GET'])
@cached(timeout=300)
@admin_required
def admin_stats():
    return jsonify({
        'students': User.query.filter_by(role='student').count(),
        'companies': User.query.filter_by(role='company').count(),
        'active_drives': PlacementDrive.query.filter_by(status='approved').count(),
        'total_drives': PlacementDrive.query.count(),
        'pending_drives': PlacementDrive.query.filter_by(status='pending').count(),
        'total_applications': Application.query.count(),
        'selected': Application.query.filter_by(status='selected').count(),
    })

@bp.route('/admin/profile', methods=['GET'])
@admin_required
def admin_profile():
    admin_id = int(get_jwt_identity())
    admin = User.query.get(admin_id)
    if not admin:
        return jsonify({'error': 'Admin not found'}), 404
    return jsonify({
        'id': admin.id,
        'username': admin.username,
        'email': admin.email,
        'name': admin.username,
        'role': admin.role
    })

@bp.route('/admin/chart-data', methods=['GET'])
@cached(timeout=300)
@admin_required
def admin_chart_data():
    from sqlalchemy import func
    app_counts = db.session.query(Application.status, func.count(Application.id)).group_by(Application.status).all()
    status_data = {s: c for s, c in app_counts}
    
    return jsonify({
        'applications': {
            'labels': ['Applied', 'Shortlisted', 'Selected', 'Rejected'],
            'data': [
                status_data.get('applied', 0),
                status_data.get('shortlisted', 0),
                status_data.get('selected', 0),
                status_data.get('rejected', 0)
            ]
        }
    })

@bp.route('/admin/students', methods=['GET'])
@cached(timeout=300, query_string=True)
@admin_required
def admin_list_students():
    q = request.args.get('q', '')
    query = User.query.filter_by(role='student')
    if q:
        query = query.filter(User.username.contains(q) | User.email.contains(q))
    students = query.all()
    result = []
    for u in students:
        p = StudentProfile.query.filter_by(user_id=u.id).first()
        result.append({
            'id': u.id, 'username': u.username, 'email': u.email,
            'is_active': u.is_active, 'is_blacklisted': u.is_blacklisted,
            'name': p.name if p else '', 'college': p.college if p else '',
            'gpa': p.gpa if p else None, 'branch': p.branch if p else '',
            'year': p.year if p else None,
            'drives_applied': Application.query.filter_by(student_id=u.id).count()
        })
    return jsonify(result)

@bp.route('/admin/companies', methods=['GET'])
@cached(timeout=300, query_string=True)
@admin_required
def admin_list_companies():
    q = request.args.get('q', '')
    query = CompanyProfile.query
    if q:
        query = query.filter(CompanyProfile.name.contains(q))
    profiles = query.all()
    result = []
    for c in profiles:
        u = User.query.get(c.user_id)
        result.append({
            'id': c.id, 'user_id': c.user_id, 'name': c.name,
            'hr_contact': c.hr_contact, 'website': c.website,
            'sector': c.sector, 'status': c.approval_status,
            'is_active': u.is_active if u else True,
            'is_blacklisted': u.is_blacklisted if u else False,
            'drives': PlacementDrive.query.filter_by(company_id=c.user_id).count()
        })
    return jsonify(result)

@bp.route('/admin/companies/<int:id>/approve', methods=['POST'])
@admin_required
def approve_company(id):
    c = CompanyProfile.query.get_or_404(id)
    c.approval_status = request.get_json().get('action', 'approved')
    db.session.commit()
    invalidate_admin_caches()
    invalidate_student_drives_cache()
    return jsonify({'message': 'Done'})

@bp.route('/admin/drives', methods=['GET'])
@cached(timeout=300, query_string=True)
@admin_required
def admin_list_drives():
    q = request.args.get('q', '')
    query = PlacementDrive.query
    if q:
        query = query.filter(PlacementDrive.job_title.contains(q))
    drives = query.all()
    result = []
    for d in drives:
        company = CompanyProfile.query.filter_by(user_id=d.company_id).first()
        result.append({
            'id': d.id, 'job_title': d.job_title, 'status': d.status,
            'deadline': str(d.deadline) if d.deadline else '',
            'company_name': company.name if company else 'Unknown',
            'applicants': Application.query.filter_by(drive_id=d.id).count(),
            'created_at': str(d.created_at)
        })
    return jsonify(result)

@bp.route('/admin/drives/<int:id>/approve', methods=['POST'])
@admin_required
def approve_drive(id):
    d = PlacementDrive.query.get_or_404(id)
    d.status = request.get_json().get('action', 'approved')
    db.session.commit()
    invalidate_admin_caches()
    invalidate_student_drives_cache()
    return jsonify({'message': 'Done'})

@bp.route('/admin/users/<int:id>/blacklist', methods=['POST'])
@admin_required
def blacklist_user(id):
    u = User.query.get_or_404(id)
    u.is_blacklisted = not u.is_blacklisted
    db.session.commit()
    return jsonify({'message': 'Toggled blacklist', 'is_blacklisted': u.is_blacklisted})

@bp.route('/admin/users/<int:id>/deactivate', methods=['POST'])
@admin_required
def deactivate_user(id):
    u = User.query.get_or_404(id)
    u.is_active = not u.is_active
    db.session.commit()
    return jsonify({'message': 'Toggled active', 'is_active': u.is_active})

@bp.route('/admin/applications', methods=['GET'])
@admin_required
def admin_all_applications():
    apps = Application.query.all()
    result = []
    for a in apps:
        student = User.query.get(a.student_id)
        sp = StudentProfile.query.filter_by(user_id=a.student_id).first()
        drive = PlacementDrive.query.get(a.drive_id)
        company = CompanyProfile.query.filter_by(user_id=drive.company_id).first() if drive else None
        result.append({
            'id': a.id, 'student_name': sp.name if sp else student.username,
            'student_email': student.email, 'drive_title': drive.job_title if drive else '',
            'company_name': company.name if company else '', 'status': a.status,
            'applied_at': str(a.applied_at)
        })
    return jsonify(result)

@bp.route('/admin/monthly-chart-data', methods=['GET'])
@cached(timeout=300)
@admin_required
def admin_monthly_chart_data():
    from sqlalchemy import func
    monthly = db.session.query(
        func.strftime('%Y-%m', User.created_at).label('month'),
        func.count(User.id)
    ).filter(User.role == 'student').group_by('month').order_by('month').all()
    status_counts = db.session.query(
        Application.status, func.count(Application.id)
    ).group_by(Application.status).all()
    return jsonify({
        'monthly_registrations': {
            'labels': [m[0] for m in monthly],
            'data': [m[1] for m in monthly]
        },
        'application_status': {
            'labels': [s[0] for s in status_counts],
            'data': [s[1] for s in status_counts]
        }
    })



@bp.route('/company/profile', methods=['GET'])
@company_required
def company_profile():
    uid = int(get_jwt_identity())
    user = User.query.get(uid)
    p = CompanyProfile.query.filter_by(user_id=uid).first()
    if not p:
        return jsonify({'error': 'Profile not found'}), 404
    return jsonify({
        'name': p.name, 'hr_contact': p.hr_contact, 'website': p.website,
        'sector': p.sector, 'established_in': p.established_in,
        'approval_status': p.approval_status, 'email': user.email if user else ''
    })

@bp.route('/company/stats', methods=['GET'])
@cached(timeout=300)
@company_required
def company_stats():
    uid = int(get_jwt_identity())
    drives = PlacementDrive.query.filter_by(company_id=uid).all()
    drive_ids = [d.id for d in drives]
    applications = Application.query.filter(Application.drive_id.in_(drive_ids)).all() if drive_ids else []
    selected_count = len([a for a in applications if a.status == 'selected'])
    return jsonify({
        'drives': len(drives),
        'applicants': len(applications),
        'selected': selected_count,
    })

@bp.route('/company/drives', methods=['GET'])
@cached(timeout=300)
@company_required
def company_drives():
    uid = int(get_jwt_identity())
    drives = PlacementDrive.query.filter_by(company_id=uid).all()
    result = []
    for d in drives:
        apps = Application.query.filter_by(drive_id=d.id).all()
        applicants_list = []
        for a in apps:
            student = User.query.get(a.student_id)
            sp = StudentProfile.query.filter_by(user_id=a.student_id).first()
            applicants_list.append({
                'id': a.id,
                'student_id': a.student_id,
                'student_name': sp.name if sp else student.username,
                'college': sp.college if sp else '',
                'gpa': sp.gpa if sp else None,
                'branch': sp.branch if sp else '',
                'status': a.status,
                'applied_at': str(a.applied_at),
                'resume_path': sp.resume_path if sp else None
            })
        result.append({
            'id': d.id, 'job_title': d.job_title, 'job_description': d.job_description,
            'status': d.status, 'deadline': str(d.deadline) if d.deadline else '',
            'eligibility_branch': d.eligibility_branch, 'eligibility_gpa': d.eligibility_gpa,
            'eligibility_year': d.eligibility_year,
            'applicants': applicants_list,
            'created_at': str(d.created_at)
        })
    return jsonify(result)

@bp.route('/company/drives', methods=['POST'])
@company_required
def create_drive():
    uid = int(get_jwt_identity())
    data = request.get_json()
    profile = CompanyProfile.query.filter_by(user_id=uid).first()
    if not profile or profile.approval_status != 'approved':
        return jsonify({'error': 'Company not approved yet'}), 403
    drive = PlacementDrive(
        company_id=uid, job_title=data['job_title'],
        job_description=data.get('job_description', ''),
        eligibility_branch=data.get('eligibility_branch', ''),
        eligibility_gpa=data.get('eligibility_gpa'),
        eligibility_year=data.get('eligibility_year'),
        deadline=datetime.fromisoformat(data['deadline']) if data.get('deadline') else None,
        status='pending'
    )
    db.session.add(drive)
    db.session.commit()
    invalidate_admin_caches()
    invalidate_student_drives_cache()
    return jsonify({'message': 'Drive created. Awaiting admin approval.'}), 201

@bp.route('/company/drives/<int:id>', methods=['PUT'])
@company_required
def update_drive(id):
    d = PlacementDrive.query.get_or_404(id)
    data = request.get_json()
    for field in ['job_title', 'job_description', 'eligibility_branch', 'eligibility_gpa', 'eligibility_year']:
        if field in data:
            setattr(d, field, data[field])
    if 'deadline' in data and data['deadline']:
        d.deadline = datetime.fromisoformat(data['deadline'])
    db.session.commit()
    return jsonify({'message': 'Drive updated'})

@bp.route('/company/drives/<int:id>/close', methods=['POST'])
@company_required
def close_drive(id):
    d = PlacementDrive.query.get_or_404(id)
    d.status = 'closed'
    db.session.commit()
    invalidate_student_drives_cache()
    return jsonify({'message': 'Drive closed'})

@bp.route('/company/drives/<int:drive_id>/applicants', methods=['GET'])
@company_required
def drive_applicants(drive_id):
    apps = Application.query.filter_by(drive_id=drive_id).all()
    result = []
    for a in apps:
        student = User.query.get(a.student_id)
        sp = StudentProfile.query.filter_by(user_id=a.student_id).first()
        result.append({
            'application_id': a.id, 'student_id': a.student_id,
            'student_name': sp.name if sp else student.username,
            'college': sp.college if sp else '', 'gpa': sp.gpa if sp else None,
            'branch': sp.branch if sp else '', 'status': a.status,
            'applied_at': str(a.applied_at),
            'resume_path': sp.resume_path if sp else None
        })
    return jsonify(result)

@bp.route('/company/applications/<int:app_id>/status', methods=['POST'])
@company_required
def update_application_status(app_id):
    a = Application.query.get_or_404(app_id)
    new_status = request.get_json().get('status')
    a.status = new_status
    if new_status in ['selected', 'rejected']:
        a.result_date = datetime.utcnow()
    db.session.commit()
    invalidate_admin_caches()
    return jsonify({'message': 'Status updated'})

@bp.route('/company/history', methods=['GET'])
@company_required
def company_history():
    uid = int(get_jwt_identity())
    drives = PlacementDrive.query.filter_by(company_id=uid, status='closed').all()
    result = []
    for d in drives:
        apps = Application.query.filter_by(drive_id=d.id).all()
        result.append({
            'id': d.id, 'job_title': d.job_title, 'deadline': str(d.deadline) if d.deadline else '',
            'total_applicants': len(apps),
            'selected': len([a for a in apps if a.status == 'selected']),
            'rejected': len([a for a in apps if a.status == 'rejected']),
        })
    return jsonify(result)

@bp.route('/company/interviews', methods=['GET'])
@company_required
def company_list_interviews():
    uid = int(get_jwt_identity())
    interviews = Interview.query.filter_by(company_id=uid).all()
    result = []
    for iv in interviews:
        app = Application.query.get(iv.application_id)
        student = User.query.get(iv.student_id)
        sp = StudentProfile.query.filter_by(user_id=iv.student_id).first()
        drive = PlacementDrive.query.get(app.drive_id) if app else None
        result.append({
            'id': iv.id,
            'application_id': iv.application_id,
            'student_id': iv.student_id,
            'student_name': sp.name if sp else student.username,
            'job_title': drive.job_title if drive else '',
            'scheduled_date': iv.scheduled_date,
            'scheduled_time': iv.scheduled_time,
            'location': iv.location,
            'mode': iv.mode,
            'result': iv.result,
            'notes': iv.notes,
            'created_at': str(iv.created_at)
        })
    return jsonify(result)

@bp.route('/company/interviews', methods=['POST'])
@company_required
def schedule_interview():
    uid = int(get_jwt_identity())
    data = request.get_json()
    app_id = data.get('application_id')
    app = Application.query.get_or_404(app_id)
    drive = PlacementDrive.query.get(app.drive_id)
    if drive.company_id != uid:
        return jsonify({'error': 'Unauthorized'}), 403
    interview = Interview(
        application_id=app_id,
        student_id=app.student_id,
        company_id=uid,
        scheduled_date=data.get('scheduled_date'),
        scheduled_time=data.get('scheduled_time'),
        location=data.get('location', ''),
        mode=data.get('mode', 'online'),
        notes=data.get('notes', '')
    )
    db.session.add(interview)
    if app.status == 'applied':
        app.status = 'shortlisted'
    
    db.session.commit()
    return jsonify({'message': 'Interview scheduled successfully', 'id': interview.id}), 201

@bp.route('/company/interviews/<int:interview_id>', methods=['PUT'])
@company_required
def update_interview(interview_id):
    uid = int(get_jwt_identity())
    iv = Interview.query.get_or_404(interview_id)
    
    if iv.company_id != uid:
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    if 'scheduled_date' in data:
        iv.scheduled_date = data['scheduled_date']
    if 'scheduled_time' in data:
        iv.scheduled_time = data['scheduled_time']
    if 'location' in data:
        iv.location = data['location']
    if 'mode' in data:
        iv.mode = data['mode']
    if 'notes' in data:
        iv.notes = data['notes']
    
    db.session.commit()
    return jsonify({'message': 'Interview updated successfully'})

@bp.route('/company/interviews/<int:interview_id>/result', methods=['POST'])
@company_required
def update_interview_result(interview_id):
    uid = int(get_jwt_identity())
    iv = Interview.query.get_or_404(interview_id)
    if iv.company_id != uid:
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    result = data.get('result', 'pending')
    iv.result = result
    app = Application.query.get(iv.application_id)
    if result == 'passed':
        app.status = 'selected'
    elif result == 'failed':
        app.status = 'rejected'
    
    app.result_date = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Interview result updated and application status changed'})

@bp.route('/student/interviews', methods=['GET'])
@student_required
def student_list_interviews():
    uid = int(get_jwt_identity())
    interviews = Interview.query.filter_by(student_id=uid).all()
    result = []
    for iv in interviews:
        app = Application.query.get(iv.application_id)
        company = CompanyProfile.query.filter_by(user_id=iv.company_id).first()
        drive = PlacementDrive.query.get(app.drive_id) if app else None
        result.append({
            'id': iv.id,
            'application_id': iv.application_id,
            'job_title': drive.job_title if drive else '',
            'company_name': company.name if company else '',
            'scheduled_date': iv.scheduled_date,
            'scheduled_time': iv.scheduled_time,
            'location': iv.location,
            'mode': iv.mode,
            'result': iv.result,
            'notes': iv.notes,
            'created_at': str(iv.created_at)
        })
    return jsonify(result)



@bp.route('/student/stats', methods=['GET'])
@student_required
def student_stats():
    uid = int(get_jwt_identity())
    apps = Application.query.filter_by(student_id=uid).all()
    return jsonify({
        'applications': len(apps),
        'shortlisted': len([a for a in apps if a.status == 'shortlisted']),
        'selected': len([a for a in apps if a.status == 'selected']),
        'rejected': len([a for a in apps if a.status == 'rejected']),
    })

@bp.route('/student/drives', methods=['GET'])
@cached(timeout=300, query_string=True)
@student_required
def student_drives():
    uid = int(get_jwt_identity())
    branch = request.args.get('branch', '')
    min_gpa = request.args.get('min_gpa', type=float)
    year = request.args.get('year', type=int)
    query = PlacementDrive.query.filter_by(status='approved')
    if branch:
        query = query.filter(PlacementDrive.eligibility_branch.contains(branch))
    if min_gpa:
        query = query.filter((PlacementDrive.eligibility_gpa <= min_gpa) | (PlacementDrive.eligibility_gpa == None))
    if year:
        query = query.filter((PlacementDrive.eligibility_year == year) | (PlacementDrive.eligibility_year == None))
    drives = query.all()
    applied_ids = [a.drive_id for a in Application.query.filter_by(student_id=uid).all()]
    result = []
    for d in drives:
        company = CompanyProfile.query.filter_by(user_id=d.company_id).first()
        result.append({
            'id': d.id, 'job_title': d.job_title, 'job_description': d.job_description,
            'deadline': str(d.deadline) if d.deadline else '',
            'eligibility_gpa': d.eligibility_gpa, 'eligibility_branch': d.eligibility_branch,
            'eligibility_year': d.eligibility_year,
            'company_name': company.name if company else 'Unknown',
            'already_applied': d.id in applied_ids,
        })
    return jsonify(result)

@bp.route('/student/apply/<int:drive_id>', methods=['POST'])
@student_required
def apply_to_drive(drive_id):
    uid = int(get_jwt_identity())
    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.status != 'approved':
        return jsonify({'error': 'Drive not open'}), 400
    if Application.query.filter_by(student_id=uid, drive_id=drive_id).first():
        return jsonify({'error': 'Already applied'}), 400
    sp = StudentProfile.query.filter_by(user_id=uid).first()
    if drive.eligibility_gpa and sp and sp.gpa and sp.gpa < drive.eligibility_gpa:
        return jsonify({'error': f'Minimum GPA required: {drive.eligibility_gpa}'}), 400
    db.session.add(Application(student_id=uid, drive_id=drive_id))
    db.session.commit()
    invalidate_admin_caches()
    return jsonify({'message': 'Applied successfully'}), 201

@bp.route('/student/applications', methods=['GET'])
@student_required
def student_applications():
    uid = int(get_jwt_identity())
    apps = Application.query.filter_by(student_id=uid).filter(
        ~Application.status.in_(['selected', 'rejected'])).all()
    result = []
    for a in apps:
        if not a.drive_id:
            continue
        drive = PlacementDrive.query.get(a.drive_id)
        if not drive:
            continue
        company = CompanyProfile.query.filter_by(user_id=drive.company_id).first()
        result.append({
            'id': a.id, 'job_title': drive.job_title or '',
            'company': company.name if company else 'Unknown',
            'applied_at': str(a.applied_at) if a.applied_at else '',
            'status': a.status,
            'result_date': str(a.result_date) if a.result_date else '',
            'deadline': str(drive.deadline) if drive.deadline else '',
        })
    return jsonify(result)

@bp.route('/student/history', methods=['GET'])
@student_required
def student_history():
    uid = int(get_jwt_identity())
    apps = Application.query.filter_by(student_id=uid).filter(
        Application.status.in_(['selected', 'rejected'])).all()
    result = []
    for a in apps:
        if not a.drive_id:
            continue
        drive = PlacementDrive.query.get(a.drive_id)
        if not drive:
            continue
        company = CompanyProfile.query.filter_by(user_id=drive.company_id).first()
        result.append({
            'id': a.id, 'job_title': drive.job_title or '',
            'company': company.name if company else 'Unknown',
            'applied_at': str(a.applied_at) if a.applied_at else '',
            'status': a.status,
            'result_date': str(a.result_date) if a.result_date else '',
        })
    return jsonify(result)

@bp.route('/student/profile', methods=['GET'])
@student_required
def student_profile_get():
    uid = int(get_jwt_identity())
    u = User.query.get(uid)
    p = StudentProfile.query.filter_by(user_id=uid).first()
    return jsonify({
        'username': u.username, 'email': u.email,
        'name': p.name if p else '', 'dob': p.dob if p else '',
        'college': p.college if p else '', 'gpa': p.gpa if p else None,
        'branch': p.branch if p else '', 'year': p.year if p else None,
        'address': p.address if p else '', 'resume_path': p.resume_path if p else ''
    })

@bp.route('/student/profile', methods=['PUT'])
@student_required
def student_profile_update():
    uid = int(get_jwt_identity())
    p = StudentProfile.query.filter_by(user_id=uid).first()
    if not p:
        return jsonify({'error': 'Profile not found'}), 404
    data = request.get_json()
    for field in ['name', 'dob', 'college', 'gpa', 'branch', 'year', 'address']:
        if field in data:
            setattr(p, field, data[field])
    db.session.commit()
    return jsonify({'message': 'Profile updated'})

@bp.route('/student/resume', methods=['POST'])
@student_required
def upload_resume():
    uid = int(get_jwt_identity())
    if 'resume' not in request.files:
        return jsonify({'error': 'No file'}), 400
    f = request.files['resume']
    upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    path = os.path.join(upload_dir, f'{uid}_{f.filename}')
    f.save(path)
    p = StudentProfile.query.filter_by(user_id=uid).first()
    p.resume_path = path
    db.session.commit()
    return jsonify({'message': 'Resume uploaded', 'path': path})

@bp.route('/student/notifications', methods=['GET'])
@student_required
def student_notifications():
    uid = int(get_jwt_identity())
    apps = Application.query.filter_by(student_id=uid).all()
    notifications = []
    for a in apps:
        drive = PlacementDrive.query.get(a.drive_id)
        if not drive:
            continue
        if drive.deadline and (drive.deadline - datetime.utcnow()).days <= 2 and (drive.deadline - datetime.utcnow()).days >= 0:
            notifications.append({
                'type': 'deadline', 'message': f"Deadline for '{drive.job_title}' is in {(drive.deadline - datetime.utcnow()).days} day(s)!",
                'date': str(drive.deadline)
            })
        if a.status in ['shortlisted', 'selected', 'rejected']:
            notifications.append({
                'type': 'status', 'message': f"Your application for '{drive.job_title}' has been {a.status}.",
                'date': str(a.result_date) if a.result_date else str(a.applied_at)
            })
    upcoming = PlacementDrive.query.filter_by(status='approved').filter(
        PlacementDrive.deadline > datetime.utcnow()).all()
    for d in upcoming:
        if not any(a.drive_id == d.id for a in apps):
            company = CompanyProfile.query.filter_by(user_id=d.company_id).first()
            notifications.append({
                'type': 'new_drive', 'message': f"New drive: '{d.job_title}' by {company.name if company else 'Unknown'}",
                'date': str(d.created_at)
            })
    return jsonify(notifications)



@bp.route('/jobs/export-csv', methods=['POST'])
@student_required
def trigger_csv_export():
    from tasks import export_student_csv
    export_student_csv.delay(int(get_jwt_identity()))
    return jsonify({'message': 'CSV export started. It will be emailed to you.'})


@bp.route('/admin/notifications', methods=['GET'])
@admin_required
def admin_notifications():
    notifications = []
    pending_drives = PlacementDrive.query.filter_by(status='pending').all()
    for d in pending_drives:
        company = CompanyProfile.query.filter_by(user_id=d.company_id).first()
        notifications.append({
            'type': 'pending_drive',
            'message': f"New placement drive '{d.job_title}' pending approval from {company.name if company else 'Unknown'}",
            'date': str(d.created_at)
        })
    pending_companies = CompanyProfile.query.filter_by(approval_status='pending').all()
    for c in pending_companies:
        notifications.append({
            'type': 'pending_company',
            'message': f"Company '{c.name}' registration pending approval",
            'date': str(c.user.created_at) if c.user else ''
        })
    total_students = User.query.filter_by(role='student').count()
    total_companies = User.query.filter_by(role='company').count()
    if total_students == 0:
        notifications.append({
            'type': 'info',
            'message': 'No students registered yet',
            'date': str(datetime.utcnow())
        })
    return jsonify(notifications)


@bp.route('/company/notifications', methods=['GET'])
@company_required
def company_notifications():
    uid = int(get_jwt_identity())
    notifications = []
    drives = PlacementDrive.query.filter_by(company_id=uid).all()
    for d in drives:
        apps = Application.query.filter_by(drive_id=d.id).all()
        for a in apps:
            if a.status in ['shortlisted', 'selected', 'rejected']:
                student = User.query.get(a.student_id)
                sp = StudentProfile.query.filter_by(user_id=a.student_id).first()
                notifications.append({
                    'type': 'application_update',
                    'message': f"{sp.name if sp else student.username} application status: {a.status}",
                    'date': str(a.result_date) if a.result_date else str(a.applied_at)
                })
        if d.status == 'pending' and (datetime.utcnow() - d.created_at).days > 2:
            notifications.append({
                'type': 'pending_approval',
                'message': f"Drive '{d.job_title}' is still pending admin approval",
                'date': str(d.created_at)
            })
    return jsonify(notifications)


@bp.route('/admin/export-csv', methods=['POST'])
@admin_required
def admin_export_csv():
    from tasks import export_admin_data_csv
    export_admin_data_csv.delay()
    return jsonify({'message': 'Admin CSV export started. You will receive it by email.'})


@bp.route('/admin/request-report', methods=['POST'])
@admin_required
def admin_request_report():
    from tasks import send_monthly_report
    send_monthly_report.delay()
    return jsonify({'message': 'Monthly report requested. It will be sent to your email.'})
