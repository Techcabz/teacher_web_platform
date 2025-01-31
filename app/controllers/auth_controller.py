from flask import flash, redirect, url_for, request,render_template
from flask_login import login_user,logout_user
from flask import session
from app.services.user_services import UserService
from app.utils.validation_utils import Validation
from app.extensions import db
from flask import jsonify


def login_user_controller(request):
    if request.method == 'GET':
        return render_template('auth/login.html')

    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserService.get_user_by_username(username)
        
        if user and user.check_password(password):
            login_user(user)
            session['role'] = user.role
            return jsonify({'success': True, 'message': 'Login successful! Redirecting...'}), 200

        else:
            return jsonify({'success': False, 'message': 'Invalid username or password.'}), 400
    return jsonify({'success': False, 'message': 'Login method must be POST.'}), 405


def register_user_controller(request):
    if request.method == 'GET':
        return render_template('auth/register.html')

    elif request.method == 'POST':
        username = request.form.get('username').lower()
        firstname = request.form.get('firstname').lower()
        lastname = request.form.get('lastname').lower()
        middlename = request.form.get('middlename', '').lower()  # Optional
        grade = request.form.get('grade')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

      
        if not all([username, firstname, lastname, grade, email, password, confirm_password]):
            return jsonify({'success': False, 'message': 'All fields are required.'}), 400

        # Validate passwords match
        if password != confirm_password:
            return jsonify({'success': False, 'message': 'Passwords do not match.'}), 400

        # Check if username already exists
        if UserService.get_user_by_username(username):
            return jsonify({'success': False, 'message': 'Username is already taken.'}), 400

        # Create new user
        new_user = UserService.create_user(
            username=username,
            firstname=firstname,
            lastname=lastname,
            middlename=middlename,
            grade=grade,
            email=email,
            password=password,
            role='teacher',
        )

        if new_user:
            return jsonify({'success': True, 'message': 'Registration successful! Please log in.'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to register. Please try again.'}), 500

    return jsonify({'success': False, 'message': 'Invalid request method.'}), 405

def logout_user_controller():
    if request.method == 'POST':
        logout_user()
        session.clear() 
        return jsonify({'success': True, 'message': 'You have been logged out'}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid request method.'}), 405