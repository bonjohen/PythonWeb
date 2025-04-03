from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app import db
from app.models import User
from app.api.errors import unauthorized

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    """Verify username and password."""
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)

@basic_auth.error_handler
def basic_auth_error():
    """Return 401 error for basic auth failures."""
    return unauthorized('Invalid credentials')

@token_auth.verify_token
def verify_token(token):
    """Verify authentication token."""
    # In a real application, you would implement token-based authentication here
    # For simplicity, we'll just use basic auth for now
    if token == 'test-token':
        g.current_user = db.session.get(User, 1)  # Use the first user for testing
        return True
    return False

@token_auth.error_handler
def token_auth_error():
    """Return 401 error for token auth failures."""
    return unauthorized('Invalid token')
