from flask import redirect, url_for, flash, session
from flask_login import current_user

def is_authenticated():
    """Check if the user is logged in."""
    return current_user.is_authenticated

def has_admin_role():
    """Check if the user has an admin role."""
    return session.get('role') == 'admin'

def redirect_to_login(message='Please log in to access this page.'):
    """Redirect to the login page with a flash message."""
    flash(message, 'danger')
    return redirect(url_for('main.login'))
