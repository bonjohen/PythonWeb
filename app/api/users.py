from flask import jsonify, request, url_for
from app import db
from app.models import User
from app.api import bp
from app.api.errors import bad_request, not_found
from app.api.auth import basic_auth

@bp.route('/users', methods=['GET'])
@basic_auth.login_required
def get_users():
    """Return list of all users."""
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        '_links': {
            'self': url_for('api.get_user', id=user.id)
        }
    } for user in users])

@bp.route('/users/<int:id>', methods=['GET'])
@basic_auth.login_required
def get_user(id):
    """Return a user."""
    user = db.session.get(User, id)
    if user is None:
        return not_found(f"User with id {id} not found")
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat() + 'Z',
        '_links': {
            'self': url_for('api.get_user', id=user.id),
            'users': url_for('api.get_users')
        }
    })

@bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('Must include username, email and password fields')

    if User.query.filter_by(username=data['username']).first():
        return bad_request('Please use a different username')

    if User.query.filter_by(email=data['email']).first():
        return bad_request('Please use a different email address')

    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(user)
    db.session.commit()

    response = jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        '_links': {
            'self': url_for('api.get_user', id=user.id)
        }
    })
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users/<int:id>', methods=['PUT'])
@basic_auth.login_required
def update_user(id):
    """Update a user."""
    user = db.session.get(User, id)
    if user is None:
        return not_found(f"User with id {id} not found")
    data = request.get_json() or {}

    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('Please use a different username')

    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('Please use a different email address')

    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        '_links': {
            'self': url_for('api.get_user', id=user.id)
        }
    })

@bp.route('/users/<int:id>', methods=['DELETE'])
@basic_auth.login_required
def delete_user(id):
    """Delete a user."""
    user = db.session.get(User, id)
    if user is None:
        return not_found(f"User with id {id} not found")
    db.session.delete(user)
    db.session.commit()
    return '', 204
