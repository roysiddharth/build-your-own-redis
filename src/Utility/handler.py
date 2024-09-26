database = {} # In-memory python dictionary as database

def handle_command(command, conn):
    """
    Handles the parsed command and sends the appropriate response.
    """
    cmd = command[0]
    args = command[1]

    if cmd == 'PING':
        conn.sendall(b"+PONG\r\n")
    elif cmd == 'ECHO' and len(args) >= 1:
        # Respond with the message directly, without the bulk string format
        message = ' '.join(args)
        response = f"{message}\r\n"
        conn.sendall(response.encode())
    elif cmd == 'SET' and len(args) == 2:
        key, value = args[0], args[1]
        database[key] = value  # Store the key-value pair in the in-memory database
        conn.sendall(b"+OK\r\n")
    elif cmd == 'GET' and len(args) == 1:
        key = args[0]
        value = database.get(key, None)  # Retrieve value from the in-memory database
        if value is not None:
            # Simply return the value without the RESP bulk string length format
            response = f"{value}\r\n"
            conn.sendall(response.encode())
        else:
            conn.sendall(b"-ERR key does not exist\r\n")  # Null bulk string if the key does not exist
    else:
        conn.sendall(b"-ERR unknown command\r\n")