from models import User, Post, db
from app import app

with app.app_context(): db.drop_all()
with app.app_context(): db.create_all()

user1 = User(first_name="Edward", last_name="Cullen", image_url="https://example.com/test.jpg")
user2 = User(first_name="Bella", last_name="Swan", image_url="https://example.com/another.jpg")
user3 = User(first_name="Jacob", last_name="Black", image_url="https://example.com/sample.jpg")

post1 = Post(title="I'm Shiny", content="This is the skin of a killer Bella.", user_id=user1.id)
post2 = Post(title="The Lion and the Lamb", content="What a stupid lamb.", user_id=user2.id)
post3 = Post(title="Woof", content="What A Marshmallow.", user_id=user3.id)

with app.app_context(): db.session.add(user1)
with app.app_context(): db.session.add(user2)
with app.app_context(): db.session.add(user3)
with app.app_context(): db.session.add(post1)
with app.app_context(): db.session.add(post2)
with app.app_context(): db.session.add(post3)

with app.app_context(): db.session.commit()

