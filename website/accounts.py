"""
_accounts_

This module implements basic account CRUD and authentication for what
can be used as a general secure users database.

Passwords are not stored -- bcrypt is used to hash passwords and to
check passwords at authentication time.

* Note: This module is a part of a learning project and as such I've
dispensed with a lot of the validation and niceties one might expect
in production. Use at your own risk.
"""
from website import config

import arrow
import bcrypt
from pymongo import MongoClient as MongoClient
from urllib.parse import quote_plus

CLIENT = None


# Module interface


def create_account(username, password):
    hashed_pw = _get_hashed_password(password)
    doc = {
        "_id": username,
        "username": username,
        "hashed_password": hashed_pw,
        "signup_date": arrow.utcnow().for_json(),
    }
    return _create_account(doc)


def update_account(username, updates):
    doc = _get_account(username)
    doc.update(updates)
    return _update_account(username, doc)


def get_account(username):
    return _get_account(username)


def delete_account(username):
    return _delete_account(username)


def authenticate(username, password):
    doc = _get_account(username)
    return _check_password(password, doc["hashed_password"])


# Private interface


def _client():
    global CLIENT
    if CLIENT is None:
        cfg = config.get_config()
        uri = f'mongodb://{quote_plus(cfg["MONGODB_AUTH_USR"])}:{quote_plus(cfg["MONGODB_AUTH_PW"])}@{cfg["MONGODB_HOST"]}'
        CLIENT = MongoClient(host=uri, authSource=cfg["MONGODB_AUTH_DB"])
    return CLIENT


def _get_auth_collection():
    return _client().accounts.kdevops_auth


def _get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def _check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password, hashed_password)


def _get_account(username):
    return _get_auth_collection().find_one({"_id": username})


def _create_account(acct_doc):
    return _get_auth_collection().insert_one(acct_doc)


def _update_account(username, contents):
    return _get_auth_collection().update({"_id": username}, contents)


def _delete_account(username):
    return _get_auth_collection().delete_one({"_id": username})
