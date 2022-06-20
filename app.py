from flask import Flask
import secrets

app = Flask(__name__)

secret = secrets.token_urlsafe(32)

app.secret_key = secret

from routes import *