import os
from flask import (Flask)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
login = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a]Ida.9Xp,2"_[pb?1{;>1MnqA<Cyk'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False    

app.config.from_object(Config)
