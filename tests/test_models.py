import unittest
from app import create_app, db
from app.models import User, Post

class TestModels(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_user_model(self):
        """Test User model."""
        # Create a user
        user = User(username='test_user', email='test@example.com', password='password123')
        db.session.add(user)
        db.session.commit()
        
        # Query the user
        queried_user = User.query.filter_by(username='test_user').first()
        
        # Assert user was created correctly
        self.assertIsNotNone(queried_user)
        self.assertEqual(queried_user.email, 'test@example.com')
        self.assertFalse(queried_user.is_admin)
        
        # Test password hashing
        self.assertNotEqual(queried_user.password_hash, 'password123')
        self.assertTrue(queried_user.check_password('password123'))
        self.assertFalse(queried_user.check_password('wrong_password'))
    
    def test_post_model(self):
        """Test Post model."""
        # Create a user
        user = User(username='test_user', email='test@example.com', password='password123')
        db.session.add(user)
        db.session.commit()
        
        # Create a post
        post = Post(title='Test Post', content='This is a test post content', user_id=user.id)
        db.session.add(post)
        db.session.commit()
        
        # Query the post
        queried_post = Post.query.filter_by(title='Test Post').first()
        
        # Assert post was created correctly
        self.assertIsNotNone(queried_post)
        self.assertEqual(queried_post.content, 'This is a test post content')
        self.assertEqual(queried_post.user_id, user.id)
