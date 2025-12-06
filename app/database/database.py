from pymongo import MongoClient
import certifi
from flask import current_app

MONGO_URI = 'mongodb+srv://mateo:mateo@cluster0.kipdlog.mongodb.net/?appName=Cluster0'
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["dbb_products_app"]
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db
