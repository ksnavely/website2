from copy import deepcopy
import json


PROD_CONF_PATH = "/etc/website.conf"


defaults = {"LOG_FILE": "website.log", "SECRET_KEY": "keep it secret, keep it safe"}


def _production_config():
    try:
        prod = json.load(open(PROD_CONF_PATH, "r+"))
    except IOError as ex:
        prod = {}
    return prod


def get_config():
    prod = deepcopy(defaults)
    prod.update(_production_config())
    return prod
