from models import User, Post, Tag, PostTag, db
from app import app

with app.app_context(): 
    db.drop_all()
    db.create_all()

    user1 = User(first_name="Edward", last_name="Cullen", image_url="https://example.com/test.jpg")
    user2 = User(first_name="Bella", last_name="Swan", image_url="https://example.com/another.jpg")
    user3 = User(first_name="Jacob", last_name="Black", image_url="https://example.com/sample.jpg")

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    post1 = Post(title="I'm Shiny", content="This is the skin of a killer Bella.", user_id=user1.id)
    post2 = Post(title="The Lion and the Lamb", content="What a stupid lamb.", user_id=user2.id)
    post3 = Post(title="Woof", content="What A Marshmallow.", user_id=user3.id)

    db.session.add_all([post1, post2, post3])
    db.session.commit()

    tag1 = Tag(name="Vampire")
    tag2 = Tag(name="Werewolf")
    tag3 = Tag(name="Love")
    
    db.session.add_all([tag1, tag2, tag3])
    db.session.commit()

    pt1 = PostTag(post_id=post1.id, tag_id=tag1.id) 
    pt2 = PostTag(post_id=post2.id, tag_id=tag3.id)
    pt3 = PostTag(post_id=post3.id, tag_id=tag2.id)
    
    db.session.add_all([pt1, pt2, pt3])
    db.session.commit()


