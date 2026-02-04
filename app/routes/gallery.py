from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory, send_file
from flask_login import login_required, current_user
from app import db
from app.models.image import Image
from app.models.user import User
from app.utils.s3 import upload_image_to_s3, delete_image_from_s3
from werkzeug.utils import secure_filename
from PIL import Image as PILImage
import os
from datetime import datetime
import io
import boto3

gallery_bp = Blueprint('gallery', __name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(original_filename):
    ext = original_filename.rsplit('.', 1)[1].lower()
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
    return timestamp + secure_filename(original_filename)

@gallery_bp.route('/')
@gallery_bp.route('/gallery')
def index():
    page = request.args.get('page', 1, type=int)
    
    if current_user.is_authenticated:
        # Show all public images and user's own images
        images = Image.query.filter(
            (Image.is_public == True) | (Image.user_id == current_user.id)
        ).order_by(Image.created_at.desc()).paginate(page=page, per_page=12)
    else:
        # Show only public images for non-authenticated users
        images = Image.query.filter_by(is_public=True).order_by(Image.created_at.desc()).paginate(page=page, per_page=12)
    
    return render_template('gallery/index.html', images=images)

@gallery_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        # Check if file is present
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('gallery.upload'))
        
        file = request.files['file']
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        is_public = request.form.get('is_public') == 'on'
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('gallery.upload'))
        
        if not title:
            flash('Title is required', 'error')
            return redirect(url_for('gallery.upload'))
        
        if file and allowed_file(file.filename):
            try:
                # Generate unique filename
                filename = generate_unique_filename(file.filename)
                
                # Upload to S3
                s3_key = upload_image_to_s3(file, filename)
                
                # Create image record with S3 key
                image = Image(
                    filename=filename,
                    original_filename=secure_filename(file.filename),
                    title=title,
                    description=description,
                    user_id=current_user.id,
                    is_public=is_public,
                    s3_key=s3_key
                )
                
                db.session.add(image)
                db.session.commit()
                
                flash('Image uploaded successfully!', 'success')
                return redirect(url_for('gallery.index'))
            
            except Exception as e:
                flash(f'Error uploading image: {str(e)}', 'error')
                return redirect(url_for('gallery.upload'))
        else:
            flash('Invalid file type. Allowed: jpg, jpeg, png, gif, webp', 'error')
            return redirect(url_for('gallery.upload'))
    
    return render_template('gallery/upload.html')

@gallery_bp.route('/image/<int:image_id>')
def view_image(image_id):
    image = Image.query.get_or_404(image_id)
    
    # Check permissions
    if not image.is_public and (not current_user.is_authenticated or (image.user_id != current_user.id and not current_user.is_admin)):
        flash('You do not have permission to view this image', 'error')
        return redirect(url_for('gallery.index'))
    
    uploader = User.query.get(image.user_id)
    return render_template('gallery/view.html', image=image, uploader=uploader)

@gallery_bp.route('/image/<int:image_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_image(image_id):
    image = Image.query.get_or_404(image_id)
    
    # Check if user owns the image or is admin
    if image.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to edit this image', 'error')
        return redirect(url_for('gallery.index'))
    
    if request.method == 'POST':
        image.title = request.form.get('title', '').strip()
        image.description = request.form.get('description', '').strip()
        image.is_public = request.form.get('is_public') == 'on'
        
        db.session.commit()
        flash('Image updated successfully!', 'success')
        return redirect(url_for('gallery.view_image', image_id=image.id))
    
    return render_template('gallery/edit.html', image=image)

@gallery_bp.route('/image/<int:image_id>/delete', methods=['POST'])
@login_required
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    
    # Check if user owns the image or is admin
    if image.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to delete this image', 'error')
        return redirect(url_for('gallery.index'))
    
    try:
        # Delete from S3 if key exists
        if image.s3_key:
            delete_image_from_s3(image.s3_key)
        
        # Delete database record
        db.session.delete(image)
        db.session.commit()
        
        flash('Image deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting image: {str(e)}', 'error')
    
    return redirect(url_for('gallery.index'))

@gallery_bp.route('/image/<int:image_id>/download')
def download_image(image_id):
    image = Image.query.get_or_404(image_id)
    
    # Check permissions
    if not image.is_public and (not current_user.is_authenticated or (image.user_id != current_user.id and not current_user.is_admin)):
        flash('You do not have permission to download this image', 'error')
        return redirect(url_for('gallery.index'))
    
    try:
        debug = current_app.config.get('DEBUG', True)
        s3_bucket = current_app.config.get('S3_BUCKET_NAME')
        use_s3 = not debug and s3_bucket
        
        if use_s3 and image.s3_key:
            # Download from S3
            s3_client = boto3.client(
                's3',
                region_name=current_app.config.get('AWS_REGION', 'us-east-1')
            )
            try:
                file_obj = io.BytesIO()
                s3_client.download_fileobj(s3_bucket, image.s3_key, file_obj)
                file_obj.seek(0)
                return send_file(
                    file_obj,
                    download_name=image.original_filename,
                    as_attachment=True
                )
            except Exception as e:
                flash(f'Error downloading from S3: {str(e)}', 'error')
                return redirect(url_for('gallery.view_image', image_id=image.id))
        else:
            # Download from local storage
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
            
            # Resolve path relative to project root
            if not os.path.isabs(upload_folder):
                upload_folder = os.path.join(os.getcwd(), upload_folder)
            
            file_path = os.path.join(upload_folder, image.filename)
            
            if os.path.exists(file_path):
                return send_file(
                    file_path,
                    download_name=image.original_filename,
                    as_attachment=True
                )
            else:
                flash(f'Image file not found: {file_path}', 'error')
                return redirect(url_for('gallery.view_image', image_id=image.id))
    
    except Exception as e:
        flash(f'Error downloading image: {str(e)}', 'error')
        return redirect(url_for('gallery.view_image', image_id=image.id))

@gallery_bp.route('/my-gallery')
@login_required
def my_gallery():
    page = request.args.get('page', 1, type=int)
    images = Image.query.filter_by(user_id=current_user.id).order_by(Image.created_at.desc()).paginate(page=page, per_page=12)
    return render_template('gallery/my_gallery.html', images=images)
