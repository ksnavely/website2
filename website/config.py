from copy import deepcopy
import json


PROD_CONF_PATH = "/etc/website/website.json"


defaults = {
    "LOG_FILE": "website.log",
    "SECRET_KEY": "(flask secret for cookies) override this",
    "MONGODB_HOST": "127.0.0.1:27017",
    "MONGODB_DB": "blogs",
    "MONGODB_USR": "overrideme",
    "MONGODB_PW": "overrideme",
}


def _production_config():
    try:
        prod = json.load(open(PROD_CONF_PATH, "r"))
    except IOError as ex:
        prod = {}
    return prod


def get_config():
    prod = deepcopy(defaults)
    prod.update(_production_config())
    return prod
