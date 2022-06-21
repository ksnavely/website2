from website import accounts
from flask import jsonify, request


def new_user():
    """
    Create a new user. Expects the following JSON data:
      - username: the desired username
      - password: the desired password
    """
    if not request.json:
        return jsonify({"error": "Request must include JSON content"}), 400

    username = request.json.get("username")
    password = request.json.get("password")

    if None in [username, password]:
        return (jsonify({"error": "Request must include JSON username and password."}),)
        400

    ack = accounts.create_account(username, password)
    return jsonify({"created": ack.inserted_id}), 201
