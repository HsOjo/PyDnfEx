from typing import TYPE_CHECKING

from pydnfex.hard_code import IMAGE_FORMAT_LINK
from pydnfex.util.io_helper import IOHelper

if TYPE_CHECKING:
    from pydnfex.img.image import Image, ZlibImage, SpriteZlibImage


class ImageLink:
    def __init__(self, images, index):
        self._images = images  # type: list
        self._index = index
        self._image = None  # type: Union[Image, ImageLink, ZlibImage, SpriteZlibImage]

    def load_image(self):
        self._image = self._images[self.index]

    @staticmethod
    def open(io, images, **kwargs):
        [index] = IOHelper.read_struct(io, '<i')
        link = ImageLink(images, index)
        return link

    def save(self, io):
        # format, link_index
        IOHelper.write_struct(io, '<2i', IMAGE_FORMAT_LINK, self.index)

    def set_image(self, image):
        if image in self._images:
            self._image = image
            return True

        return False

    @property
    def index(self):
        if self._image is None:
            return self._index
        return self._images.index(self._image)

    @property
    def image(self):
        return self._image

    @property
    def final_image(self):
        final = self
        repeat = set()
        while isinstance(final, ImageLink):
            if final in repeat:
                raise Exception('Circular Link:', final._index)
            else:
                repeat.add(final)

            final = final.image

        return final
