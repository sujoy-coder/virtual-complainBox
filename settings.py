from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os


app = Flask(__name__, static_url_path="/User/static")

if "SECRET_KEY" in os.environ:
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
else:
    app.config['SECRET_KEY'] = '768b58310b8ba53756af1b223d803bf5he787effr78gg8g8tf8dsf5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

if "DATABASE_URI" in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))
    fullName = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    roll = db.Column(db.String(20),nullable=False)
    semester = db.Column(db.Integer,nullable=False)
    department = db.Column(db.String(50),nullable=False)
    year = db.Column(db.String(20),nullable=False)
    addressTo = db.Column(db.String(100), nullable=False)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    isViewed = db.Column(db.String, default='False', nullable=False)
    date = db.Column(db.String, default=str(date.today()), nullable=False)


class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adminUser = db.Column(db.String(100), nullable=False)
    adminEmail = db.Column(db.String(120), nullable=False)
    adminPassword = db.Column(db.Text,nullable=False)


from Admin import admin
from User import user


app.register_blueprint(user, url_prefix="/")
app.register_blueprint(admin, url_prefix="/admin")


@app.route('/')
def index():
    return '<h1> Server is under maintenance. We will be come back soon :( </h1>'

