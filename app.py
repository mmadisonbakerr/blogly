"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

# db.create_all()

# with app.app_context():
#     db.create_all()

"""Home page."""
@app.route('/')
def home():
    return render_template('home.html')

"""Shows all users"""
@app.route('/all-users')
def list_users():
    users = User.query.all()
    posts = Post.query.all()
    return render_template('list.html', users=users, posts=posts)

"""Create a new user."""
@app.route('/new-user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        print("Form data received:", request.form)
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        image_url = request.form.get('image_url') or None

        if not first_name or not last_name:
            return "First name and last name are required!", 400

        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        return redirect(f'/{new_user.id}')
    return render_template('add-user.html')

"""Show user profile."""
@app.route('/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user-details.html", user=user)

"""Edit user."""
@app.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.image_url = request.form.get('image_url') or None

        db.session.commit()

        return redirect(f'/{user_id}')
    
    if request.method == 'GET': 
        return render_template('edit-user.html', user=user)

"""Delete  user."""
@app.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    Post.query.filter_by(user_id=user_id).delete()

    db.session.delete(user)
    db.session.commit()
    return redirect('/all-users')

"""Add new post for user."""
@app.route('/<int:user_id>/add-post', methods=['GET', 'POST'])
def add_post(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            return "Title and content are required!", 400

        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        return redirect(f'/{user_id}')

    return render_template('add-post.html', user=user)

"""Show  specific post."""
@app.route('/<int:user_id>/<int:post_id>')
def show_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    return render_template('post-details.html', user=user, post=post)

"""Edit post."""
@app.route('/<int:user_id>/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(user_id, post_id):

    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')

        db.session.commit()

        return redirect(f'/{user_id}/{post_id}')

    return render_template('edit-post.html', user=user, post=post)

"""Delete post."""
@app.route('/<int:user_id>/<int:post_id>/delete', methods=['POST'])
def delete_post(user_id, post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/{user_id}')