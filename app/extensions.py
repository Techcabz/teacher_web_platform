from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter

db = SQLAlchemy()
migrate = Migrate()