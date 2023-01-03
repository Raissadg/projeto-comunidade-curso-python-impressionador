from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b797d60107000f6814325b860cf12baa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

bcrypt = Bcrypt(app)

database = SQLAlchemy(app)
database.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from comunidadeimpressionadora import routes