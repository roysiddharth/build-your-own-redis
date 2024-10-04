import time

from DatabaseManager import database
from globals import db_obj

def handle_command(command, conn):
    """
    Handles the parsed command and sends the appropriate response.
    """
    global db_obj
    cmd = command[0]
    args = command[1]

    if cmd == 'PING':
        conn.sendall(b"+PONG\r\n")

    elif cmd == 'ECHO' and len(args) >= 1:
        # Respond with the message directly, without the bulk string format
        message = ' '.join(args)
        response = f"{message}\r\n"
        conn.sendall(response.encode())

    elif cmd == 'SET':
        if len(args) >= 2:
            key, value = args[0], args[1]

            # Check if EX options is provided
            if len(args) == 4 and args[2].upper() == "EX":
                try:
                    ttl = int(args[3]) # Expiration time in seconds
                    expiry_time = time.time() + ttl # Current time + ttl for expiration
                    db_obj[key] = {"value": value, "expiry": expiry_time} # Store key with expiry time
                except ValueError:
                    conn.sendall(b"-ERR invalid expiration time\r\n")
            else:
                # No expiry, store value without expiration
                db_obj[key] = {"value": value, "expiry": None}

            # Send confirmation to client
            conn.sendall(b"+OK\r\n")
        else:
            conn.sendall(b"-ERR wrong number of arguments for 'SET' command\r\n")

    elif cmd == 'GET' and len(args) == 1:
        key = args[0]
        entry = db_obj.get(key, None)  # Retrieve value from the in-memory database
        if entry is not None:
            # Check if the key has expired
            if entry["expiry"] is not None and time.time() >= entry["expiry"]:
                del db_obj[key]  # Remove the key if it's expired
                conn.sendall(b"-ERR key does not exist\r\n")
            else:
                # Return the value if it's not expired
                response = f"{entry["value"]}\r\n"
                conn.sendall(response.encode())
        else:
            conn.sendall(b"-ERR key does not exist\r\n")  # Null bulk string if the key does not exist

    elif cmd == "SAVE":
        database.save_data_to_mongodb()
        conn.sendall(b"+OK\r\n")

    else:
        conn.sendall(b"-ERR unknown command\r\n")