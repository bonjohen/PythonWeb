"""Integration tests for authentication flows."""
from tests.integration.base import IntegrationTestCase
from app.models import User
# No need for db import here

class AuthFlowTestCase(IntegrationTestCase):
    """Test authentication flows."""

    def test_login_logout_flow(self):
        """Test the login and logout flow."""
        # Test login with valid credentials
        response = self.login('admin@example.com', 'adminpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, admin', response.data)

        # Test logout
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Flask Web App', response.data)
        self.assertNotIn(b'Welcome, admin', response.data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        # Test login with invalid email
        response = self.login('nonexistent@example.com', 'password')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email or password', response.data)

        # Test login with invalid password
        response = self.login('admin@example.com', 'wrongpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email or password', response.data)

    def test_registration_flow(self):
        """Test the user registration flow."""
        # Test registration with new user
        response = self.client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)

        # Verify user was created in database
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'new@example.com')

        # Test login with new user
        response = self.login('new@example.com', 'newpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, newuser', response.data)

    def test_registration_validation(self):
        """Test registration form validation."""
        # Test registration with existing username
        response = self.client.post('/auth/register', data={
            'username': 'admin',  # Existing username
            'email': 'different@example.com',
            'password': 'password',
            'confirm_password': 'password'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'That username is already taken', response.data)

        # Test registration with existing email
        response = self.client.post('/auth/register', data={
            'username': 'different',
            'email': 'admin@example.com',  # Existing email
            'password': 'password',
            'confirm_password': 'password'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'That email is already registered', response.data)

        # Test registration with mismatched passwords
        response = self.client.post('/auth/register', data={
            'username': 'newuser2',
            'email': 'new2@example.com',
            'password': 'password1',
            'confirm_password': 'password2'  # Different password
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field must be equal to password', response.data)

    def test_protected_routes(self):
        """Test access to protected routes."""
        # Try to access dashboard without login
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in to access this page', response.data)

        # Login and access dashboard
        self.login('admin@example.com', 'adminpassword')
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to your dashboard', response.data)
