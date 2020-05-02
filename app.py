import os
from flask import Flask, request, render_template, redirect, flash, jsonify, session, g,url_for
import requests
from flask_restful import reqparse, abort, Api, Resource
from api import models, Models, SingleModel
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from functools import wraps
from bs4 import BeautifulSoup
from forms import UserAddForm, UserEditForm, LoginForm, EditPasswordForm, RiskProfile
from models import db, connect_db, User, Portfolios, ETFs
 

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
api = Api(app)




app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///kiken'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'isaacneterothe12thchairman')
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)
 

connect_db(app)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash("Access unauthorized.", "danger")
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get_or_404(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage:
    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    if g.user:
        
        return render_template('home.html')

    else:
        return render_template('home-anon.html')

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

# Signup and Login page =====================

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                first_name = form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)
        do_login(user)
        flash(f"Welcome {user.username}!", "success")
        return redirect("/")
    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')
    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash('You have been successfully logged out.', 'info')
    return redirect("/login")


# Risk Profile==========================
@app.route('/risk-profile', methods=["GET", "POST"])
def new_risk_profile():
    if g.user:
        flash("You have to logout to access this page", "warning")
        return redirect('/')
    form = RiskProfile()
    login_form = LoginForm()

    if form.validate_on_submit():
        q1 = form.q1.data
        q2 = form.q2.data
        q3 = form.q3.data
        q4 = form.q4.data
        q5 = form.q5.data
        q6= form.q6.data
        q7= form.q7.data
        q8 = form.q8.data
        q9 = form.q9.data
        q10 = form.q10.data

        answers = [int(q1), int(q2), int(q3), int(q4), int(q5), int(q6), int(q7), int(q8), int(q9), int(q10)]
        Sum = sum(answers)
        if Sum <= 20:
            risk_profile = "Preservation"
        elif Sum > 20 and Sum <= 40:
            risk_profile = "Conservative"
        elif Sum > 40 and Sum <= 60:
            risk_profile = "Balanced"
        elif Sum > 60 and Sum <= 80:
            risk_profile = "Aggressive"
        else:
            risk_profile = "All Equity"
        
        return render_template('/results.html', risk_profile=risk_profile, form=login_form )
    else:
        return render_template("risk-form.html", form=form)

# Updating a risk profile
@app.route('/update/risk-profile', methods=["GET", "POST"])
@login_required
def update_riskprofile():
    id = g.user.id
    user = User.query.get_or_404(id)
    form = RiskProfile(obj=user)

    if form.validate_on_submit():
        q1 = form.q1.data
        q2 = form.q2.data
        q3 = form.q3.data
        q4 = form.q4.data
        q5 = form.q5.data
        q6= form.q6.data
        q7= form.q7.data
        q8 = form.q8.data
        q9 = form.q9.data
        q10 = form.q10.data

        answers = [int(q1), int(q2), int(q3), int(q4), int(q5), int(q6), int(q7), int(q8), int(q9), int(q10)]
        Sum = sum(answers)
        if Sum <= 20:
            risk_profile = "Preservation"
        elif Sum > 20 and Sum <= 40:
            risk_profile = "Conservative"
        elif Sum > 40 and Sum <= 60:
            risk_profile = "Balanced"
        elif Sum > 60 and Sum <= 80:
            risk_profile = "Aggressive"
        else:
            risk_profile = "All Equity"
        user.risk_profile = risk_profile
        db.session.commit()
        flash("Update Successful", "success")
        return redirect('/')
    else:
        return render_template('update-risk-form.html', form=form)

# Update Profile

@app.route('/update/profile', methods=["GET", "POST"])
@login_required
def update_profile():
    id = g.user.id
    user = User.query.get_or_404(id)
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data
            db.session.commit()
            flash(f"Updated Profile {user.username}!", "success")
            return redirect('/')
        flash("Invalid password, please try again.", 'danger')
    return render_template('update-user-form.html', form = form, user = user)

# Update Password

@app.route('/update/password', methods=["GET", "POST"])
@login_required
def update_password():

    form = EditPasswordForm(obj=g.user)

    if form.validate_on_submit():
        user = User.change_password(g.user.username,
                                 form.old_password.data,
                                 form.new_password.data,
                                 form.confirm.data)
        if not user:
            flash('Incorrect Password', 'danger')
            return redirect('/')
        try:
            db.session.commit()
            flash('Password successfully changed', 'success')
            return redirect("/")
        except (InvalidRequestError, IntegrityError):
            db.session.rollback()
            flash("Something went wrong. Session rolled back.", 'danger')

    return render_template('update-password-form.html', form=form, user_id=g.user.id)


# Delete Profile
@app.route('/update/delete', methods=["POST"])
@login_required
def delete_user():
    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")
# About Route
@app.route('/about')
def show_about():
    return render_template('about.html')

# Methodology Route
@app.route('/methodology')
def show_methodology():
    return render_template('methodology.html')
##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34076804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req


# API GET Route
@app.route("/api/portfolios")
def list_portfolios():
    """ All portfolios"""

    portfolios = [portfolio.to_dict() for portfolio in Portfolios.query.all()]
    return jsonify(portfolios=portfolios)

@app.route("/api/portfolios/<name>")
def get_portfolio(name):
    """ get one portfolios"""

    portfolio = Portfolios.query.filter_by(name=name).first_or_404()
    return jsonify(portfolio=portfolio.to_dict())

# API GET Route
@app.route("/api/etfs")
def list_etfs():
    """ All etfs"""

    all_etfs = [etf.to_dict() for etf in ETFs.query.all()]
    return jsonify(etfs=all_etfs)
    


@app.route('/api/etfs/<symbol>')
def get_etf(symbol):
    etf = ETFs.query.filter_by(symbol=symbol).first_or_404()
    return jsonify(etf=etf.to_dict())


parser = reqparse.RequestParser()
parser.add_argument('name')

## Actually setup the Api resource routing here
##

# Portfolio APIs



api.add_resource(Models, '/api/models')
api.add_resource(SingleModel, '/api/models/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)