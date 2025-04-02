def fixed_16_bytes(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    if len(data) < 16:
        return data + b'\x00' * (16 - len(data))
    return data[:16]