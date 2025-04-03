import unittest
from flask import url_for
from app import create_app, db
from app.models import User

class TestRoutes(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.app = create_app('testing')

        # Configure the app for testing
        self.app.config['SERVER_NAME'] = 'localhost.localdomain'
        self.app.config['APPLICATION_ROOT'] = '/'
        self.app.config['PREFERRED_URL_SCHEME'] = 'http'
        self.app.config['TESTING'] = True

        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        """Test home page route."""
        response = self.client.get(url_for('main.index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Flask Web App', response.data)

    def test_about_page(self):
        """Test about page route."""
        response = self.client.get(url_for('main.about'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About This Project', response.data)

    def test_dashboard_redirect_if_not_logged_in(self):
        """Test dashboard redirects when not logged in."""
        response = self.client.get(url_for('main.dashboard'), follow_redirects=False)
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_login_page(self):
        """Test login page route."""
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register_page(self):
        """Test register page route."""
        response = self.client.get(url_for('auth.register'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)
