from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
 
db = SQLAlchemy()
bcrypt = Bcrypt()
 
def connect_db(app):
    db.app = app
    db.init_app(app)
 

# MODELS GO BELOW!

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_url = db.Column(
        db.Text,
        default="/static/img/default-pic.png",
    )


    risk_profile = db.Column(db.Text)

    password = db.Column(
        db.Text,
        nullable=False,
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"


    def serialize(self):
        return {"id":self.id,
        "first_name":self.first_name,
        "last_name":self.last_name,  
        "username":self.username, 
        "email":self.email, 
        "image_url": self.image_url,
        "header_image_url": self.header_image_url,
        "risk_profile": self.risk_profile}

    @classmethod
    def signup(cls, first_name, last_name, username, email, password, image_url):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    @classmethod
    def change_password(cls, username, old_password, new_password, new_password_confirm):
        """Change user's password from old_password to new_password.
        Checks if original user credentials match and that new password matches
        the password confirmation. If successful, adds changed password to the
        system and returns user object.
        If matching user is not found, password is wrong or new password is 
        incorrectly confirmed, returns False.
        """
        if not new_password == new_password_confirm:
            return False
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, old_password)
            if is_auth:
                hashed_pwd = bcrypt.generate_password_hash(new_password).decode('UTF-8')
                user.password = hashed_pwd
                db.session.add(user)
                return user

        return False

class Portfolios(db.Model):
    """Porfolio Model"""

    __tablename__ = 'portfolios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text,nullable=False, unique=True)
    ITOT = db.Column(db.Integer, default=0)
    VEA = db.Column(db.Integer, default=0)
    VNQ = db.Column(db.Integer, default=0)
    GLD = db.Column(db.Integer, default=0)
    AGG = db.Column(db.Integer, default=0)
    BIL = db.Column(db.Integer, default=0)
    fees = db.Column(db.Float, default=0)
    desc = db.Column(db.Text, nullable=False)


    def to_dict(self):
        """Serialize."""

        return {
            "id": self.id,
            "name": self.name,
            "ITOT": self.ITOT,
            "VEA": self.VEA,
            "VNQ": self.VNQ,
            "GLD": self.GLD,
            "AGG": self.AGG,
            "BIL": self.BIL,
            "fees": self.fees,
            "desc": self.desc
        }


class ETFs(db.Model):
    """Etfs Model"""

    __tablename__ = 'etfs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.Text,nullable=False, unique=True)
    name = db.Column(db.Text, default=0)
    category = db.Column(db.Text, default=0)
    expense_ratio = db.Column(db.Float, default=0)
    


    def to_dict(self):
        """Serialize."""

        return {
            "id": self.id,
            "symbol": self.symbol,
            "name": self.name,
            "category": self.category,
            "expense_ratio": self.expense_ratio
        }

