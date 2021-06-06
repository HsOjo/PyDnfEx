import zlib

from pydnfex.hard_code import IMAGE_EXTRA_ZLIB
from ..image import Image


class ZlibImage(Image):
    def __init__(self, fmt):
        super().__init__(fmt)
        self.extra = IMAGE_EXTRA_ZLIB

        self._zip_data = None

    def load(self, force=False):
        if super().load(force):
            self._zip_data = self._data
            self._data = zlib.decompress(self._data)
            return True

        return False

    def compress(self):
        data = zlib.compress(self.data)
        self._size = len(data)
        self._zip_data = data

    @property
    def zip_data(self):
        if self._zip_data is None:
            self.compress()
        return self._zip_data
