from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import  current_user
from app.controllers.auth_controller import login_user_controller,logout_user_controller,register_user_controller
from app.models.user_models import User
from app.models.category_models import Category
from app.models.file_models import File
from app.extensions import db
from app.utils.auth_utils import web_guard

from app.controllers.categories_controller import categories
from app.controllers.files_controller import files

main = Blueprint('main', __name__)
admin = Blueprint('admin', __name__, url_prefix='/admin')

# AUTHENTICATION
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and request.endpoint != 'admin.dashboard':
        return redirect(url_for('admin.dashboard'))
    return login_user_controller(request)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated and request.endpoint != 'admin.dashboard':
        return redirect(url_for('admin.dashboard'))

    return register_user_controller(request)

@main.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated and request.endpoint != 'admin.dashboard':
        return redirect(url_for('admin.dashboard'))

    result = register_user_controller(request)
    if result:
        return result
    return render_template('auth/login.html')

@main.route('/logout', methods=['GET', 'POST'])
def logout():
    return logout_user_controller()


# ADMINISTRATOR
@admin.route('/dashboard')
@web_guard
def dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/category',methods=['GET', 'POST'])
@admin.route('/category/<int:categoryy_id>', methods=['GET', 'PUT', 'DELETE'])
@web_guard
def category(categoryy_id=None):
    return categories(request,categoryy_id)

@admin.route('/docs',methods=['GET', 'POST', 'PUT', 'DELETE'])
@web_guard
def docs():
    return files(request)

@admin.route('/docs/<slug>')
@web_guard
def view_folder(slug):
    category = Category.query.filter_by(slug=slug).first()
    
    files = category.files 
    return render_template('admin/single.html', category=category, files=files)

@admin.route('/management')
@web_guard
def management():
    return render_template('admin/management.html')

