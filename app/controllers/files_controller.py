from flask import  request,render_template
from flask import jsonify
from app.services.services import CRUDService
from app.models.category_models import Category
from app.utils.validation_utils import Validation

category_service = CRUDService(Category)

def files(request):
    if request.method == 'GET':
        categories = category_service.get()
        return render_template('admin/docs.html', categories=categories)
    