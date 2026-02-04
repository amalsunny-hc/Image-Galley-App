"""
Database initialization script
Creates database and optionally creates a default admin user
"""
from app import create_app, db
from app.models.user import User
import os

def init_db():
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created successfully")
        
        # Check if any users exist
        user_count = User.query.count()
        if user_count == 0:
            print("\nNo users found. Creating default admin user...")
            
            # Create default admin
            admin = User(
                username='admin',
                email='admin@imagegallery.local',
                is_admin=True,
                is_active=True
            )
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            
            print(f"✓ Admin user created!")
            print(f"\n  Username: admin")
            print(f"  Password: admin123")
            print(f"  Email: admin@imagegallery.local")
            print(f"\n  ⚠️  Change the password after first login!")
        else:
            print(f"\n✓ Database already initialized with {user_count} user(s)")
        
        print("\n✓ Database initialization complete!")
        print(f"  Database location: {os.path.abspath('image_gallery.db')}")

if __name__ == '__main__':
    init_db()
