from pydnfex.hard_code import IMAGE_EXTRA_ZLIB_SPRITE
from pydnfex.util.io_helper import IOHelper
from ..image import Image


class SpriteZlibImage(Image):
    def __init__(self, fmt):
        super().__init__(fmt)
        self.extra = IMAGE_EXTRA_ZLIB_SPRITE

        self.keep = 0
        self.sprite_index = 0
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0

        # horizontal, vertical
        self.rotate = 0

    def open(self, io, **kwargs):
        super().open(io)

        keep, sprite_index, lx, ly, rx, ry, rotate = IOHelper.read_struct(io, '<7i')

        self.keep = keep
        self.sprite_index = sprite_index
        self.left = lx
        self.top = ly
        self.right = rx
        self.bottom = ry
        self.rotate = rotate

        return self

    def save(self, io):
        super().save(io)
        # keep, sprite_index, left, top, right, bottom, rotate
        IOHelper.write_struct(io, '<7i', self.keep, self.sprite_index,
                              self.left, self.top, self.right, self.bottom, self.rotate)
