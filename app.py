"""Blogly application."""

from flask import Flask, render_template, redirect, request,flash
from models import db, connect_db, User, Post
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']= 'thisisnotasecret'

app.debug = False
toolbar = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def display_home_page():
    """Displays most recent posts"""
    posts = Post.query.order_by(Post.id.desc()).limit(5).all()
    return render_template("home.html",posts=posts)

@app.route('/users')
def display_users():
    """Displays all users in database"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users = users)

@app.route('/users/<int:id>')
def user_information(id):
    """Displays an individual user information"""
    user = User.query.get(id)
    return render_template('details.html',user = user)

@app.route('/users/new')
def user_form():
    """Displays a form for a new user to be created"""
    return render_template('user_form.html')

@app.route('/users/new', methods = ['POST'])
def new_user_handle():
    """Handles new user information"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    description = request.form['description']
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url if image_url else None, description = description if description else None)

    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:id>/edit')
def edit_user(id):
    """Takes user to a form to edit their info"""
    user = User.query.get(id)
    return render_template('edit_user.html', user = user)

@app.route('/users/<int:id>/edit', methods = ['POST'])
def edit_user_handle(id):
    """Handles submission of a user-edit form"""
    user = User.query.get(id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    user.description = request.form['description']
    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/{user.id}')

@app.route('/users/<int:id>/delete')
def delete_user(id):
    """Deletes user based on id given in url"""
    User.query.filter_by(id = id).delete()
    db.session.commit()
    return redirect('/users')



@app.route('/users/<int:id>/posts/new')
def new_post(id):
    """"Displays a form for a user to create a new post"""
    user = User.query.get_or_404(id)
    return render_template('new_post.html',user = user)

@app.route('/users/<int:id>/posts/new', methods=['POST'])
def new_post_handle(id):
    """"Handles submission of a new post"""
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title = title, content = content, user_id = id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/posts/{new_post.id}')

@app.route('/posts/<int:id>')
def show_post(id):
    """Display post based on post id"""
    post = Post.query.get_or_404(id)
    return render_template('post.html',post=post)

@app.route('/posts/<int:id>/edit')
def edit_post(id):
    """Edit a post through html form"""
    post = Post.query.get_or_404(id)
    return render_template('edit_post.html',post=post)

@app.route('/posts/<int:id>/edit', methods =['POST'])
def edit_post_handle(id):
    """Edit a post through html form"""
    post = Post.query.get(id)
    title = request.form.get('title')
    content = request.form.get('content')
    post.title = title
    post.content = Content
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:id>/delete')
def delete_post(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/')
