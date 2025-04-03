import os
import sys
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from different .env files based on instance name
def load_env_files():
    # Always load the base .env file first
    load_dotenv(os.path.join(basedir, '.env'))

    # Check for instance-specific .env file
    instance = os.environ.get('FLASK_INSTANCE')
    if instance:
        instance_env = os.path.join(basedir, f'.env.{instance}')
        if os.path.exists(instance_env):
            load_dotenv(instance_env, override=True)
            print(f"Loaded instance-specific environment from {instance_env}")

    # Check for environment-specific .env file
    env = os.environ.get('FLASK_ENV') or os.environ.get('FLASK_CONFIG')
    if env:
        env_file = os.path.join(basedir, f'.env.{env}')
        if os.path.exists(env_file):
            load_dotenv(env_file, override=True)
            print(f"Loaded environment-specific settings from {env_file}")

# Load environment variables
load_env_files()

class Config:
    """Base configuration class."""
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Server settings
    SERVER_HOST = os.environ.get('SERVER_HOST') or '127.0.0.1'
    SERVER_PORT = int(os.environ.get('SERVER_PORT') or 5000)

    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_PORT = int(os.environ.get('DB_PORT') or 5432)  # Default PostgreSQL port

    # Mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']

    # Redis settings (for potential future use with caching/sessions)
    REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
    REDIS_PORT = int(os.environ.get('REDIS_PORT') or 6379)

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SERVER_PORT = int(os.environ.get('DEV_SERVER_PORT') or 5000)

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SERVER_PORT = int(os.environ.get('TEST_SERVER_PORT') or 5001)  # Different port for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SERVER_HOST = os.environ.get('PROD_SERVER_HOST') or '0.0.0.0'  # Bind to all interfaces
    SERVER_PORT = int(os.environ.get('PROD_SERVER_PORT') or 8000)  # Use a different port for production

    # Use Gunicorn/uWSGI in production
    WSGI_SERVER_PORT = int(os.environ.get('WSGI_SERVER_PORT') or 8000)

    # Web server settings (Nginx/Apache)
    WEB_SERVER_HTTP_PORT = int(os.environ.get('WEB_SERVER_HTTP_PORT') or 80)
    WEB_SERVER_HTTPS_PORT = int(os.environ.get('WEB_SERVER_HTTPS_PORT') or 443)

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
