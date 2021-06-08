import zlib

from pydnfex.hard_code import IMAGE_EXTRA_ZLIB
from ..image import Image


class ZlibImage(Image):
    def __init__(self, fmt):
        super().__init__(fmt)
        self.extra = IMAGE_EXTRA_ZLIB

        self._zip_data = None

    def load(self, force=False):
        super().load(force)
        self._zip_data = self._data
        self._data = None

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

    @property
    def data(self):
        zip_data = self.zip_data
        if self._data is None and self.is_loaded:
            self._data = zlib.decompress(zip_data)
        return self._data

    @property
    def is_loaded(self):
        return self._zip_data is not None

    def save(self, io):
        self.compress()
        super().save(io)
