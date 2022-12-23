from typing import List, Union

from pydnfex.util import image as image_util
from pydnfex.util.io_helper import IOHelper
from ..image import Image, ImageLink, ZlibImage, FormatConvertor, SpriteZlibImage


class IMG:
    def __init__(self):
        self._io = None
        self._keep = 0
        self._version = 0
        self._images = []  # type: List[Union[Image, ImageLink, ZlibImage, SpriteZlibImage]]

    def open(self, io, version, images_size, keep):
        self._io = io
        self._version = version
        self._keep = keep

        [image_count] = IOHelper.read_struct(io, '<i')

        self._callback_before_images_open()
        self._callback_images_open(image_count)
        self._callback_after_images_open(images_size)

    def _callback_before_images_open(self):
        pass

    def _callback_images_open(self, count):
        pass

    def _callback_after_images_open(self, images_size):
        pass

    def load_all(self, force=False):
        for image in self._images:
            image.load(force)

    @property
    def version(self):
        return self._version

    @property
    def images(self):
        return self._images

    def save(self, io):
        io.truncate()
        self._callback_before_save(io)
        # keep, version, img_count
        IOHelper.write_struct(io, '<3i', self._keep, self._version, len(self._images))
        self._callback_before_images_save(io)
        self._callback_images_save(io)
        self._callback_after_images_save(io)

    def _callback_before_save(self, io):
        pass

    def _callback_before_images_save(self, io):
        pass

    def _callback_images_save(self, io):
        pass

    def _callback_after_images_save(self, io):
        pass

    @property
    def images_header_size(self):
        size = 0
        for image in self._images:
            # format
            size += 4
            if isinstance(image, ImageLink):
                # link
                size += 4
            else:
                # extra, w, h, size, x, y, mw, mh
                size += 32

        return size

    @property
    def images_data_size(self):
        size = 0
        for image in self._images:
            if type(image) in [ImageLink, SpriteZlibImage]:
                continue
            elif isinstance(image, ZlibImage):
                data = image.zip_data
            else:
                data = image.data

            size += len(data)

        return size

    @property
    def file_size(self):
        size = self._common_size

        # keep, version, img_count
        size += 12

        size += self.images_header_size
        size += self.images_data_size

        return size

    @property
    def _common_size(self):
        return 0

    def build(self, image, **kwargs):
        if isinstance(image, ImageLink):
            return self.build(image.final_image, **kwargs)

        return self._build(image, **kwargs)

    def _build(self, image, **kwargs):
        data = FormatConvertor.to_raw(image.data, image.format)
        result = image_util.load_raw(data, image.w, image.h)

        return result

    def image_by_index(self, index):
        if 0 <= index < len(self._images):
            return self._images[index]
