"""Models views tests."""

# run these tests like:
#
#    python -m unittest tests/test_models.py


import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Portfolios, ETFs
from forms import LoginForm, RiskProfile

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///kiken-test"


# Now we can import app

from app import app, CURR_USER_KEY

app.config['SQLALCHEMY_ECHO'] = False
# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True
# Don't req CSRF for testing
app.config['WTF_CSRF_ENABLED'] = False

db.create_all()

GENERIC_IMAGE = "https://mylostpetalert.com/wp-content/themes/mlpa-child/images/nophoto.gif"


class UserModelTestCase(TestCase):
    """Test views for Models."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        david = User.signup("david.salazar","salazar", "david", "test@test1.com", "david1991", GENERIC_IMAGE)

        jorge = User.signup("jorge","salazar", "jorge", "test@test2.com", "david1991", GENERIC_IMAGE)

        test=User(first_name="test", last_name="test", username="test", email="test@test.com", password="david1991", risk_profile="Preservation")

        db.session.add(test)
        db.session.add(david)
        db.session.add(jorge)
        db.session.commit()

        self.test_id = test.id 
        self.david_id = david.id 
        self.jorge_id = jorge.id

    def tearDown(self):
        db.session.rollback()
    

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            first_name="rick",
            last_name="sanchez",
            email="risksanchez@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(u.risk_profile, None)
    
    def test_repr(self):

        u_test = User.query.get(self.david_id)
        u_test2 = User.query.get(self.jorge_id)
        self.assertIsNotNone(u_test)
        self.assertIsNotNone(u_test2)
        self.assertEqual(u_test, u_test)

    def test_valid_signup(self):
        u_test = User.signup("Rick","Sanchez", "Rick", "ricksanchez@test2.com", "david1991", GENERIC_IMAGE)

        db.session.add(u_test)
        db.session.commit()

        u_test = User.query.get(4)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "Rick")
        self.assertEqual(u_test.email, "ricksanchez@test2.com")
        self.assertNotEqual(u_test.password, "david1991")
        self.assertTrue(u_test.password.startswith("$"))

    def test_error_signup(self):
        with app.test_client() as client:
            d = {
              "first_name":"adfasf",
              "last_name": "asdfasf",
              "username":"test", "email": "testusertestcom", "password": "HASHED_PASSWORD", "image_url": GENERIC_IMAGE}

            resp = client.post("/signup", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Invalid email address.', html)

    def test_invalid_username_signup(self):
        invalid = User.signup("Rick","Sanchez",None, "test@test.com", "password", GENERIC_IMAGE)
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
          db.session.commit()

    # AUTH TEST

    def test_valid_auth(self):
        u = User.authenticate("david", "david1991")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.david_id)

    def test_invalid_username(self):
        self.assertFalse(User.authenticate("notreal", "password"))

    def test_invalid_password(self):
        self.assertFalse(User.authenticate("david", "wrongpassword"))