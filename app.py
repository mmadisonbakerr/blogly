"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

# db.create_all()

# with app.app_context():
#     db.create_all()

@app.route('/')
def list_users():
    users = User.query.all()
    return render_template('list.html', users=users)

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

@app.route('/<int:user_id>')
def show_user(user_id):
    """Show user profile."""
    user = User.query.get_or_404(user_id)
    return render_template("user-details.html", user=user)

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

@app.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Delete a user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')




