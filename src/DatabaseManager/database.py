from pymongo import MongoClient
from globals import db_obj

client = MongoClient('localhost', 27017)
db = client['redis_storage']
collection = db['kv_store']

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