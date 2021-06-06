from pydnfex.hard_code import IMAGE_EXTRA_ZLIB_SPRITE
from pydnfex.util.io_helper import IOHelper
from .zlib import ZlibImage


class SpriteZlibImage(ZlibImage):
    def __init__(self, fmt):
        super().__init__(fmt)
        self.extra = IMAGE_EXTRA_ZLIB_SPRITE

        self.keep = 0
        self.map_index = 0
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0

        # horizontal, vertical
        self.rotate = 0

    def _open(self, io):
        super()._open(io)

        keep, map_index, lx, ly, rx, ry, rotate = IOHelper.read_struct(io, '<7i')

        self.keep = keep
        self.map_index = map_index
        self.left = lx
        self.top = ly
        self.right = rx
        self.bottom = ry
        self.rotate = rotate

    def save(self, io_header):
        super().save(io_header)
        # keep, map_index, left, top, right, bottom, rotate
        IOHelper.write_struct(io_header, '<7i', self.keep, self.map_index,
                              self.left, self.top, self.right, self.bottom, self.rotate)