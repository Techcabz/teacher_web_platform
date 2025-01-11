from flask import flash, redirect, url_for, request
from flask_login import login_user,logout_user
from flask import session
from app.services.user_services import UserService
from ..extensions import db

def login_user_controller(request):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserService.get_user_by_username(username)
        
        if user and user.check_password(password):
            login_user(user)
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard')) 
        else:
            flash('Invalid email or password.', 'danger')

    return None

def register_user_controller(request):
     if request.method == 'POST':
        username = request.form.get('username')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        middlename = request.form.get('middlename', '')  # Optional
        grade = request.form.get('grade')
        email = request.form.get('email')
        
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate required fields
        if not all([username, firstname, lastname, grade, email, password, confirm_password]):
            flash('All fields are required.', 'danger')
            return None

        # Validate passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return None

        # Check if username already exists
        if UserService.get_user_by_username(username):
            flash('Username is already taken.', 'danger')
            return None

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
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('main.login'))
        else:
            flash('Failed to register. Please try again.', 'danger')

     return None

def logout_user_controller():
    logout_user()
    session.clear() 
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))