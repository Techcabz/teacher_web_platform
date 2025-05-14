import os
from urllib.parse import urlparse

class Config:
    # Base directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Decide database type: 'sqlite' or 'mysql'
    DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()

    if DB_TYPE == "mysql":
        # MySQL configuration using pymysql
        MYSQL_DATABASE_URL = os.getenv("MYSQL_DATABASE_URL", "mysql+pymysql://root:@localhost/adhoc")
        parsed_url = urlparse(MYSQL_DATABASE_URL)

        SQLALCHEMY_DATABASE_URI = MYSQL_DATABASE_URL
        MYSQL_USER = parsed_url.username
        MYSQL_PASSWORD = parsed_url.password
        MYSQL_HOST = parsed_url.hostname
        MYSQL_PORT = parsed_url.port or 3306
        MYSQL_DB_NAME = parsed_url.path.lstrip("/")
    else:
        # SQLite configuration
        SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", os.path.join(BASE_DIR, "app.db"))
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_DB_PATH}"
        
    # Common configurations
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_URL = os.getenv("API_URL", "")
    API_KEY = os.getenv("API_KEY", "")
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24).hex())

    SESSION_COOKIE_SECURE = True
    JSON_SORT_KEYS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    FILE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
    UPLOAD_PATH = os.getenv("UPLOAD_PATH", os.path.join(FILE_DIR, r"app\static\upload"))

    # Ensure the directory exists
    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH, exist_ok=True)

    @classmethod
    def Initialize_database(cls):
        """Auto-create MySQL database if selected and doesn't exist."""
        if cls.DB_TYPE == "mysql":
            import pymysql
            try:
                # Connect to MySQL server without specifying the database
                connection = pymysql.connect(
                    host=cls.MYSQL_HOST,
                    user=cls.MYSQL_USER,
                    password=cls.MYSQL_PASSWORD,
                    port=cls.MYSQL_PORT
                )
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {cls.MYSQL_DB_NAME}")
                    connection.commit()
                finally:
                    connection.close()
            except pymysql.MySQLError as e:
                print(f"Error initializing database: {e}")

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    TEMPLATES_AUTO_RELOAD = True

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
    SESSION_COOKIE_SECURE = True
