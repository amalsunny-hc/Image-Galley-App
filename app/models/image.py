from app import db
from datetime import datetime

class Image(db.Model):
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_public = db.Column(db.Boolean, default=True)
    s3_key = db.Column(db.String(512), nullable=True)  # S3 object key
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Image {self.original_filename}>'
    
    def get_file_path(self):
        """For backwards compatibility - returns S3 key if available"""
        return self.s3_key if self.s3_key else f'uploads/{self.filename}'
    
    def get_s3_signed_url(self, expiration=3600):
        """Get signed URL from S3 or local path based on storage mode"""
        if not self.s3_key:
            return None
        
        # Check if using S3 or local storage
        from app.utils.s3 import should_use_s3
        from flask import url_for
        
        if should_use_s3():
            # S3 mode - return signed URL
            from app.utils.s3 import get_signed_url
            return get_signed_url(self.s3_key, expiration=expiration)
        else:
            # DEBUG mode - return local static URL
            return url_for('static', filename=self.s3_key)
