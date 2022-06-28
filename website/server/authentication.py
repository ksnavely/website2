"""
These components are used with flask-login to
provide authentication for the flask layer.
"""
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username):
        self.id = username


def setup_auth_hooks(login_manager):
    @login_manager.user_loader
    def load_user(username):
        return User(username)
