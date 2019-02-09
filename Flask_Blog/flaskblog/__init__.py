from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
# from flaskblog.models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a0cbd62460b7d49eb7d8519503f0b4d6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # view we pass in is the function name of the route
login_manager.login_message_category = 'info' # To Highlight the msg
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
# user = User.query.filter_by(username = 'nitssats').first()
# print("user.username = "+user.username)
# print("user.password = "+user.password)

# app.config['MAIL_USERNAME'] = user.username
# app.config['MAIL_PASSWORD'] = user.password
mail = Mail(app)

from flaskblog import routes