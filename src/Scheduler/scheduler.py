import os
import time
import threading

from globals import db_obj
from DatabaseManager.database import collection

EXPIRY_CHECK_TIMER = int(os.environ.get("EXPIRY_CHECK_TIMER"))
AUTO_SAVE_TIMER = int(os.environ.get("AUTO_SAVE_TIMER"))

def remove_expired_keys():
    """
    Periodically check and remove expired keys from both the in-memory db_obj and MongoDB.
    """
    global db_obj
    
    while True:
        current_time = time.time()
        keys_to_remove = []

        # Iterate through the db_obj and find expired keys
        for key, data in db_obj.items():
            expiry = data.get("expiry")
            if expiry is not None and current_time >= expiry:
                keys_to_remove.append(key)
        
        # Remove expired keys from db_obj and MongoDB
        for key in keys_to_remove:
            del db_obj[key]  # Remove from in-memory store
            collection.delete_one({"key": key})  # Remove from MongoDB
        
        # Sleep for 1 second before checking again
        time.sleep(EXPIRY_CHECK_TIMER)

def auto_save():
    """
    Periodically save the in-memory db_obj to MongoDB.
    """
    while True:
        # Iterate over db_obj and save each key-value pair to MongoDB
        for key, data in db_obj.items():
            value = data["value"]
            expiry = data.get("expiry", None)  # Handle expiry if it exists
            # Update the MongoDB document for the key, with both value and expiry
            collection.update_one(
                {"key": key},
                {"$set": {"value": value, "expiry": expiry}},
                upsert=True
            )

        time.sleep(AUTO_SAVE_TIMER)  # Auto-save every X seconds

# Start the expiry checker in a background thread when this module is imported
def start_expiry_thread():
    """
    Start the background thread that removes expired keys.
    """
    expiry_thread = threading.Thread(target=remove_expired_keys, daemon=True)
    expiry_thread.start()

# Start the auto-save in a background thread
def start_auto_save_thread():
    """
    Start the background thread for auto-saving db_obj to MongoDB every X seconds.
    """
    auto_save_thread = threading.Thread(target=auto_save, daemon=True)
    auto_save_thread.start()
