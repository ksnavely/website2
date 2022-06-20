"""
These components are used with flask-login to
provide authentication for the flask layer.
"""
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.is_active = True
        self.is_authenticated = False
        self.is_anonymous = True

    @property
    def is_active(self):
        return self.__is_active

    @property
    def is_authenticated(self):
        return self.__is_authenticated

    @property
    def is_anonymous(self):
        return self.__is_active

    def get_id(self):
        return self.username


def setup_auth_hooks(login_manager):
    @login_manager.user_loader
    def load_user(username):
        return User(username)
