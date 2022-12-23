import zlib


def zfill_bytes(data, size):
    fill_size = size - len(data)
    if fill_size > 0:
        data += b'\x00' * fill_size
    return data


def zlib_decompress(data: bytes):
    if data.startswith(b'\x78'):
        data = zlib.decompress(data)
    else:
        header_index = data.rfind(b'\x78')
        try:
            data = zlib.decompress(data[header_index:] + data)
        except zlib.error:
            data = zlib.decompress(data[header_index:header_index + 2] + data)

    return data
