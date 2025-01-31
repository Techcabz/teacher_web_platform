from flask import redirect, url_for, session, flash
from flask_login import current_user
from functools import wraps

def web_guard(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('main.login')) 

        if session.get('role') != 'admin': 
            flash('Access denied: Admins only!', 'error')
            return redirect(url_for('main.login')) 
        return func(*args, **kwargs)
    return wrapper
