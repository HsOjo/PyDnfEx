from io import BytesIO

from pydnfex.util.io_helper import IOHelper
from .factory import FormatFactory


class FormatConvertor:
    @staticmethod
    def to_raw_indexes(data, colors):
        with BytesIO(data) as io_indexes:
            with BytesIO() as io_raw:
                temp = IOHelper.read_struct(io_indexes, '<B', False)
                while temp is not None:
                    [index] = temp
                    IOHelper.write_struct(io_raw, '<4B', *colors[index])
                    temp = IOHelper.read_struct(io_indexes, '<B', False)
                data_raw = IOHelper.read_range(io_raw)

        return data_raw

    @staticmethod
    def to_raw(data, image_format):
        fmt = FormatFactory.instance(image_format)
        return fmt.to_raw(data)

    @staticmethod
    def to_raw_crop(data, image_format, w, box):
        fmt = FormatFactory.instance(image_format)
        return fmt.to_raw_crop(data, w, box)

    @staticmethod
    def from_image(image, image_format):
        fmt = FormatFactory.instance(image_format)
        return fmt.from_image(image)
