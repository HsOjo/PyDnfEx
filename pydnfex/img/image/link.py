from pydnfex.hard_code import IMAGE_FORMAT_LINK
from pydnfex.util.io_helper import IOHelper


class ImageLink:
    def __init__(self, images, index):
        self._images = images  # type: list
        self._index = index
        self._image = None

    def load_image(self):
        self._image = self._images[self.index - 1]

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
        return self._images.index(self._image) + 1

    @property
    def image(self):
        return self._image
