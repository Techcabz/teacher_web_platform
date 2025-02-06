from flask import  request,render_template
from flask import jsonify
from app.services.services import CRUDService
from app.models.category_models import Category
from app.utils.validation_utils import Validation

category_service = CRUDService(Category)


def categories(request, category_id=None):
    if request.method == 'GET':
        if category_id:
            # Fetch a single inventory item by ID
            category = category_service.get_one(id=category_id)
            if not category:
                return jsonify({'success': False, 'message': 'Category not found'}), 404

            return jsonify(category.serialize()), 200
        categories = category_service.get()
    
        return render_template('admin/category.html', categories=categories)
    elif request.method == 'POST':
        name = request.form['ciname']

        if  Validation.has_repeated_characters(name):
            return jsonify({'success': False, 'message': 'Name must not have three or more consecutive repeated characters.'}), 400
        
        existing_category = category_service.get_one(name=name)
        if existing_category:
            return jsonify({'success': False, 'message': 'Category name is already taken.'}), 400
        
        new_category = category_service.create(name=name)
        if new_category:
            return jsonify({'success': True, 'message': 'Category created successfully!'}), 201
        
    elif request.method == 'PUT':
        # Handle updating a category
        print('category_id', category_id)
        if category_id:
            name = request.form['ciname']
            existing_category = category_service.get_one(id=category_id)
            if not existing_category:
                return jsonify({'success': False, 'message': 'Category not found.'}), 404
        
            updated_category = category_service.update(category_id, name=name)
            if updated_category:
                return jsonify({'success': True, 'message': 'Category updated successfully!'}), 200
        return jsonify({'success': False, 'message': 'Error updating category.'}), 500

    elif request.method == 'DELETE':
        if category_id:
            existing_category = category_service.get_one(id=category_id)
            if not existing_category:
                return jsonify({'success': False, 'message': 'Category not found.'}), 404
            delete_success = category_service.delete(category_id)
            if delete_success:
                return jsonify({'success': True, 'message': 'Category deleted successfully!'}), 200
            return jsonify({'success': False, 'message': 'Error deleting category.'}), 500

    return jsonify({'success': False, 'message': 'Create method must be POST.'}), 405