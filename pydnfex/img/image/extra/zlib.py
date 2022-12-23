import zlib

from pydnfex.hard_code import IMAGE_EXTRA_ZLIB
from pydnfex.util.common import zlib_decompress
from ..image import Image


class ZlibImage(Image):
    def __init__(self, fmt):
        super().__init__(fmt)
        self.extra = IMAGE_EXTRA_ZLIB

        self._zip_data = None

    def load(self, force=False):
        super().load(force)
        self._zip_data = self._data
        self._data = zlib_decompress(self._zip_data)

    def compress(self):
        data = zlib.compress(self.data)
        self._size = len(data)
        self._zip_data = data

    def set_data(self, data):
        super().set_data(data)
        self._size = 0
        self._zip_data = None

    @property
    def zip_data(self):
        if not self.is_loaded:
            self.load()
        if self._zip_data is None and self._data:
            self.compress()
        return self._zip_data

    def save(self, io):
        self.compress()
        super().save(io)
