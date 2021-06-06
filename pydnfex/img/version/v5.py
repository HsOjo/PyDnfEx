from io import FileIO
from typing import List

from pydnfex.util.io_helper import IOHelper
from .v4 import IMGv4
from ..image import Sprites, SpriteZlibImage


class IMGv5(IMGv4):
    def __init__(self):
        super().__init__()
        self._sprites_list = []  # type: List[Sprites]

    def _callback_before_images_open(self):
        io = self._io  # type: FileIO

        # sprites image.
        sprites_count, file_size = IOHelper.read_struct(io, '<2i')

        super()._callback_before_images_open()

        sprites_list = []
        for _ in range(sprites_count):
            sprites_list.append(Sprites.open(io))

        self._sprites_list = sprites_list

    def _callback_before_count_image_offset(self, offset):
        for sprites in self._sprites_list:
            sprites.set_io_info(offset, self._io)
            offset += sprites.data_size

        return offset

    def load_all(self, force=False):
        super().load_all(force)

        for sprites in self._sprites_list:
            sprites.load(force)

    @property
    def sprites_list(self):
        return self._sprites_list

    @property
    def images_header_size(self):
        size = super().images_header_size
        for image in self._images:
            if isinstance(image, SpriteZlibImage):
                # keep, map_index, left, top, right, bottom, rotate
                size += 28

        return size

    @property
    def file_size(self):
        size = super().file_size
        # map_count, img_size
        size += 8
        # keep, format, index, data_size, raw_size, w, h
        size += len(self._sprites_list) * 28

        return size

    @property
    def images_data_size(self):
        size = super().images_data_size
        for sprites in self._sprites_list:
            size += len(sprites.zip_data)

        return size

    def _callback_before_images_save(self, io):
        # map_count, file_size
        IOHelper.write_struct(io, '<2i', len(self._sprites_list), self.file_size)

        super()._callback_before_images_save(io)

        for sprites in self._sprites_list:
            sprites.save(io)

    def _callback_after_images_save(self, io):
        for sprites in self._sprites_list:
            io.write(sprites.zip_data)

        super()._callback_after_images_save(io)

    def _build(self, image, **kwargs):
        if isinstance(image, SpriteZlibImage):
            l, t, r, b = image.left, image.top, image.right, image.bottom
            sprites = self._sprites_list[image.map_index]
            result = sprites.build_sprite((l, t, r, b), image.rotate)
        else:
            result = super()._build(image, **kwargs)

        return result
