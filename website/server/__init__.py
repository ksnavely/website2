import logging
import sys

from flask import Flask
from flask_login import LoginManager

import website
from website.config import get_config
from website.server import authentication, utils
from website.server.views import frontpage, login, logout, version


LOGGER = None


#
# functions for building the Flask application
#


def build_application():
    app = Flask(__name__)

    # Setup for flask-login
    login_manager = LoginManager()
    login_manager.init_app(app)
    authentication.setup_auth_hooks(login_manager)

    app.config.update(get_config())

    return app


def setup_logging(app):
    global LOGGER

    LOGGER = logging.getLogger(__name__)
    filerh = logging.FileHandler(app.config["LOG_FILE"])
    filerh.setLevel(logging.DEBUG)
    LOGGER.addHandler(filerh)
    stdouth = logging.StreamHandler(stream=sys.stdout)
    stdouth.setLevel(logging.DEBUG)
    LOGGER.addHandler(stdouth)

    @app.errorhandler(Exception)
    def exception_handler(error):
        LOGGER.exception("Unexpected error: {0}".format(error))
        return "Server Error", 500

    LOGGER.debug("website: logging initiated")


def setup_jinja_globals(app):
    app.jinja_env.globals.update(archive_dates=utils.archive_dates)


#
# Set up the application, logging, endpoints
#

app = build_application()
setup_logging(app)
setup_jinja_globals(app)

app.add_url_rule("/", "index", frontpage.index, methods=["GET"])
app.add_url_rule("/login", "login", login.login, methods=["POST"])
app.add_url_rule("/logout", "logout", logout.logout, methods=["POST"])
app.add_url_rule("/version", "version", version.version, methods=["GET"])
app.add_url_rule(
    "/create_post", "create_post", frontpage.create_blog_entry, methods=["GET"]
)
app.add_url_rule(
    "/create_post",
    "create_post_submit",
    frontpage.create_blog_entry_submit,
    methods=["POST"],
)
app.add_url_rule("/<post_id>", "get_post", frontpage.get_blog_entry, methods=["GET"])
app.add_url_rule(
    "/update_post/<post_id>",
    "update_post",
    frontpage.update_blog_entry,
    methods=["GET"],
)
app.add_url_rule(
    "/update_post/<post_id>",
    "update_post_submit",
    frontpage.update_blog_entry_submit,
    methods=["POST"],
)

if __name__ == "__main__":
    app.run()
