from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None):
    """Create a JSON error response with the given status code and message."""
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

def bad_request(message):
    """400 Bad Request response."""
    return error_response(400, message)

def unauthorized(message):
    """401 Unauthorized response."""
    return error_response(401, message)

def forbidden(message):
    """403 Forbidden response."""
    return error_response(403, message)

def not_found(message):
    """404 Not Found response."""
    return error_response(404, message)

def internal_server_error(message):
    """500 Internal Server Error response."""
    return error_response(500, message)
