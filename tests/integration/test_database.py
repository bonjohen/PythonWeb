"""Integration tests for database operations."""
from tests.integration.base import IntegrationTestCase
from app.models import User, Post
from app import db
# No need for datetime import here

class DatabaseTestCase(IntegrationTestCase):
    """Test database operations."""

    def test_create_user(self):
        """Test creating a user in the database."""
        # Create a new user
        user = User(
            username='testuser',
            email='test@test.com',
            password='testpassword'
        )

        # Add user to database
        db.session.add(user)
        db.session.commit()

        # Retrieve user from database
        retrieved_user = User.query.filter_by(username='testuser').first()

        # Verify user was created correctly
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, 'test@test.com')
        self.assertTrue(retrieved_user.check_password('testpassword'))
        self.assertFalse(retrieved_user.is_admin)

    def test_update_user(self):
        """Test updating a user in the database."""
        # Get existing user
        user = User.query.filter_by(username='user').first()

        # Update user
        user.username = 'updated_user'
        user.email = 'updated@example.com'
        user.set_password('newpassword')

        # Commit changes
        db.session.commit()

        # Retrieve updated user
        updated_user = db.session.get(User, user.id)

        # Verify user was updated correctly
        self.assertEqual(updated_user.username, 'updated_user')
        self.assertEqual(updated_user.email, 'updated@example.com')
        self.assertTrue(updated_user.check_password('newpassword'))

    def test_delete_user(self):
        """Test deleting a user from the database."""
        # Get existing user
        user = User.query.filter_by(username='user').first()
        user_id = user.id

        # Delete user
        db.session.delete(user)
        db.session.commit()

        # Try to retrieve deleted user
        deleted_user = db.session.get(User, user_id)

        # Verify user was deleted
        self.assertIsNone(deleted_user)

    def test_create_post(self):
        """Test creating a post in the database."""
        # Create a new post
        post = Post(
            title='Test Post',
            content='This is a test post.',
            user_id=1  # admin user
        )

        # Add post to database
        db.session.add(post)
        db.session.commit()

        # Retrieve post from database
        retrieved_post = Post.query.filter_by(title='Test Post').first()

        # Verify post was created correctly
        self.assertIsNotNone(retrieved_post)
        self.assertEqual(retrieved_post.content, 'This is a test post.')
        self.assertEqual(retrieved_post.user_id, 1)

    def test_update_post(self):
        """Test updating a post in the database."""
        # Get existing post
        post = Post.query.filter_by(title='First Test Post').first()

        # Update post
        post.title = 'Updated Post'
        post.content = 'This post has been updated.'

        # Commit changes
        db.session.commit()

        # Retrieve updated post
        updated_post = db.session.get(Post, post.id)

        # Verify post was updated correctly
        self.assertEqual(updated_post.title, 'Updated Post')
        self.assertEqual(updated_post.content, 'This post has been updated.')

    def test_delete_post(self):
        """Test deleting a post from the database."""
        # Get existing post
        post = Post.query.filter_by(title='First Test Post').first()
        post_id = post.id

        # Delete post
        db.session.delete(post)
        db.session.commit()

        # Try to retrieve deleted post
        deleted_post = db.session.get(Post, post_id)

        # Verify post was deleted
        self.assertIsNone(deleted_post)

    def test_cascade_delete(self):
        """Test that deleting a user cascades to their posts."""
        # Create a new user with posts
        user = User(
            username='cascade_user',
            email='cascade@example.com',
            password='password'
        )
        db.session.add(user)
        db.session.commit()

        # Add posts for this user
        post1 = Post(title='Cascade Post 1', content='Content 1', user_id=user.id)
        post2 = Post(title='Cascade Post 2', content='Content 2', user_id=user.id)
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()

        # Get post IDs
        post1_id = post1.id
        post2_id = post2.id

        # Delete the user
        db.session.delete(user)
        db.session.commit()

        # Verify the posts were also deleted
        self.assertIsNone(db.session.get(Post, post1_id))
        self.assertIsNone(db.session.get(Post, post2_id))
