from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from oauthlib.oauth2 import WebApplicationClient

app = Flask(__name__)
try:
    app.config.from_object('config.Config')
except:
    pass

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

loginmanager = LoginManager(app)
loginmanager.login_view = 'home'
loginmanager.login_message_category = 'info'

client = WebApplicationClient(app.config["GOOGLE_CLIENT_ID"])

with app.app_context():
    from flaskr.authentication import auth
    from flaskr.errors.handlers import errors

    app.register_blueprint(auth.bp)
    app.register_blueprint(errors)

    from flaskr.route import *

    from flaskr.dashboard_dash.dashboard import create_dashboard

    app = create_dashboard(app)
