from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    """Home page route."""
    return render_template('index.html', title='Home')

@bp.route('/about')
def about():
    """About page route."""
    return render_template('about.html', title='About')

@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page route (requires login)."""
    return render_template('dashboard.html', title='Dashboard')

@bp.route('/api/docs')
def api_docs():
    """API documentation page."""
    return render_template('api_docs.html', title='API Documentation')
