from functools import wraps
from ..utils.auth_utils import is_authenticated, has_admin_role, redirect_to_login

def web_guard(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if the user is logged in
        if not is_authenticated():
            return redirect_to_login()

        # Check if the user has an admin role
        if not has_admin_role():
            return redirect_to_login('Access denied: Admins only!')
        
        # Proceed to the requested function
        return func(*args, **kwargs)
    return wrapper
