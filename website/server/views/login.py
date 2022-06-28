from flask import jsonify, redirect, request, url_for
from flask_login import login_user

from website.accounts import authenticate, get_account
from website.server.authentication import User


def login():
    """
    Process a form-data based login. Redirect to the front page on success,
    error otherwise.
    """
    validation_msg = (
        "Login request must contain form encoded username and "
        "password fields, with string values."
    )

    if not request.form:
        return jsonify({"error": validation_msg}), 401

    username = request.form.get("username")
    password = request.form.get("password")

    validated = all([isinstance(username, str), isinstance(password, str)])
    if not validated:
        return jsonify({"error": validation_msg}), 401

    failed_auth_msg = "Authentication failed."

    if get_account(username) is None:
        return jsonify({"error": failed_auth_msg}), 401

    user = User(username)

    if authenticate(user.id, password):
        login_user(user)
        return redirect(url_for("index", _external=True, _scheme="https"))
    else:
        return jsonify({"error": failed_auth_msg}), 401
