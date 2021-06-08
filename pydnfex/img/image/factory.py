from pydnfex.hard_code import *
from pydnfex.util.io_helper import IOHelper
from .exception import *
from .extra import ZlibImage, SpriteZlibImage
from .image import Image
from .link import ImageLink


class ImageFactory:
    @staticmethod
    def instance(fmt=IMAGE_FORMAT_8888, extra=IMAGE_EXTRA_NONE):
        cls_extra_map = {
            IMAGE_EXTRA_NONE: Image,
            IMAGE_EXTRA_ZLIB: ZlibImage,
            IMAGE_EXTRA_ZLIB_SPRITE: SpriteZlibImage,
        }

        cls = cls_extra_map.get(extra)
        if cls is None:
            raise ImageExtraException(extra)

        return cls(fmt)

    @staticmethod
    def open(io, images, **kwargs):
        [fmt] = IOHelper.read_struct(io, '<i')
        if fmt not in IMAGE_FORMATS_ALL:
            raise ImageFormatException(fmt)

        if fmt == IMAGE_FORMAT_LINK:
            return ImageLink.open(io, images, **kwargs)
        else:
            [extra] = IOHelper.read_struct(io, '<i')
            return ImageFactory.instance(fmt, extra).open(io, **kwargs)
