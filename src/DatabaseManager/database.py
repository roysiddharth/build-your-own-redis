import os
from pymongo import MongoClient
from globals import db_obj

MONGO_HOST=os.environ.get("MONGO_HOST")
MONGO_PORT=int(os.environ.get("MONGO_PORT"))
MONGO_DB=os.environ.get("MONGO_DB")
MONGO_COLLECTION=os.environ.get("MONGO_COLLECTION")

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

def save_data_to_mongodb():
    """
    Save the entire in-memory Python dictionary to MongoDB.
    """
    global db_obj
    for key, value in db_obj.items():
        collection.update_one({'key': key}, {'$set': {'value': value}}, upsert=True)
    print("Data saved to MongoDB")

def load_data_from_mongodb():
    """
    Load all key-value pairs from MongoDB into the in-memory Python dictionary.
    """
    global db_obj
    for item in collection.find():
        db_obj[item['key']] = item['value']
    print("Data loaded from MongoDB.")