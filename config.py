import os
from urllib.parse import urlparse
import psycopg2

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    DB_TYPE = os.getenv("DB_TYPE", "postgresql").lower()
    
    if DB_TYPE == "mysql":
        MYSQL_DATABASE_URL = os.getenv("MYSQL_DATABASE_URL", "mysql+pymysql://root:@localhost/adhoc")
        parsed_url = urlparse(MYSQL_DATABASE_URL)

        SQLALCHEMY_DATABASE_URI = MYSQL_DATABASE_URL
        MYSQL_USER = parsed_url.username
        MYSQL_PASSWORD = parsed_url.password
        MYSQL_HOST = parsed_url.hostname
        MYSQL_PORT = parsed_url.port or 3306
        MYSQL_DB_NAME = parsed_url.path.lstrip("/")

    elif DB_TYPE == "postgresql":
        POSTGRESQL_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL", "postgresql+psycopg2://postgres:@localhost/adhoc")
        parsed_url = urlparse(POSTGRESQL_DATABASE_URL)

        SQLALCHEMY_DATABASE_URI = POSTGRESQL_DATABASE_URL
        POSTGRESQL_USER = parsed_url.username
        POSTGRESQL_PASSWORD = parsed_url.password
        POSTGRESQL_HOST = parsed_url.hostname
        POSTGRESQL_PORT = parsed_url.port or 5432
        POSTGRESQL_DB_NAME = parsed_url.path.lstrip("/")

    else:
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

    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH, exist_ok=True)

    @classmethod
    def Initialize_database(cls):
        """Auto-create MySQL DB if it doesn't exist. PostgreSQL/SQLite handled outside."""
        if cls.DB_TYPE == "mysql":
            import pymysql
            try:
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
                print(f"Error initializing MySQL database: {e}")
        elif cls.DB_TYPE == "postgresql":
            try:
                # Connect to the default 'postgres' DB to issue CREATE DATABASE
                conn = psycopg2.connect(
                    dbname='postgres',
                    user=cls.POSTGRESQL_USER,
                    password=cls.POSTGRESQL_PASSWORD,
                    host=cls.POSTGRESQL_HOST,
                    port=cls.POSTGRESQL_PORT
                )
                conn.autocommit = True
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = %s", (cls.POSTGRESQL_DB_NAME,))
                    exists = cursor.fetchone()
                    if not exists:
                        cursor.execute(f"CREATE DATABASE {cls.POSTGRESQL_DB_NAME}")
                conn.close()
            except Exception as e:
                print(f"Error initializing PostgreSQL database: {e}")
            

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    TEMPLATES_AUTO_RELOAD = True

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
    SESSION_COOKIE_SECURE = True
