"""Blogly application."""

from flask import Flask, render_template, redirect, request,flash
from models import db, connect_db, User
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
    """Redirects to users"""
    return redirect('/users')

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
    user = User.query.get(id)
    return render_template('edit_user.html', user = user)

@app.route('/users/<int:id>/edit', methods = ['POST'])
def edit_user_handle(id):
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
    User.query.filter_by(id = id).delete()
    db.session.commit()
    return redirect('/users')
