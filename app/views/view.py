from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import  current_user
from ..controllers.auth_controller import login_user_controller,logout_user_controller,register_user_controller
from ..utils.web_utils import web_guard
from ..models.user_models import User
from ..extensions import db

main = Blueprint('main', __name__)
admin = Blueprint('admin', __name__, url_prefix='/admin')

# AUTHENTICATION
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and request.endpoint != 'admin.dashboard':
        return redirect(url_for('admin.dashboard'))

    result = login_user_controller(request)
    if result:
        return result
    return render_template('auth/login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated and request.endpoint != 'admin.dashboard':
        return redirect(url_for('admin.dashboard'))

    result = register_user_controller(request)
    if result:
        return result
    return render_template('auth/register.html')

@main.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated and request.endpoint != 'admin.dashboard':
        return redirect(url_for('admin.dashboard'))

    result = register_user_controller(request)
    if result:
        return result
    return render_template('auth/login.html')

@main.route('/logout')
def logout():
    return logout_user_controller()


# ADMINISTRATOR
@admin.route('/dashboard')
@web_guard
def dashboard():
    return render_template('admin/dashboard.html')
