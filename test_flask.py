from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    """Test User model."""

    def setUp(self):
        print("Setting up test case...")
        User.query.delete()

        user = User(first_name="Test", last_name="User", image_url="https://example.com/test.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        db.session.rollback()

    def test_list_users(self):
        print("Testing list users...")
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            print("Response HTML:", html)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Test User', html)

    def test_create_user(self):
        with app.test_client() as client:
            response = client.post('/new-user', data={
                'first_name': 'New',
                'last_name': 'User',
                'image_url': 'https://example.com/new.jpg'
            }, folllow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('New User', html)

    def test_show_user(self):
        with app.test_client() as client:
            response = client.get(f'/{self.user_id}')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Test User', html)

    def test_delete_user(self):
        with app.test_client() as client:
            response = client.post(f'/delete/{self.user_id}', follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertNotIn('Test User', html)

