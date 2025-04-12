from models import User, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

user1 = User(first_name="Test", last_name="User", image_url="https://example.com/test.jpg")
user2 = User(first_name="Another", last_name="User", image_url="https://example.com/another.jpg")
user3 = User(first_name="Sample", last_name="User", image_url="https://example.com/sample.jpg")

db.session.add_all([user1, user2, user3])

db.session.commit()

