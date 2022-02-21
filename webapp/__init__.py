from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'main.inloggen'
login_manager.login_message_category = 'warning'
login_manager.login_message = "Je moet ingelogd zijn om de pagina te bezoeken."

from webapp.bookings.views import bookings
from webapp.bungalows.views import bungalows
from webapp.main.views import main

app.register_blueprint(bookings)
app.register_blueprint(bungalows)
app.register_blueprint(main)