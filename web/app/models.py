from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    ratings=db.relationship('Rating', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

class Movie(db.Model):
    __tablename__='movies'

    id = db.Column(db.Integer, primary_key=True)
    moviename = db.Column(db.String(64), unique=True, index=True)
    movie_genres = db.Column(db.String(64))
    ratings = db.relationship('Rating', backref='movie', lazy='dynamic')

    def __repr__(self):
        return '<Movie %r>' % self.moviename

class Rating(db.Model):
    __tablename__='ratings'
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    rating = db.Column(db.Integer)

    def __repr__(self):
        return '<Rating %r>' % self.rating

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
