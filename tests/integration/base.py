"""Base class for integration tests."""
import os
import tempfile
import unittest
from app import create_app, db
from app.models import User, Post
from config import config

class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary database file
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        # Configure the app for testing
        self.app = create_app('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{self.db_path}'
        self.app.config['SERVER_NAME'] = 'localhost.localdomain'
        self.app.config['APPLICATION_ROOT'] = '/'
        self.app.config['PREFERRED_URL_SCHEME'] = 'http'
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        
        # Create application context and test client
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)
        
        # Create database tables
        db.create_all()
        
        # Set up test data
        self.setup_test_data()
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove database session
        db.session.remove()
        
        # Drop all tables
        db.drop_all()
        
        # Close application context
        self.app_context.pop()
        
        # Close and remove temporary database file
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def setup_test_data(self):
        """Set up test data in the database."""
        # Create test users
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            is_admin=True
        )
        
        regular_user = User(
            username='user',
            email='user@example.com',
            password='userpassword'
        )
        
        # Add users to database
        db.session.add(admin_user)
        db.session.add(regular_user)
        db.session.commit()
        
        # Create test posts
        post1 = Post(
            title='First Test Post',
            content='This is the first test post content.',
            user_id=1  # admin user
        )
        
        post2 = Post(
            title='Second Test Post',
            content='This is the second test post content.',
            user_id=2  # regular user
        )
        
        # Add posts to database
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()
    
    def login(self, email, password):
        """Helper method to log in a user."""
        return self.client.post('/auth/login', data={
            'email': email,
            'password': password,
            'remember_me': False
        }, follow_redirects=True)
    
    def logout(self):
        """Helper method to log out a user."""
        return self.client.get('/auth/logout', follow_redirects=True)
