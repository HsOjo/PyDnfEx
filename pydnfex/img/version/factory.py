from pydnfex.hard_code import *
from pydnfex.util.io_helper import IOHelper
from .v1 import IMGv1
from .v2 import IMGv2
from .v4 import IMGv4
from .v5 import IMGv5
from .v6 import IMGv6


class NotIMGFileException(Exception):
    pass


class IMGVersionException(Exception):
    pass


class IMGFactory:
    @staticmethod
    def instance(version):
        cls_version_map = {
            IMG_VERSION_1: IMGv1,
            IMG_VERSION_2: IMGv2,
            IMG_VERSION_4: IMGv4,
            IMG_VERSION_5: IMGv5,
            IMG_VERSION_6: IMGv6,
        }

        cls = cls_version_map.get(version)
        if cls is None:
            raise IMGVersionException(version)

        return cls()

    @staticmethod
    def open(io):
        magic = IOHelper.read_ascii_string(io, 18)
        if magic not in [IMG_MAGIC, IMG_MAGIC_OLD]:
            raise NotIMGFileException

        images_size = 0
        if magic == IMG_MAGIC:
            # images_size without version,count,extra(color_board,sprites)...
            [images_size] = IOHelper.read_struct(io, 'i')
        elif magic == IMG_MAGIC_OLD:
            # unknown.
            [_] = IOHelper.read_struct(io, 'h')

        # keep: 0
        [keep, version] = IOHelper.read_struct(io, '<2i')

        img = IMGFactory.instance(version)
        img.open(io, version, images_size, keep)

        return img
