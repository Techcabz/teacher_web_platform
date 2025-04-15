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
    elif request.method == 'DELETE':
        if users_id:
            existing_category = user_services.get_one(id=users_id)
            if not existing_category:
                return jsonify({'success': False, 'message': 'Users not found.'}), 404
            delete_success = user_services.delete(users_id)
            if delete_success:
                return jsonify({'success': True, 'message': 'Users deleted successfully!'}), 200
            return jsonify({'success': False, 'message': 'Error deleting Users.'}), 500

    return jsonify({'success': False, 'message': 'Create method must be POST.'}), 405

def adminList(request,users_id=None):
    if request.method == 'GET':
        users = user_services.get()
       
        return render_template('admin/management.html', users=users)
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
    
        user_services.delete(users_id)
        return jsonify({'success': False, 'message': 'User remove successfully.'}), 200
    
    return jsonify({'success': False, 'message': 'Create method must be DELETE.'}), 405

def get_profiles_admin(users_id):
    user = user_services.get_one(id=users_id)
   
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    user_data = {
        "id": user.id,
        "username": user.username,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "middlename": user.middlename,
        "email": user.email,
        "status": user.status,
      
        "role": user.role,
       
    }
    return jsonify({"success": True, "user": user_data})

def update_profile_user():
    data = request.json
    user_id = data.get("profile_user_id")
    user = user_services.get_one(id=user_id)
 
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    # Fields to update
    update_data = {
        "firstname": data.get("afname"),
        "middlename": None if data.get("amname") == "N/A" else data.get("amname"),
        "lastname": data.get("alname"),
        "email": data.get("email"),
    }

    new_password = data.get("newPassword")
    print(update_data)
    if new_password:  
        password_error = Validation.is_valid_password(new_password)
        if password_error:
            return jsonify({"success": False, "message": password_error}), 400

        user.set_password(new_password) 
    updated_user = user_services.update(user_id, **update_data)

    if updated_user:
        return jsonify({"success": True, "message": "Profile updated successfully"})
    else:
        return jsonify({"success": False, "message": "Error updating profile"}), 500


def dashboard_report():
     # Fetch categories
    categories = category_services.get()
    files = file_services.get()  
    users = user_services.get()

    pending_count = sum(1 for user in users if user.status == 0)
    total_count = len(users)
    total_file = len(files)
   
    
    file_data = {category.name: 0 for category in categories}  

    for file in files:
        if file.category_id in [category.id for category in categories]:
            category_name = next(cat.name for cat in categories if cat.id == file.category_id)
            file_data[category_name] += 1
    print(file_data)
    return render_template(
        'admin/dashboard.html',
        total_count=total_count,
        total_file=total_file,
        pendingCount=pending_count,
        file_data=file_data  
    )