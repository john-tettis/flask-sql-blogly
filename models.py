from flask_sqlalchemy import SQLAlchemy
import datetime
"""Models for Blogly."""
default_profile = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQidyj5Yz_9BeIL5TDj0uzMJKlBDpsMaHa2Qg&usqp=CAU'

db = SQLAlchemy()

def connect_db(app):
    
    db.app = app
    db.init_app(app)
    

class User(db.Model):
    __tablename__='users'
    def __repr__(self):
        return f'<user id = {self.id}, name = "{self.first_name} {self.last_name}">'

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True)
    first_name = db.Column(db.String,
        nullable=False)
    last_name = db.Column(db.String,
        nullable=False)
    image_url = db.Column(db.String,
        nullable = False,
        default = default_profile)
    description = db.Column(db.String, default ='No description.')

    posts = db.relationship('Post', cascade='all, delete')

    def _full_name(self):
        return f'{self.first_name} {self.last_name}'
    full_name = property(_full_name)


class Post(db.Model):

    __tablename__ = 'posts'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
        )
    title = db.Column(
        db.Text,
        nullable=False
        )
    content = db.Column(
        db.Text, nullable=False
    )
    created_at = db.Column(db.Text, default=datetime.date.today().strftime("%B %d, %Y"))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User')
    
    # post_tags = db.relationship('PostTag',cascade='all, delete, delete-orphan')

class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text, unique=True)

    posts = db.relationship('Post', secondary='posts_tags', backref='tags', cascade='all,delete', passive_deletes=True)

class PostTag(db.Model):
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='cascade'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='cascade'), primary_key=True)

