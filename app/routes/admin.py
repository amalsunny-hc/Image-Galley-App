from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.user import User
from app.models.image import Image
from app.utils.s3 import delete_image_from_s3
import os
from flask import current_app

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required', 'error')
            return redirect(url_for('gallery.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    total_images = Image.query.count()
    total_admins = User.query.filter_by(is_admin=True).count()
    
    stats = {
        'total_users': total_users,
        'total_images': total_images,
        'total_admins': total_admins,
        'active_users': User.query.filter_by(is_active=True).count()
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=10)
    return render_template('admin/users.html', users=users)

@admin_bp.route('/user/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        is_admin = request.form.get('is_admin') == 'on'
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return redirect(url_for('admin.create_user'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('admin.create_user'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return redirect(url_for('admin.create_user'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('admin.create_user'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('admin.create_user'))
        
        # Create new user
        user = User(username=username, email=email, is_admin=is_admin, is_active=True)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        role = 'Admin' if is_admin else 'User'
        flash(f'User {username} created successfully as {role}', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin/create_user.html')

@admin_bp.route('/user/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    if user_id == current_user.id:
        flash('You cannot change your own admin status', 'error')
        return redirect(url_for('admin.manage_users'))
    
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = 'Admin' if user.is_admin else 'User'
    flash(f'User {user.username} is now {status}', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/user/<int:user_id>/toggle-active', methods=['POST'])
@login_required
@admin_required
def toggle_active(user_id):
    if user_id == current_user.id:
        flash('You cannot deactivate your own account', 'error')
        return redirect(url_for('admin.manage_users'))
    
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.username} has been {status}', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    if user_id == current_user.id:
        flash('You cannot delete your own account', 'error')
        return redirect(url_for('admin.manage_users'))
    
    user = User.query.get_or_404(user_id)
    username = user.username
    
    try:
        # Delete user's images from S3
        images = Image.query.filter_by(user_id=user_id).all()
        for image in images:
            if image.s3_key:
                delete_image_from_s3(image.s3_key)
        
        db.session.delete(user)
        db.session.commit()
        
        flash(f'User {username} and their images have been deleted', 'success')
    except Exception as e:
        flash(f'Error deleting user: {str(e)}', 'error')
    
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/images')
@login_required
@admin_required
def manage_images():
    page = request.args.get('page', 1, type=int)
    images = Image.query.order_by(Image.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/images.html', images=images)

@admin_bp.route('/image/<int:image_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    
    try:
        # Delete from S3 if key exists
        if image.s3_key:
            delete_image_from_s3(image.s3_key)
        
        db.session.delete(image)
        db.session.commit()
        
        flash('Image deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting image: {str(e)}', 'error')
    
    return redirect(url_for('admin.manage_images'))

@admin_bp.route('/image/<int:image_id>/toggle-public', methods=['POST'])
@login_required
@admin_required
def toggle_public(image_id):
    image = Image.query.get_or_404(image_id)
    image.is_public = not image.is_public
    db.session.commit()
    
    status = 'public' if image.is_public else 'private'
    flash(f'Image is now {status}', 'success')
    return redirect(url_for('admin.manage_images'))
