import bcrypt
from flask import Flask
import secrets
from flask_bcrypt import Bcrypt


app = Flask(__name__)
secret = secrets.token_urlsafe(32)
app.secret_key = secret
app.config['SESSION_COOKIE_NAME'] = "my_session"
bcrypt = Bcrypt(app)

from routes import *