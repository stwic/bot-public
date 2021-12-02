from pymongo import MongoClient
from config import mongo_password, mongo_url
from cryptos import cryptos
import urllib

password = urllib.parse.quote(mongo_password)
client = MongoClient(mongo_url % password)

def init_cryptos_db():
    db=client.blackFlag
    # insert new collection only if empty
    if db.cryptos.count() == 0:
        db.cryptos.insert_many(cryptos)
    print(db.cryptos.count())
    return db.cryptos

cryptos=init_cryptos_db()