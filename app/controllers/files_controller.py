from flask import  request,render_template
from flask import jsonify
from app.services.services import CRUDService
from app.models.category_models import Category
from app.utils.validation_utils import Validation
from app.models.file_models import File
from app.models.user_models import User

category_service = CRUDService(Category)

def files(request):
    if request.method == 'GET':
        categories = category_service.get()
        
        files = File.query.join(User).join(Category).add_columns(
            File.id, File.filename, File.file_size, File.file_extension, File.uploader_id,
            File.uploaded_at,
            User.firstname, User.middlename, User.lastname,
            Category.name.label('category_name'), Category.slug.label('category_slug')
            ).all()
        return render_template('admin/docs.html', categories=categories, files=files)
    