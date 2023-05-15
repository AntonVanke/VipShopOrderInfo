from tinydb import TinyDB, where

db = TinyDB("database.json")
# 创建表
users = db.table("users")
orders = db.table("orders")
details = db.table("details")

if not users.search(where("id") == 533372022):
    users.insert({
        "id": 533372023,
        "token": "F40CCFF26B6FABAA90E5B11CB99CE07AECAED842",
        "time": "2020-02-10T00:00:00.000Z",
        "username": "冯君奭",
        "phone": "178****9970",
        "remark": "这是一条备注"
    })
    print("ok")
