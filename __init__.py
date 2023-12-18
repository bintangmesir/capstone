import os
from flask import Flask, request, flash, send_from_directory
from flask_login import LoginManager
from datetime import datetime
from .model.db import db
from functools import wraps
from flask_bcrypt import Bcrypt

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

bcrypt = Bcrypt(app)

login = LoginManager()
login.init_app(app)
login.login_view = 'login'


users = db['users']
roles = db['roles']


@login.user_loader
def load_user(username):
    u = users.find_one({"username": username})
    if not u:
        return None
    return User(username=u['username'], role=u['role'], id=u['_id'])


class User:
    def __init__(self, id, username, role):
        self._id = id
        self.username = username
        self.role = role

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)


def roles_required(*role_names):
    def decorator(original_route):
        @wraps(original_route)
        def decorated_route(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('home'))
            if not current_user.role in role_names:
                return redirect(url_for('home'))
            else:
                return original_route(*args, **kwargs)
        return decorated_route
    return decorator


from .controller.client.home import *
from .controller.client.aktivitas import *
from .controller.client.aktivitasku import *
from .controller.client.tentang import *
from .controller.client.artikel import *
from .controller.client.donatur import *
from .controller.auth.auth import *
from .controller.server.dashboard import *
from .controller.server.data_user import *
from .controller.server.data_aktivitas import *
from .controller.server.data_aktivitasku import *
from .controller.server.data_donatur import *
from .controller.server.data_artikel import *


@app.template_filter(name='linebreaksbr')
def linebreaksbr_filter(text):
    return text.replace('\n', '<br>')


@app.template_filter(name='date')
def date(d):
    d = datetime.strptime(str(d), '%Y-%m-%d %H:%M:%S.%f').date()
    d.strftime("%d-%m-%y")
    return d
