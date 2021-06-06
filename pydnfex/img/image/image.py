from pydnfex.hard_code import PIX_SIZE, IMAGE_EXTRA_NONE
from pydnfex.util.io_helper import IOHelper


class Image:
    def __init__(self, fmt):
        self._io = None
        self._data = None
        self._offset = 0
        self._size = 0

        self.format = fmt
        self.extra = IMAGE_EXTRA_NONE
        self.w = 0
        self.h = 0
        self.x = 0
        self.y = 0
        self.mw = 0
        self.mh = 0

    def set_io_info(self, offset, io=None):
        self._offset = offset
        self._io = io

    def open(self, io, fix_size=False, **kwargs):
        w, h, size, x, y, mw, mh = IOHelper.read_struct(io, '<7i')
        self.w = w
        self.h = h
        self._size = size
        # fix size to real size.
        if fix_size and self.extra == IMAGE_EXTRA_NONE:
            self._size = self.size_fix
        self.x = x
        self.y = y
        self.mw = mw
        self.mh = mh

        return self

    @property
    def size(self):
        return self._size

    @property
    def size_fix(self):
        return self.w * self.h * PIX_SIZE[self.format]

    def load(self, force=False):
        if self._io and (force or not self.is_loaded):
            self._data = IOHelper.read_range(self._io, self._offset, self._size)
            return True

        return False

    def save(self, io_header):
        # format, extra, w, h, size, x, y, mw, mh
        IOHelper.write_struct(io_header, '<9i', self.format, self.extra, self.w, self.h, self.size,
                              self.x, self.y, self.mw, self.mh)

    @property
    def is_loaded(self):
        return self._data is not None

    @property
    def data(self):
        if not self.is_loaded:
            self.load()
        return self._data
