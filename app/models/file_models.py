from app.extensions import db
from datetime import datetime
import os

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(512), nullable=False) 
    file_size = db.Column(db.Integer, nullable=False)  
    file_extension = db.Column(db.String(10), nullable=False)  
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)  
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    category = db.relationship('Category', backref=db.backref('files', lazy=True))

    def __repr__(self):
        return f"<File {self.id}: {self.filename} ({self.file_size} bytes)>"

    def get_size_in_kb(self):
        """Returns file size in KB"""
        return round(self.file_size / 1024, 2)

    def get_size_in_mb(self):
        """Returns file size in MB"""
        return round(self.file_size / (1024 * 1024), 2)

    def get_file_extension(self):
        """Returns file extension"""
        return os.path.splitext(self.filename)[1].lower()  # Example: '.jpg'
