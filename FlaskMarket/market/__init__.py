from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

# this thing is to encrypt the password,means helps in generating hash_passwords
from flask_bcrypt import Bcrypt

from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///market.db'
app.config["SECRET_KEY"]="5a49527ccb0f5a62af57c729"
# Cookies are small pieces of text sent to your browser by a website you visit. 
# They help that website remember information about your visit, which can both make 
# it easier to visit the site again and make the site more useful to you.
# What does app SECRET_KEY do?
# Each Flask web application contains a secret key which used to sign session cookies 
# for protection against cookie data tampering

# started an instance of LoginManager by passing the application as the argument
login_manager=LoginManager(app)
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)


# if the user is not authenticated then the control will come here ,so we should specify our 
# login_manager where is our login route actually located
login_manager.login_view="login_page"
# this will redirect our user to login page

login_manager.login_message_category ="info"
# this will be responsible for flashing the message "Please login to access this page"

from market import routes
# from market import models

