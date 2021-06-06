from pydnfex.hard_code import NPK_FILENAME_DECORD_FLAG
from pydnfex.util import common
from pydnfex.util.io_helper import IOHelper


class File:
    def __init__(self, name, data=None):
        self._io = None
        self.name = name  # type: str
        self._offset = 0  # type: int
        self._size = 0  # type: int
        self._data = data  # type: bytes

    def set_io_info(self, offset, size, io=None):
        self._offset = offset
        self._size = size
        self._io = io

    @staticmethod
    def open(io):
        offset, size = IOHelper.read_struct(io, '<2i')
        name_data = File._decrypt_name(io.read(256))
        try:
            name = name_data.decode('euc_kr')
            name = name[:name.find('\x00')]
        except:
            name = name_data[:name_data.find(b'\x00')].decode('euc_kr', errors='ignore')

        file = File(name)
        file.set_io_info(offset, size, io)

        return file

    def save(self, io_header, offset, io):
        IOHelper.write_struct(io_header, '<2i', offset, self._size)

        name_data = self.name
        if isinstance(name_data, str):
            name_data = name_data.encode(encoding='euc_kr')

        name_data = self._decrypt_name(name_data)

        io_header.write(name_data)

        io.seek(offset)
        io.write(self.data)

    @property
    def data(self):
        if not self.is_loaded:
            self.load()
        return self._data

    def load(self, force=False, size=None):
        if self._io and (force or not self.is_loaded):
            size = self._size if size is None else size
            self._data = IOHelper.read_range(self._io, self._offset, size)
            return True

        return False

    @property
    def is_loaded(self):
        return self._data is not None

    @property
    def offset(self):
        return self._offset

    @property
    def size(self):
        return self._size

    @property
    def data_size(self):
        return len(self.data)

    @staticmethod
    def _decrypt_name(data):
        data = common.zfill_bytes(data, 256)
        result_list = [0] * 256

        for i in range(256):
            result_list[i] = data[i] ^ NPK_FILENAME_DECORD_FLAG[i]

        result = bytes(result_list)
        return result
