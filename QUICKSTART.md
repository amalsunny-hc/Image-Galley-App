# Image Gallery Application - Setup Instructions

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**
   ```bash
   python run.py
   ```

3. **Access at** `http://localhost:5000`

## Default Credentials

No default accounts are created. You need to:
1. Register a user account
2. Manually set `is_admin=True` in the database for one user to create an admin

## Environment Setup

The `.env` file contains all configuration. Update as needed:

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=sqlite:///image_gallery.db
UPLOAD_FOLDER=app/static/uploads
MAX_FILE_SIZE=16777216
DEBUG=True
```

## First Admin Creation

After creating a user account, you can make them admin by:

### Option 1: Using Python Shell
```bash
python
>>> from app import create_app, db
>>> from app.models.user import User
>>> app = create_app()
>>> with app.app_context():
...     user = User.query.filter_by(username='your_username').first()
...     user.is_admin = True
...     db.session.commit()
>>> exit()
```

### Option 2: Direct Database (SQLite)
```bash
sqlite3 image_gallery.db
UPDATE users SET is_admin = 1 WHERE username = 'your_username';
.exit
```

## Features Breakdown

**Public Access:**
- View public images in gallery

**Authenticated Users:**
- Upload images
- Manage own images
- View all public images + own private images

**Admins:**
- Full user management (create, activate, deactivate, promote)
- Full image management (view all, delete, toggle visibility)
- System dashboard with statistics

## File Structure

```
image_gallery/
├── app/
│   ├── models/           # Database models (User, Image)
│   ├── routes/           # Route handlers (auth, gallery, admin)
│   ├── templates/        # HTML templates
│   ├── static/           # CSS, JS, uploaded images
│   └── __init__.py       # App initialization
├── .env                  # Configuration
├── requirements.txt      # Dependencies
└── run.py               # Entry point
```

## Technologies Used

- **Backend**: Flask 2.3.3
- **Database**: SQLAlchemy (SQLite)
- **Authentication**: Flask-Login, Werkzeug
- **Image Processing**: Pillow
- **Frontend**: Bootstrap 5
- **Configuration**: python-dotenv

## Common Tasks

**Upload an image:**
1. Login
2. Click "Upload" in navbar
3. Select file, add title & description
4. Choose public/private
5. Submit

**Manage users (Admin):**
1. Go to Admin Panel → Manage Users
2. Promote/demote/deactivate users

**Delete inappropriate content (Admin):**
1. Go to Admin Panel → Manage Images
2. Click Delete on the image

**Change image visibility:**
- Users: Edit → toggle checkbox
- Admins: Manage Images → toggle visibility
