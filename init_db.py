"""
Database initialization script.
Run this script to create the initial database and tables.
"""
import os
import click
from flask.cli import with_appcontext
from app import create_app, db
from app.models import User, Post

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db.drop_all()
    db.create_all()
    
    # Create a default admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        password='adminpassword',
        is_admin=True
    )
    
    # Create a default regular user
    user = User(
        username='user',
        email='user@example.com',
        password='userpassword'
    )
    
    # Create some sample posts
    post1 = Post(
        title='Welcome to Flask Web Template',
        content='This is a sample post to demonstrate the functionality of the application.',
        user_id=1
    )
    
    post2 = Post(
        title='Getting Started with Flask',
        content='Flask is a lightweight WSGI web application framework in Python.',
        user_id=1
    )
    
    # Add to database
    db.session.add(admin)
    db.session.add(user)
    db.session.commit()  # Commit to get user IDs
    
    db.session.add(post1)
    db.session.add(post2)
    db.session.commit()
    
    click.echo('Initialized the database with sample data.')

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        init_db_command()
