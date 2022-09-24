from pymongo import MongoClient
from conf import conf

client = MongoClient(conf['mongod_conf']['url'])

miyanodb = client['miyano']