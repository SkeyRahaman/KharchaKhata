from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from oauthlib.oauth2 import WebApplicationClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
try:
    app.config.from_object('config_local.Config')
except Exception as e:
    print("we are configuring the Server side configaration.",e)
    app.config.from_object('config.Config')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

loginmanager = LoginManager(app)
loginmanager.login_view = 'home'
loginmanager.login_message_category = 'info'

client = WebApplicationClient(app.config["GOOGLE_CLIENT_ID"])

with app.app_context():
    from flaskr.authentication import auth
    from flaskr.errors.handlers import errors
    from flaskr.api import api_authentication, api_route
    from flaskr.android import android_routes

    app.register_blueprint(auth.bp)
    app.register_blueprint(errors)
    app.register_blueprint(api_route.bp)
    app.register_blueprint(api_authentication.bp)
    app.register_blueprint(android_routes.bp)

    from flaskr.route import *

    from flaskr.dashboard_dash.dashboard import create_dashboard

    app = create_dashboard(app)



