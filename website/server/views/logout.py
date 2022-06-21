from flask import redirect, url_for
from flask_login import login_required, logout_user


@login_required
def logout():
    logout_user()
    return redirect(url_for("index", _external=True, _scheme="https"))
