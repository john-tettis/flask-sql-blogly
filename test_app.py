from app import app
from unittest import TestCase
from models import User, db


app.config['TESTING']= True
app.config['DEBUG_TB_HOSTS']=['dont-show-debug-toolbar']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class FlaskTests(TestCase):
    def setUp(self):
        User.query.delete()
        user = User(first_name = 'Ben', last_name = 'Burger', image_url = 'this is the image url')
        db.session.add(user)
        db.session.commit()
        self.id = user.id
    def tearDown(self):
        db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

    def test_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)
            self.assertIn('All Users', html)

    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.id}')
            html = resp.get_data(as_text=True)
            self.assertIn('Ben Burger', html)
            self.assertIn('No description',html)