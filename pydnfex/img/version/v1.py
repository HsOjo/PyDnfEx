from io import SEEK_CUR

from pydnfex.hard_code import IMG_MAGIC_OLD
from pydnfex.util.io_helper import IOHelper
from .img import IMG
from .. import ImageLink, ImageFactory


class IMGv1(IMG):
    def _callback_images_open(self, count):
        io = self._io

        images = []
        for _ in range(count):
            image = ImageFactory.open(io, images, fix_size=True)
            images.append(image)

            offset = io.tell()
            image.set_io_info(offset, io)
            io.seek(image.size, SEEK_CUR)

        self._images = images

    def _callback_after_images_open(self, images_size):
        for image in self._images:
            if isinstance(image, ImageLink):
                image.load_image()

    def _callback_before_save(self, io):
        IOHelper.write_ascii_string(io, IMG_MAGIC_OLD)
        # TODO: unknown, now be zero.
        IOHelper.write_struct(io, 'h', 0)

    @property
    def _common_size(self):
        # magic, unknown
        size = len(IMG_MAGIC_OLD) + 3

        return size

    def _callback_images_save(self, io):
        for image in self._images:
            image.save(io)
            io.write(image.data)
