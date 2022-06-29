import bcrypt
from flask import Flask
import secrets
from flask_bcrypt import Bcrypt


app = Flask(__name__)
secret = 'jafnjfsandkjfnasdfkjld1235fa1sd5f1asd3f21561312'
app.secret_key = secret
app.config['SESSION_COOKIE_NAME'] = "my_session"
bcrypt = Bcrypt(app)

from routes import *