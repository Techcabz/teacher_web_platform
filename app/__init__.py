import os
from flask import Flask, render_template
from flask_login import LoginManager
from config import DevelopmentConfig, ProductionConfig
from app.models.user_models import User
from app.services.user_services import UserService
from app.extensions import db

def create_app():
    app = Flask(__name__)
    
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Initialize SQLAlchemy
    db.init_app(app)
    with app.app_context():
        db.create_all()
        UserService.create_default_admin()
        
    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  
    login_manager.login_message = "Please log in to access this page."

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.views.view import main
    from app.views.view import admin
    app.register_blueprint(main)
    app.register_blueprint(admin)

    # Error handler for 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # Error handler for 500 (optional)
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
  
    return app
