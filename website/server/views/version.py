import website

from flask import jsonify


def version():
    """
    Returns version JSON.
    """
    info = {
        "ok": True,
        "version": website.__version__,
    }

    return jsonify(info)
