import zlib

from pydnfex.hard_code import IMAGE_FORMATS_DDS
from pydnfex.img.image.format import FormatConvertor
from pydnfex.util import image as image_util
from pydnfex.util.common import zlib_decompress
from pydnfex.util.io_helper import IOHelper


class Sprite:
    def __init__(self):
        self._io = None
        self._offset = 0
        self._data = None
        self._zip_data = None

        self.keep = 0
        self.format = 0
        self.index = 0
        self.data_size = 0
        self.raw_size = 0
        self.w = 0
        self.h = 0

    def set_io_info(self, offset, io):
        self._io = io
        self._offset = offset

    @staticmethod
    def open(io):
        keep, fmt, index, data_size, raw_size, w, h = IOHelper.read_struct(io, '<7i')

        sprite = Sprite()
        sprite.keep = keep
        sprite.format = fmt
        sprite.index = index
        sprite.data_size = data_size
        sprite.raw_size = raw_size
        sprite.w = w
        sprite.h = h

        return sprite

    def load(self, force=False):
        if self._io and (force or not self.is_loaded):
            self._zip_data = IOHelper.read_range(self._io, self._offset, self.data_size)
            self._data = zlib_decompress(self._zip_data)

    def save(self, io):
        self.compress()
        IOHelper.write_struct(io, '<7i', self.keep, self.format, self.index,
                              self.data_size, self.raw_size, self.w, self.h)

    @property
    def is_loaded(self):
        return self._data is not None

    @property
    def data(self):
        if not self.is_loaded:
            self.load()
        return self._data

    def set_data(self, data):
        self.raw_size = len(data)
        self._data = data
        self.data_size = 0
        self._zip_data = None

    def compress(self):
        data = self.data
        self.raw_size = len(data)
        data = zlib.compress(data)
        self.data_size = len(data)
        self._zip_data = data

    @property
    def zip_data(self):
        if not self.is_loaded:
            self.load()
        if self._zip_data is None and self._data:
            self.compress()
        return self._zip_data

    def build(self, box=None, rotate=0):
        data = self.data

        if self.format in IMAGE_FORMATS_DDS:
            image = image_util.load_dds(data, box, rotate)
        else:
            if box:
                data = FormatConvertor.to_raw_crop(data, self.format, self.w, box)
                [l, t, r, b] = box
                w, h = r - l, b - t
            else:
                data = FormatConvertor.to_raw(data, self.format)
                w, h = self.w, self.h
            image = image_util.load_raw(data, w, h, rotate)

        return image
