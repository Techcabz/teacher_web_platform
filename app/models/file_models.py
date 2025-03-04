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
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ✅ Store user ID
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    category = db.relationship('Category', backref=db.backref('files', lazy=True))
    uploader = db.relationship('User', backref=db.backref('uploaded_files', lazy=True))  # ✅ Relate to User

    def __repr__(self):
        return f"<File {self.id}: {self.filename} ({self.file_size} bytes) uploaded by {self.uploader_id}>"

    def get_size_in_kb(self):
        return round(self.file_size / 1024, 2)

    def get_size_in_mb(self):
        return round(self.file_size / (1024 * 1024), 2)

    def get_file_extension(self):
        return os.path.splitext(self.filename)[1].lower()  
