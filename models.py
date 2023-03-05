from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User table"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), unique=True, nullable=False)

    password = db.Column(db.String(60), nullable=False)

    favs = db.relationship('Favs', backref='user')

    drinks = db.relationship('Drinks')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"
    
    def does_fav(self, drink_fav):
        """Is this user following `other_use`?"""

        found_user_list = [user for user in self.drinks if user == drink_fav]
        return len(found_user_list) == 1

    @classmethod
    def signup(cls, username, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
        username=username,
        password=hashed_pwd)

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

class Favs(db.Model):
    """Fav drint table"""

    __tablename__ = "favs"

    fav_id = db.Column(db.Integer,primary_key=True)

    user_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete='cascade'))

    drink_id = db.Column(db.Integer,db.ForeignKey('drinks.drink_id', ondelete='cascade'))

class Drinks(db.Model):
    """Drinks table"""

    __tablename__ = "drinks"

    drink_id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,)

    drink_name = db.Column(db.String, nullable=False, unique=True)

    recipe = db.Column(db.String, nullable=False, unique=True)

    ingredient1 = db.Column(db.String, nullable=False, unique=True)

    ingredient2 = db.Column(db.String, nullable=False, unique=True)

    ingredient3 = db.Column(db.String, nullable=False, unique=True)

    ingredient4 = db.Column(db.String, nullable=False, unique=True)

    ingredient5 = db.Column(db.String, nullable=False, unique=True)

    ingredient6 = db.Column(db.String, nullable=False, unique=True)

    ingredient7 = db.Column(db.String, nullable=False, unique=True)       
    
    ingredient8 = db.Column(db.String, nullable=False, unique=True)

    ingredient9 = db.Column(db.String, nullable=False, unique=True)

    ingredient10 = db.Column(db.String, nullable=False, unique=True)

    ingredient11 = db.Column(db.String, nullable=False, unique=True)

    ingredient12 = db.Column(db.String, nullable=False, unique=True)

    ingredient13 = db.Column(db.String, nullable=False, unique=True)

    ingredient14 = db.Column(db.String, nullable=False, unique=True)

    ingredient15 = db.Column(db.String, nullable=False, unique=True)

    user = db.relationship('User')