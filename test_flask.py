from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

with app.app_context(): db.drop_all()
with app.app_context(): db.create_all()

class UserTestCase(TestCase):

    def setUp(self):
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User(first_name="Test", last_name="User", image_url="https://example.com/test.jpg")
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id

    def tearDown(self):
        with app.app_context():
            db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Test User', html)

    def test_create_user(self):
        with app.test_client() as client:
            response = client.post('/users/new', data={
                'first_name': 'New',
                'last_name': 'User',
                'image_url': 'https://example.com/new.jpg'
            }, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('New User', html)

    def test_show_user(self):
        with app.test_client() as client:
            response = client.get(f'/users/{self.user_id}')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Test User', html)

    def test_delete_user(self):
        with app.test_client() as client:
            response = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertNotIn('Test User', html)

# class PostTestCase(TestCase):
    
#     def setUp(self):
#         with app.app_context():
#             Post.query.delete()
#             User.query.delete()
#             Tag.query.delete()
#             db.session.commit()

#             user = User(first_name="Test", last_name="User", image_url="https://example.com/test.jpg")
#             db.session.add(user)
#             db.session.commit()

#             self.user_id = user.id

#             post = Post(title="Test Post", content="This is a test post.", user_id=user.id)
#             db.session.add(post)
#             db.session.commit()

#             self.post_id = post.id

#             tag = Tag(name="Test Tag")
#             db.session.add(tag)
#             db.session.commit()

#             post.tags.append(tag)
#             db.session.commit()

#     def tearDown(self):
#         with app.app_context():
#             db.session.rollback()

#     def test_add_post(self):
#         with app.test_client() as client:
#             response = client.post(f'/users/{self.user_id}/posts/new', data={
#                 'title': 'New Post',
#                 'content': 'This is a new post.'
#             }, follow_redirects=True)
#             html = response.get_data(as_text=True)

#             self.assertEqual(response.status_code, 200)
#             self.assertIn('New Post', html)

#     def test_show_post(self):
#         with app.test_client() as client:
#             response = client.get(f'/posts/{self.post_id}')
#             html = response.get_data(as_text=True)

#             self.assertEqual(response.status_code, 200)
#             self.assertIn('Test Post', html)

#     def test_edit_post(self):
#         with app.test_client() as client:
#             response = client.post(f'/posts/{self.post_id}/edit', data={
#                 'title': 'Updated Post',
#                 'content': 'This is an updated post.'
#             }, follow_redirects=True)
#             html = response.get_data(as_text=True)

#             self.assertEqual(response.status_code, 200)
#             self.assertIn('Updated Post', html)

#     def test_delete_post(self):
#         with app.test_client() as client:
#             response = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
#             html = response.get_data(as_text=True)

#             self.assertEqual(response.status_code, 200)
#             self.assertNotIn('Test Post', html)

    