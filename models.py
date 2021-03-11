from flask_sqlalchemy import SQLAlchemy
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

    def _full_name(self):
        return f'{self.first_name} {self.last_name}'
    full_name = property(_full_name)