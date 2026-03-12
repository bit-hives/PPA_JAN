
from app import create_app
from models import db

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✓ Database tables created successfully!")
        from models import User, StudentProfile, CompanyProfile, PlacementDrive, Application
        tables = [User.__tablename__, StudentProfile.__tablename__, CompanyProfile.__tablename__, 
                  PlacementDrive.__tablename__, Application.__tablename__]
        print(f"✓ Tables created: {', '.join(tables)}")
        admin = User.query.filter_by(role='admin').first()
        if admin:
            print(f"✓ Admin user exists: {admin.username}")
        else:
            print("✗ Admin user not found")
