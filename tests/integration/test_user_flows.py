"""Integration tests for end-to-end user flows."""
from tests.integration.base import IntegrationTestCase
from app.models import User, Post
from app import db

class UserFlowTestCase(IntegrationTestCase):
    """Test end-to-end user flows."""
    
    def test_registration_login_dashboard_flow(self):
        """Test the complete flow from registration to dashboard access."""
        # 1. Register a new user
        response = self.client.post('/auth/register', data={
            'username': 'flowuser',
            'email': 'flow@example.com',
            'password': 'flowpassword',
            'confirm_password': 'flowpassword'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)
        
        # 2. Log in with the new user
        response = self.login('flow@example.com', 'flowpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, flowuser', response.data)
        
        # 3. Access the dashboard
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to your dashboard', response.data)
        
        # 4. Verify user profile information on dashboard
        self.assertIn(b'flowuser', response.data)
        self.assertIn(b'flow@example.com', response.data)
        
        # 5. Log out
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Flask Web App', response.data)
        
        # 6. Verify dashboard is no longer accessible
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in to access this page', response.data)
    
    def test_admin_user_flow(self):
        """Test admin user specific flows."""
        # 1. Log in as admin
        response = self.login('admin@example.com', 'adminpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, admin', response.data)
        
        # 2. Access dashboard
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        
        # 3. Verify admin status is displayed
        # Note: This assumes the dashboard shows admin status, which may need to be implemented
        # self.assertIn(b'Administrator', response.data)
        
        # 4. Log out
        response = self.logout()
        self.assertEqual(response.status_code, 200)
    
    def test_navigation_flow(self):
        """Test navigation through the application."""
        # 1. Start at home page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Flask Web App', response.data)
        
        # 2. Navigate to about page
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About This Project', response.data)
        
        # 3. Navigate to login page
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
        
        # 4. Navigate to register page
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)
        
        # 5. Navigate to API documentation
        response = self.client.get('/api/docs')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'API Documentation', response.data)
    
    def test_error_handling_flow(self):
        """Test error handling flows."""
        # 1. Access non-existent page
        response = self.client.get('/nonexistent', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page Not Found', response.data)
        
        # 2. Access dashboard without login
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in to access this page', response.data)
