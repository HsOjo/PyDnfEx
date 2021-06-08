from pydnfex.hard_code import *
from .f1555 import Format1555
from .f4444 import Format4444
from .f8888 import Format8888


class ImageFormatException(Exception):
    pass


class FormatFactory:
    @staticmethod
    def instance(image_format):
        cls_format_map = {
            IMAGE_FORMAT_1555: Format1555,
            IMAGE_FORMAT_4444: Format4444,
            IMAGE_FORMAT_8888: Format8888,
        }

        cls = cls_format_map.get(image_format)
        if cls is None:
            raise ImageFormatException(image_format)

        return cls()
