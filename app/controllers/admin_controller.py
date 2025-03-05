from flask import  request,render_template
from flask import jsonify
from app.services.services import CRUDService
from app.models.user_models import User
from app.utils.validation_utils import Validation

user_services = CRUDService(User)

def cusers(request,users_id=None):
    if request.method == 'GET':
        users = user_services.get()
        pending_count = sum(1 for user in users if user.status == 0)
        print(users)
        return render_template('admin/users.html', users=users, pendingCount=pending_count)
    elif request.method == 'POST':
        return render_template('admin/users.html', users=users)
    elif request.method == 'PUT':
        # Handle updating a category
        # category_id = request.form['id']
        # name = request.form['name'].strip().lower()
        
        # if not all([category_id, name]):
        #     return jsonify({'success': False, 'message': 'All fields are required.'}), 400
        
        # existing_category = category_service.get_one(id=category_id)
        # if not existing_category:
        #     return jsonify({'success': False, 'message': 'Category not found.'}), 404
        
        # updated_category = category_service.update(category_id, name=name)
        # if updated_category:
        #     return jsonify({'success': True, 'message': 'Category updated successfully!'}), 200
        return jsonify({'success': False, 'message': 'Error updating category.'}), 500

    elif request.method == 'DELETE':
        # Handle deleting a category
        # category_id = request.form['id']
        
        # if not category_id:
        #     return jsonify({'success': False, 'message': 'Category ID is required.'}), 400
        
        # existing_category = category_service.get_one(id=category_id)
        # if not existing_category:
        #     return jsonify({'success': False, 'message': 'Category not found.'}), 404
        
        # delete_success = category_service.delete(category_id)
        # if delete_success:
        #     return jsonify({'success': True, 'message': 'Category deleted successfully!'}), 200
        return jsonify({'success': False, 'message': 'Error deleting category.'}), 500

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