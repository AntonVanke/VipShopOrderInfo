import yaml
from tinydb import TinyDB, where

from utils.get_orders import get_order
from utils.user_info import is_visible, get_user_info
from utils.get_details import get_details
from utils.get_browser import chrome
from utils.get_cookie import get_qr_code, get_cookie

browser = chrome()
db = TinyDB("database.json")
users = db.table("users")
orders = db.table("orders")
details = db.table("details")


def add_user():
    qr_code = get_qr_code(browser)
    print(qr_code)
    cookie = get_cookie(browser)
    if not users.search(where("id") == cookie[0]):
        users.insert({"id": cookie[0], "token": cookie[1]})


def check_user():
    for user in users.all():
        print(is_visible(user["id"], user["token"]))


check_user()
