import re
from flask import flash, redirect, url_for, request, render_template, session, jsonify
from flask_login import login_user, logout_user
from app.services.user_services import UserService
from app.utils.validation_utils import Validation
from app.extensions import db


def login_user_controller(request):
    if request.method == 'GET':
        return render_template('auth/login.html')

    elif request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '')

        # Check for empty fields
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required.'}), 400

        user = UserService.get_user_by_username(username)

        # Check if user exists and password is correct
        if user and user.check_password(password):
            if user.status == 0:  # User is pending
                return jsonify({'success': False, 'message': 'Your account is pending approval. Please wait for admin approval.'}), 403

            login_user(user)
            session['role'] = user.role
            session['user_id'] = user.id
            session['username'] = user.username
            session['fullname'] = user.fullname
            session.permanent = True  # Set session expiration

            return jsonify({'success': True, 'message': 'Login successful! Redirecting...'}), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password.'}), 400

    return jsonify({'success': False, 'message': 'Invalid request method.'}), 405


def register_user_controller(request):
    if request.method == 'GET':
        return render_template('auth/register.html')

    elif request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        firstname = request.form.get('firstname', '').strip().lower()
        lastname = request.form.get('lastname', '').strip().lower()
        middlename = request.form.get('middlename', '').strip().lower() or None  # Optional
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validate required fields
        if not all([username, firstname, lastname, email, password, confirm_password]):
            return jsonify({'success': False, 'message': 'All fields are required.'}), 400

        # Validate name (only alphabetic characters)
        if not Validation.is_valid_name(firstname) or not Validation.is_valid_name(lastname):
            return jsonify({'success': False, 'message': 'Names must contain only alphabetic characters.'}), 400

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({'success': False, 'message': 'Invalid email format.'}), 400

        # Validate strong password
        if not Validation.is_strong_password(password):
            return jsonify({'success': False, 'message': 'Password must be at least 8 characters long, with uppercase, lowercase, a number, and a special character.'}), 400

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
        session.clear()  # Clear session data
        return jsonify({'success': True, 'message': 'You have been logged out'}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid request method.'}), 405
