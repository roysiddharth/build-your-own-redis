def parse_resp(data):
    """
    Parses both RESP and simple commands.
    - RESP for array commands like SET key value.
    - Simple string parsing for commands like PING, SET key value.
    Returns a tuple (command, args) where command is the Redis command and args are the arguments.
    """
    parts = data.split(b'\r\n')

    # Handle RESP commands (starting with *)
    if parts[0].startswith(b'*'):
        # Array of bulk strings or commands (RESP format)
        array_size = int(parts[0][1:])  # Extract the number of elements in the array
        elements = []
        i = 1

        while len(elements) < array_size and i < len(parts):
            if parts[i].startswith(b'$'):
                # Bulk string: next line contains the actual content
                string_length = int(parts[i][1:])  # Length of the bulk string (can be ignored for now)
                element = parts[i + 1].decode()    # The actual string content
                elements.append(element)
                i += 2  # Move to the next bulk string (skip length line and content line)
            else:
                i += 1  # Skip over invalid parts (if any)

        if len(elements) > 0:
            command = elements[0].upper()  # First element is the command
            args = elements[1:]            # The rest are arguments (if any)
            return (command, args)

    # Handle simple string commands (e.g., SET key value)
    elif data.endswith(b'\r\n'):
        # Split by spaces to handle commands like SET key value
        command_parts = data.decode().strip().split(' ')
        command = command_parts[0].upper()  # First part is the command
        args = command_parts[1:]            # The rest are arguments
        return (command, args)

    return None
