from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User in the system."""
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50), 
                           nullable=False)
    last_name = db.Column(db.String(50), 
                          nullable=False)
    image_url = db.Column(db.Text, 
                          default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png')
    # posts = db.relationship('Post',
    #                         backref='user', 
    #                         cascade='all, delete-orphan')

class Post(db.Model):
    """Post in the system."""
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100), 
                      nullable=False)
    content = db.Column(db.String(500), 
                        nullable=False)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'), 
                        nullable=False)
    created_at = db.Column(db.DateTime, 
                           default=db.func.current_timestamp())

    tags = db.relationship('Tag', 
                           secondary='post_tags',
                           backref='posts',)
    user = db.relationship('User',
                           backref='posts')

class Tag(db.Model): 
    """Tag in the system."""
    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(50), 
                     nullable=False, 
                     unique=True)
    # posts = db.relationship('Post', 
    #                         secondary='post_tags', 
    #                         backref='tags')

class PostTag(db.Model):
    """Mapping of posts to tags."""
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, 
                        db.ForeignKey('posts.id'), 
                        primary_key=True)
    tag_id = db.Column(db.Integer, 
                       db.ForeignKey('tags.id'), 
                       primary_key=True)  
    
    

# def post_tags():
#     db.session.query(Tag.name, Post.title).outerjoin(Post).all()


# post_tags = db.Table(
#     'post_tags',
#     db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
#     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
# )
