"""Integration tests for API endpoints."""
import json
import base64
from tests.integration.base import IntegrationTestCase
from app.models import User, Post
from app import db

def get_auth_headers(username, password):
    """Generate Basic Auth headers for testing."""
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode('utf-8')
    return {'Authorization': f'Basic {encoded}'}

class APIIntegrationTestCase(IntegrationTestCase):
    """Test API endpoints with database integration."""

    def test_get_users_with_db(self):
        """Test getting users from the API with database integration."""
        # Get authentication headers
        headers = get_auth_headers('admin', 'adminpassword')

        # Make request to API
        response = self.client.get('/api/v1/users', headers=headers)

        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Verify data matches database
        self.assertEqual(len(data), 2)  # admin and user
        self.assertEqual(data[0]['username'], 'admin')
        self.assertEqual(data[1]['username'], 'user')

    def test_get_user_with_db(self):
        """Test getting a specific user from the API with database integration."""
        # Get authentication headers
        headers = get_auth_headers('admin', 'adminpassword')

        # Make request to API
        response = self.client.get('/api/v1/users/1', headers=headers)

        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Verify data matches database
        self.assertEqual(data['username'], 'admin')
        self.assertEqual(data['email'], 'admin@example.com')

    def test_create_user_with_db(self):
        """Test creating a user through the API with database integration."""
        # Prepare data
        user_data = {
            'username': 'apiuser',
            'email': 'api@example.com',
            'password': 'apipassword'
        }

        # Make request to API
        response = self.client.post(
            '/api/v1/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )

        # Verify response
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['username'], 'apiuser')

        # Verify user was created in database
        user = User.query.filter_by(username='apiuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'api@example.com')

    def test_update_user_with_db(self):
        """Test updating a user through the API with database integration."""
        # Get authentication headers
        headers = get_auth_headers('admin', 'adminpassword')

        # Prepare data
        update_data = {
            'username': 'updated_admin',
            'email': 'updated_admin@example.com'
        }

        # Make request to API
        response = self.client.put(
            '/api/v1/users/1',
            data=json.dumps(update_data),
            content_type='application/json',
            headers=headers
        )

        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['username'], 'updated_admin')

        # Verify user was updated in database
        user = db.session.get(User, 1)
        self.assertEqual(user.username, 'updated_admin')
        self.assertEqual(user.email, 'updated_admin@example.com')

    def test_delete_user_with_db(self):
        """Test deleting a user through the API with database integration."""
        # Create a user to delete
        user = User(username='to_delete', email='delete@example.com', password='password')
        db.session.add(user)
        db.session.commit()
        user_id = user.id

        # Get authentication headers
        headers = get_auth_headers('admin', 'adminpassword')

        # Make request to API
        response = self.client.delete(f'/api/v1/users/{user_id}', headers=headers)

        # Verify response
        self.assertEqual(response.status_code, 204)

        # Verify user was deleted from database
        deleted_user = db.session.get(User, user_id)
        self.assertIsNone(deleted_user)

    def test_get_posts_with_db(self):
        """Test getting posts from the API with database integration."""
        # Make request to API
        response = self.client.get('/api/v1/posts')

        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Verify data matches database
        self.assertEqual(len(data), 2)  # Two test posts
        self.assertEqual(data[0]['title'], 'First Test Post')
        self.assertEqual(data[1]['title'], 'Second Test Post')

    def test_create_post_with_db(self):
        """Test creating a post through the API with database integration."""
        # Get authentication headers
        headers = get_auth_headers('admin', 'adminpassword')

        # Prepare data
        post_data = {
            'title': 'API Created Post',
            'content': 'This post was created through the API.',
            'user_id': 1
        }

        # Make request to API
        response = self.client.post(
            '/api/v1/posts',
            data=json.dumps(post_data),
            content_type='application/json',
            headers=headers
        )

        # Verify response
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'API Created Post')

        # Verify post was created in database
        post = Post.query.filter_by(title='API Created Post').first()
        self.assertIsNotNone(post)
        self.assertEqual(post.content, 'This post was created through the API.')
        self.assertEqual(post.user_id, 1)

    def test_full_api_workflow(self):
        """Test a complete API workflow with database integration."""
        # 1. Create a new user
        user_data = {
            'username': 'workflow',
            'email': 'workflow@example.com',
            'password': 'password'
        }

        response = self.client.post(
            '/api/v1/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        user_response = json.loads(response.data)
        user_id = user_response['id']

        # 2. Get authentication headers for the new user
        headers = get_auth_headers('workflow', 'password')

        # 3. Create a post as the new user
        post_data = {
            'title': 'Workflow Post',
            'content': 'This is part of the workflow test.',
            'user_id': user_id
        }

        response = self.client.post(
            '/api/v1/posts',
            data=json.dumps(post_data),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, 201)
        post_response = json.loads(response.data)
        post_id = post_response['id']

        # 4. Update the post
        update_data = {
            'title': 'Updated Workflow Post',
            'content': 'This post has been updated.'
        }

        response = self.client.put(
            f'/api/v1/posts/{post_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, 200)

        # 5. Verify the post was updated in the database
        post = db.session.get(Post, post_id)
        self.assertEqual(post.title, 'Updated Workflow Post')

        # 6. Delete the post
        response = self.client.delete(f'/api/v1/posts/{post_id}', headers=headers)
        self.assertEqual(response.status_code, 204)

        # 7. Verify the post was deleted
        deleted_post = db.session.get(Post, post_id)
        self.assertIsNone(deleted_post)

        # 8. Delete the user
        response = self.client.delete(f'/api/v1/users/{user_id}', headers=headers)
        self.assertEqual(response.status_code, 204)

        # 9. Verify the user was deleted
        deleted_user = db.session.get(User, user_id)
        self.assertIsNone(deleted_user)
