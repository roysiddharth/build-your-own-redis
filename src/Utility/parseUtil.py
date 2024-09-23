def parse_resp(data):
    """
    Parses RESP (Redis Serialization Protocol) encoded data.
    Supports parsing array commands like *1\r\n$4\r\nPING\r\n
    """
    if data.startswith(b'*'):
        parts = data.split(b'\r\n')
        array_size = int(parts[0][1:])
        command = parts[2].decode()
        return command
    return data