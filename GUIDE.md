# Image Gallery Application - Complete Guide

A professional Python Flask image gallery application with user authentication, admin controls, and image management.

## 🎯 Project Overview

This application allows users to:
- **Register and login** with secure authentication
- **Upload and manage images** with titles and descriptions
- **View public gallery** of images from all users
- **Control image visibility** (public/private)

Admins can:
- **Manage users**: Create, activate, deactivate, promote to admin
- **Manage images**: Delete, toggle visibility, monitor content
- **View dashboard**: See system statistics

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step-by-Step Setup

1. **Navigate to project directory**
   ```bash
   cd /home/sharoon/Sharoon/workspace/ai-projects/projects1/image_gallery
   ```

2. **Install dependencies** (already done)
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize database** (already done)
   ```bash
   python3 init_db.py
   ```

4. **Run the application**
   ```bash
   python3 run.py
   ```

5. **Open in browser**
   - Go to `http://localhost:5000`

## 🔑 Default Login Credentials

After database initialization, use these credentials to login:

**Admin Account:**
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@imagegallery.local`

⚠️ **IMPORTANT**: Change the password after first login!

## 🎨 User Guide

### For Regular Users

#### Registration
1. Click "Register" on login page
2. Enter username (unique)
3. Enter email address
4. Enter password (minimum 6 characters)
5. Click "Register"

#### Login
1. Click "Login" on home page
2. Enter username and password
3. Click "Login"

#### Uploading Images
1. After login, click "Upload" in navigation
2. Select an image file (JPG, PNG, GIF, WebP)
3. Enter image title (required)
4. Add description (optional)
5. Choose visibility:
   - ✓ **Public**: Visible to all users
   - ☐ **Private**: Visible only to you
6. Click "Upload Image"

#### Managing Your Images
1. Click "My Images" in navigation
2. View your uploaded images
3. Click image to view details
4. Click "Edit" to change title/description/visibility
5. Click "Delete" to remove image

#### Browsing Gallery
1. Click "Gallery" to view all public images
2. Use pagination to browse
3. Click image to view details and uploader info

### For Admins

#### Accessing Admin Panel
1. Login with admin account
2. Click "Admin Panel" dropdown in navigation
3. Choose from:
   - Dashboard
   - Manage Users
   - Manage Images

#### Dashboard
- View total users
- View active users
- View total images
- View admin users
- Quick links to user and image management

#### Managing Users
1. Go to Admin Panel → Manage Users
2. View all users in the system
3. For each user, you can:
   - **Make Admin**: Grant admin privileges
   - **Remove Admin**: Revoke admin privileges
   - **Activate**: Enable deactivated account
   - **Deactivate**: Disable account (user can't login)
   - **Delete**: Permanently delete user and their images

#### Managing Images
1. Go to Admin Panel → Manage Images
2. View all images with thumbnails
3. For each image, you can:
   - **View**: Open image details
   - **Make Public**: Allow all users to see
   - **Make Private**: Restrict to owner only
   - **Delete**: Permanently remove image

## 📁 Project Structure

```
image_gallery/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # User database model
│   │   └── image.py             # Image database model
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py              # Login/Register routes
│   │   ├── gallery.py           # Gallery/Upload routes
│   │   └── admin.py             # Admin panel routes
│   ├── static/
│   │   ├── uploads/             # User-uploaded images
│   │   ├── css/                 # Stylesheets
│   │   └── js/                  # JavaScript files
│   └── templates/
│       ├── base.html            # Base layout
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       ├── gallery/
│       │   ├── index.html       # Gallery view
│       │   ├── upload.html      # Upload form
│       │   ├── view.html        # Image details
│       │   ├── edit.html        # Edit image
│       │   └── my_gallery.html  # User's images
│       └── admin/
│           ├── dashboard.html   # Admin dashboard
│           ├── users.html       # User management
│           └── images.html      # Image management
├── .env                         # Configuration file
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── init_db.py                   # Database initialization
├── setup.sh                     # Setup script
├── README.md                    # Full documentation
├── QUICKSTART.md                # Quick start guide
└── GUIDE.md                     # This file
```

## ⚙️ Configuration (.env file)

Edit `.env` to customize:

| Variable | Default | Purpose |
|----------|---------|---------|
| `FLASK_APP` | run.py | Entry point |
| `FLASK_ENV` | development | Environment (development/production) |
| `SECRET_KEY` | key | Session encryption key |
| `DATABASE_URL` | sqlite:///image_gallery.db | Database location |
| `UPLOAD_FOLDER` | app/static/uploads | Image storage folder |
| `MAX_FILE_SIZE` | 16777216 | Max upload size (16MB) |
| `DEBUG` | True | Debug mode |

### Production Configuration

For production deployment:

1. Change `FLASK_ENV` to `production`
2. Change `DEBUG` to `False`
3. Generate a strong `SECRET_KEY`:
   ```python
   import secrets
   secrets.token_hex(32)
   ```
4. Use PostgreSQL instead of SQLite
5. Set proper `DATABASE_URL`
6. Use HTTPS only

## 🛡️ Security Features

✓ Password hashing with Werkzeug  
✓ Session management with Flask-Login  
✓ CSRF protection on forms  
✓ SQL injection prevention (SQLAlchemy)  
✓ Role-based access control  
✓ Account activation/deactivation  
✓ Image visibility controls  

## 🖼️ Supported Image Formats

- ✓ JPEG (.jpg, .jpeg)
- ✓ PNG (.png)
- ✓ GIF (.gif)
- ✓ WebP (.webp)

**Maximum file size:** 16MB (configurable in `.env`)

## 📊 Database Schema

### Users Table
```
id (Primary Key)
username (Unique)
email (Unique)
password_hash (Hashed)
is_admin (Boolean)
is_active (Boolean)
created_at (DateTime)
```

### Images Table
```
id (Primary Key)
filename (Stored file name)
original_filename (Upload name)
title (String)
description (Text)
user_id (Foreign Key → Users)
is_public (Boolean)
created_at (DateTime)
updated_at (DateTime)
```

## 🐛 Troubleshooting

### Issue: "Port 5000 already in use"
**Solution:** Kill the process or use different port:
```bash
python3 run.py  # Change port in code or use environment variable
```

### Issue: "No images folder"
**Solution:** The folder is created automatically on first run.

### Issue: "Database locked"
**Solution:** Close all instances of the app and delete `.db-journal` file.

### Issue: "Can't upload images"
**Solution:** Check file format and size, ensure `app/static/uploads/` is writable.

### Issue: "Forgot password"
**Solution:** Access database and reset:
```bash
sqlite3 image_gallery.db
UPDATE users SET password_hash = '' WHERE username = 'admin';
```

## 🚀 Advanced Usage

### Creating Additional Admins

**Via Python Shell:**
```bash
python3
>>> from app import create_app, db
>>> from app.models.user import User
>>> app = create_app()
>>> with app.app_context():
...     user = User.query.filter_by(username='john').first()
...     user.is_admin = True
...     db.session.commit()
```

**Via Database:**
```bash
sqlite3 image_gallery.db
UPDATE users SET is_admin = 1 WHERE username = 'john';
```

### Backup Database

```bash
cp image_gallery.db image_gallery.db.backup
```

### Restore Database

```bash
cp image_gallery.db.backup image_gallery.db
```

### Delete User's Images

```bash
python3
>>> from app import create_app, db
>>> from app.models.image import Image
>>> app = create_app()
>>> with app.app_context():
...     Image.query.filter_by(user_id=5).delete()
...     db.session.commit()
```

## 📝 Development Notes

- All images are optimized on upload (max 2000x2000 px)
- Images are stored with timestamp prefix (YYYYMMDD_HHMMSS_filename)
- Database auto-creates on first run
- Bootstrap 5 used for responsive design
- No external CDN dependencies in production

## 🔄 Common Tasks

### Reset Admin Password
1. Delete the database: `rm image_gallery.db`
2. Reinitialize: `python3 init_db.py`
3. Login with new credentials

### Export User List
```bash
sqlite3 image_gallery.db
SELECT username, email, is_admin, created_at FROM users;
```

### Disable Registration
Edit `app/routes/auth.py` and remove/comment out the register route.

### Change Upload Folder
Update `UPLOAD_FOLDER` in `.env` file.

## 📞 Support

For issues:
1. Check `.env` configuration
2. Review browser console for JavaScript errors
3. Check terminal for Python errors
4. Verify database exists and is readable
5. Ensure write permissions on upload folder

## 🎓 Learning Resources

This application demonstrates:
- Flask web application structure
- SQLAlchemy ORM usage
- User authentication and authorization
- Role-based access control (RBAC)
- File upload handling
- Image processing with Pillow
- Bootstrap responsive design
- Jinja2 templating

## 📜 Version History

- **v1.0.0** - Initial release
  - User authentication
  - Image upload/management
  - Admin panel
  - Image gallery

## 📄 License

This project is provided for educational and personal use.

---

**Last Updated:** February 4, 2026  
**Application Name:** Image Gallery  
**Version:** 1.0.0
