from flask import  request,render_template
from flask import jsonify
from app.services.services import CRUDService
from app.models.user_models import User
from app.utils.validation_utils import Validation
from app.models.file_models import File 
from app.models.category_models import Category

user_services = CRUDService(User)
file_services = CRUDService(File)
category_services = CRUDService(Category)

def cusers(request,users_id=None):
    if request.method == 'GET':
        users = user_services.get()
        pending_count = sum(1 for user in users if user.status == 0)
       
        return render_template('admin/users.html', users=users, pendingCount=pending_count)
    return jsonify({'success': False, 'message': 'Create method must be POST.'}), 405

def user_approved(request,users_id=None):
    if request.method == 'PUT':
        users = user_services.get_one(id=users_id)
        if not users:
            return jsonify({'success': False, 'message': 'Invalid User'}), 405
        
        data = request.json
        new_status = int(data.get("status"))
        
        user_services.update(users_id,status=new_status)
        return jsonify({'success': False, 'message': 'User approved successfully.'}), 200
    
    return jsonify({'success': False, 'message': 'Create method must be POST.'}), 405


def user_disapproved(request,users_id=None):
    if request.method == 'DELETE':
        users = user_services.get_one(id=users_id)
        if not users:
            return jsonify({'success': False, 'message': 'Invalid User'}), 404
    
        user_services.delete(id=users_id)
        return jsonify({'success': False, 'message': 'User remove successfully.'}), 200
    
    return jsonify({'success': False, 'message': 'Create method must be DELETE.'}), 405

def dashboard_report():
    users = user_services.get()
    pending_count = sum(1 for user in users if user.status == 0)
    total_count = len(users)

    # Fetch categories
    categories = category_services.get()
    files = file_services.get()  

    
    file_data = {category.name: 0 for category in categories}  

    for file in files:
        if file.category_id in [category.id for category in categories]:
            category_name = next(cat.name for cat in categories if cat.id == file.category_id)
            file_data[category_name] += 1
    print(file_data)
    return render_template(
        'admin/dashboard.html',
        total_count=total_count,
        pendingCount=pending_count,
        file_data=file_data  
    )