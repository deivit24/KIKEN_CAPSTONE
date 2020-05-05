from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField
import email_validator
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo

# FORM CLASSES GO BELOW!

class UserAddForm(FlaskForm):
    """Form for adding users."""

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')

class UserAddFormRisk(FlaskForm):
    """Form for adding users."""

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')  
    risk_profile = StringField('Risk Profile')  

class UserEditForm(FlaskForm):
    """Form for adding users."""

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')

class EditPasswordForm(FlaskForm):
    """Form for changing existing user's password."""

    old_password = PasswordField('Current Password', validators=[Length(min=6)])
    new_password = PasswordField('New Password', validators=[Length(min=6), EqualTo('confirm', 'New passwords much match!')])
    confirm = PasswordField('Confirm New Password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class RiskProfile(FlaskForm):
    
    q1 = RadioField("1. What is your current age?", 
    choices = [
      ('0', 'More than 60'),
      ('2', 'Between 51 and 60'), 
      ('5', 'Between 41 and 50'), 
      ('8', 'Between 31 and 40'), 
      ('10', '30 or younger')])
    q2 = RadioField("2. Please estimate when you will need to withdraw 20% of your current portfolio value, such as a need for a house down payment or some other major financial need?", choices = [
      ('0', 'Within the next year'), 
      ('2', '2 - 5 years from now'), 
      ('5', '5 - 10 years from now'), 
      ('8', '10 - 20 years from now'), 
      ('10', 'More than 20 years from now')])
    q3 = RadioField("3. If you were to lose your job today, how long will you be able to maintain your current spending life style before you run out of money in your Savings and Checking account?", 
    choices = [
      ('0', '1 week'), 
      ('2', '1 month'), 
      ('5', '3 months'), 
      ('8', '6 months or more'), 
      ('10', 'I am retired')])
    q4 = RadioField("4. What is your total annual income? ( Work, Pension, Social Security, etc.)", choices = [
      ('0', 'Less than $50,000'), 
      ('2', '$50,000 - $100,000'), 
      ('5', '$100,000 - $150,000'), 
      ('8', '$150,000 - $250,000'), 
      ('10', 'More than $250,000')])
    q5 = RadioField("5. Please rate the stability of your income.", 
    choices = [
      ('0', 'Very low'), 
      ('2', 'Below average'), 
      ('5', 'Average'), 
      ('8', 'Above Average'), 
      ('10', 'Very High')])
    q6 = RadioField("6. If you unexpectedly received $20,000 to invest today, what would you do?", 
    choices = [
      ('0', 'Deposit it in bank account, money market account or an insured cd'), 
      ('2', 'Invest only in safe quality bonds or bond funds'), 
      ('5', 'Invest in a proper mix of bonds and stocks'), 
      ('8', 'Invest only in stocks or stock funds'), 
      ('10', 'Buy $20,000 worth of lottery tickets')])
    q7 = RadioField("7. When you think of the word “risk” in a financial context, which of the following words come to mind?", 
    choices = [
      ('0', 'Absolute loss'), 
      ('2', 'Danger'), 
      ('5', 'Uncertainty'), 
      ('8', 'Opportunity'), 
      ('10', 'Thrill')])
    q8 = RadioField("8. Which of these statements would best describe your attitudes about the next three years performance of this investment?", 
    choices = [
      ('0', 'I need to see at least a little return'), 
      ('2', "I'd have a hard time tolerating any losses"), 
      ('5', 'I can tolerate a small loss'), 
      ('8', 'I can tolerate a loss'), 
      ('10', "I don't mind a loss")])   
    q8 = RadioField("8. Which of these statements would best describe your attitudes about the next three years performance of this investment?", 
    choices = [
      ('0', 'I need to see at least a little return'), 
      ('2', "I'd have a hard time tolerating any losses"), 
      ('5', 'I can tolerate a small loss'), 
      ('8', 'I can tolerate a loss'), 
      ('10', "I don't mind a loss")])
    q9 = RadioField("9. Throughout the 17-month bear during the 2008 Mortgage Crisis, the S&P 500 lost 50% of its value. Which of the following would you have done if your portfolio experiences a 50% loss?", 
    choices = [
      ('0', 'Sell all of your remaining investments and remain in cash'), 
      ('2', "Move all of your investments into bonds and CDs"), 
      ('5', 'Change to a more conservative allocation'), 
      ('8', 'Hold on to your investments'), 
      ('10', "Invest more")]) 
    q10 = RadioField("10. How emotionally comfortable are you with volatility?", 
    choices = [
      ('0', 'Plan A'), 
      ('2', "Plan B"), 
      ('5', 'Plan C'), 
      ('8', 'Plan D'), 
      ('10', "Plan E")])