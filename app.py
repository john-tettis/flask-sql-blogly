"""Blogly application."""

from flask import Flask, render_template, redirect, request,flash
from models import db, connect_db, User, Post, Tag, PostTag
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
import sys


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
    tags = Tag.query.all()
    return render_template('new_post.html',user = user, tags = tags)

@app.route('/users/<int:id>/posts/new', methods=['POST'])
def new_post_handle(id):
    """"Handles submission of a new post"""
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title = title, content = content, user_id = id)

    tags = request.form.getlist('tags')
    for tag in tags:
        new_post.tags.append(Tag.query.get(tag))
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/posts/{new_post.id}')

@app.route('/posts')
def display_all_posts():
    """Renders all posts to the page"""
    posts = Post.query.order_by(Post.created_at).all()
    return render_template('home.html', posts = posts)

@app.route('/posts/<int:id>')
def show_post(id):
    """Display post based on post id"""
    post = Post.query.get_or_404(id)
    return render_template('post.html',post=post)

@app.route('/posts/<int:id>/edit')
def edit_post(id):
    """Edit a post through html form"""
    post = Post.query.get_or_404(id)
    tags = Tag.query.all()
    return render_template('edit_post.html',post=post, tags=tags)

@app.route('/posts/<int:id>/edit', methods =['POST'])
def edit_post_handle(id):
    """Edit a post through html form"""
    post = Post.query.get(id)
    title = request.form.get('title')
    content = request.form.get('content')
    post.title = title
    post.content = content
    ids = request.form.getlist('tags')
    tags = [Tag.query.get(id) for id in ids]
    post.tags = tags
    
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:id>/delete')
def delete_post(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/')


@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags = tags)

@app.route('/tags/<int:id>')
def tag_details(id):
    tag = Tag.query.get_or_404(id)
    return render_template('tag_details.html',tag = tag)

@app.route('/tags/new')
def new_tag():
    """Renders a form for a new tag to be created"""

    return render_template('new_tag.html')

@app.route('/tags/new', methods = ['POST'])
def new_tag_handle():
    tag_name = request.form.get('tag-name')
    tag = Tag(name = tag_name)
    try:
        db.session.add(tag)
        db.session.commit()
    except:
        db.session.rollback()
    return redirect('/tags')

@app.route('/tags/<int:id>/edit')
def edit_tag(id):
    """Displays a form to allow a user to edit a tag"""
    tag = Tag.query.get_or_404(id)
    return render_template('edit_tag.html', tag = tag)

@app.route('/tags/<int:id>/edit', methods = ['POST'])
def edit_tag_handle(id):
    """Displays a form to allow a user to edit a tag"""
    tag = Tag.query.get_or_404(id)
    tag_name = request.form.get('tag-name')
    tag.name = tag_name
    try:
        db.session.add(tag)
        db.session.commit()
    except:
        db.session.rollback()
    return redirect('/tags')

@app.route('/tags/<int:id>/delete')
def delete_tag(id):
    delete = db.session.query(Tag).filter(Tag.id==id).one()
    db.session.delete(delete)
    # Tag.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/tags')

