import unittest
import json
import base64
from app import create_app, db
from app.models import User, Post

def get_auth_headers(username, password):
    """Generate Basic Auth headers for testing."""
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode('utf-8')
    return {'Authorization': f'Basic {encoded}'}

class TestAPI(unittest.TestCase):
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
        
        # Create test users
        self.test_user = User(username='testuser', email='test@example.com', password='password')
        db.session.add(self.test_user)
        
        # Create test posts
        self.test_post = Post(title='Test Post', content='This is a test post', user_id=1)
        db.session.add(self.test_post)
        
        db.session.commit()
    
    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_get_users(self):
        """Test getting all users."""
        # This should fail without authentication
        response = self.client.get('/api/v1/users')
        self.assertEqual(response.status_code, 401)
        
        # This should succeed with authentication
        headers = get_auth_headers('testuser', 'password')
        response = self.client.get('/api/v1/users', headers=headers)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['username'], 'testuser')
    
    def test_get_user(self):
        """Test getting a specific user."""
        # This should fail without authentication
        response = self.client.get('/api/v1/users/1')
        self.assertEqual(response.status_code, 401)
        
        # This should succeed with authentication
        headers = get_auth_headers('testuser', 'password')
        response = self.client.get('/api/v1/users/1', headers=headers)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')
    
    def test_create_user(self):
        """Test creating a new user."""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword'
        }
        
        response = self.client.post('/api/v1/users', 
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        # Verify the user was created
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'new@example.com')
    
    def test_get_posts(self):
        """Test getting all posts."""
        response = self.client.get('/api/v1/posts')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Test Post')
    
    def test_get_post(self):
        """Test getting a specific post."""
        response = self.client.get('/api/v1/posts/1')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Test Post')
        self.assertEqual(data['content'], 'This is a test post')
    
    def test_create_post(self):
        """Test creating a new post."""
        data = {
            'title': 'New Post',
            'content': 'This is a new post',
            'user_id': 1
        }
        
        # This should fail without authentication
        response = self.client.post('/api/v1/posts', 
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 401)
        
        # This should succeed with authentication
        headers = get_auth_headers('testuser', 'password')
        response = self.client.post('/api/v1/posts', 
                                   data=json.dumps(data),
                                   content_type='application/json',
                                   headers=headers)
        self.assertEqual(response.status_code, 201)
        
        # Verify the post was created
        post = Post.query.filter_by(title='New Post').first()
        self.assertIsNotNone(post)
        self.assertEqual(post.content, 'This is a new post')
