from flask import jsonify, request, url_for
from app import db
from app.models import Post, User
from app.api import bp
from app.api.errors import bad_request, not_found
from app.api.auth import basic_auth

@bp.route('/posts', methods=['GET'])
def get_posts():
    """Return list of all posts."""
    posts = Post.query.all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at.isoformat() + 'Z',
        'user_id': post.user_id,
        '_links': {
            'self': url_for('api.get_post', id=post.id),
            'author': url_for('api.get_user', id=post.user_id)
        }
    } for post in posts])

@bp.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    """Return a post."""
    post = db.session.get(Post, id)
    if post is None:
        return not_found(f"Post with id {id} not found")
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at.isoformat() + 'Z',
        'user_id': post.user_id,
        '_links': {
            'self': url_for('api.get_post', id=post.id),
            'author': url_for('api.get_user', id=post.user_id),
            'posts': url_for('api.get_posts')
        }
    })

@bp.route('/posts', methods=['POST'])
@basic_auth.login_required
def create_post():
    """Create a new post."""
    data = request.get_json() or {}
    if 'title' not in data or 'content' not in data or 'user_id' not in data:
        return bad_request('Must include title, content and user_id fields')

    # Verify user exists
    user = db.session.get(User, data['user_id'])
    if user is None:
        return bad_request('Invalid user_id')

    post = Post(
        title=data['title'],
        content=data['content'],
        user_id=data['user_id']
    )
    db.session.add(post)
    db.session.commit()

    response = jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at.isoformat() + 'Z',
        'user_id': post.user_id,
        '_links': {
            'self': url_for('api.get_post', id=post.id),
            'author': url_for('api.get_user', id=post.user_id)
        }
    })
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_post', id=post.id)
    return response

@bp.route('/posts/<int:id>', methods=['PUT'])
@basic_auth.login_required
def update_post(id):
    """Update a post."""
    post = db.session.get(Post, id)
    if post is None:
        return not_found(f"Post with id {id} not found")
    data = request.get_json() or {}

    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']

    db.session.commit()
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at.isoformat() + 'Z',
        'user_id': post.user_id,
        '_links': {
            'self': url_for('api.get_post', id=post.id),
            'author': url_for('api.get_user', id=post.user_id)
        }
    })

@bp.route('/posts/<int:id>', methods=['DELETE'])
@basic_auth.login_required
def delete_post(id):
    """Delete a post."""
    post = db.session.get(Post, id)
    if post is None:
        return not_found(f"Post with id {id} not found")
    db.session.delete(post)
    db.session.commit()
    return '', 204
