"""User views tests."""

# run these tests like:
#
#    python -m unittest tests/test_views.py


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


class UserViewTestCase(TestCase):
    """Test views for Users."""

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

# TESTING HOME ROUTE WITH NO USER
    def test_home_route_no_user(self):
        """Testiing home route as not a user"""
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Welcome to KIKEN", html)

# TESTING HOME ROUTE WITH USER
    def test_home_route_with_user(self):
        """Testiing home route as a user"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.david_id
                
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Looks Empty... Let's starts by taking the Risk Profile Assessment", html)
    
# TESTING ABOUT ROUTES

    def test_about(self):
        """Testing about route"""
        with app.test_client() as client:
            res = client.get("/about")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Google will give you links of huge", html)

# TESTING METHODOLOGY ROUTE

    def test_methodology(self):
        """Testing methodology route"""
        with app.test_client() as client:
            res = client.get("/methodology")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("It's all about diversification", html)


# TESTING RISK ASSESSMENT ROUTE

    def test_risk_assessment(self):
        """Testing risk assessment route"""
        with app.test_client() as client:
            res = client.get("/risk-profile")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("What is your current age?", html)

# TESTING RISK ASSESSMENT UPDATE
    def test__risk_assessment_user(self):
        """Testiing Risk Assesment Update user"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.david_id
                
            res = client.get("/update/risk-profile")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("What is your total annual income?", html)


# TESTING RISK ASSESSMENT UPDATE POST
    def test__risk_assessment_user_post(self):
        """Testiing Risk Assesment Update user"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.david_id
            
            d = {
              "q1":"10","q2":"10","q3":"10","q4":"10","q5":"10","q6":"10","q7":"10","q8":"10","q9":"10","q10":"10",
            }
            res = client.post("/update/risk-profile", data=d, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("All Equity", html)


# TESTING HOME ROUTE with user and riskprofile
    def test__risk_assessment_user(self):
        """Testing Risk Assesment Update POST user"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_id
                
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Preservation", html)

# TESTING Update profile with user and riskprofile
    def test__update_profile_user(self):
        """Testing Risk Assesment Update POST user"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_id
                
            res = client.get("/update/profile")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Delete Profile", html)

# TESTING Update profile with user and riskprofile
    def test__update_profile_user_post(self):
        """Testing Risk Assesment Update POST user"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.david_id
            d= {"username": "rick", "password":"david1991"}
            res = client.post("/update/profile", data=d, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Updated Profile rick!", html)


# TESTING Deleting a Profile
    def test__delete_profile_user(self):
        """Testing Risk Assesment Delete User"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_id
                
            res = client.post("/update/delete", follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Signup", html)

# TESTING Deleting a Profile
    def test_login(self):
        """Testing login"""
        with app.test_client() as client:
            d={'username': 'david', 'password':'david1991'}
            res = client.post("/login", data=d,follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Hello, david!", html)

# TESTING Deleting a Profile
    def test__signout_user(self):
        """Testing Signing out user"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.david_id
                
            res = client.get("/logout", follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("You have been successfully logged out.", html)