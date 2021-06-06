from pydnfex.hard_code import PIX_SIZE, IMAGE_FORMAT_1555
from pydnfex.util.io_helper import IOHelper
from .color import Color
from .format import Format


class Format1555(Format):
    ps = PIX_SIZE[IMAGE_FORMAT_1555]

    def callback_to_raw(self, io, io_raw):
        temp = IOHelper.read_struct(io, '<2B', False)
        while temp is not None:
            [v1, v2] = temp
            IOHelper.write_struct(io_raw, '<4B', *Color.from_1555(v1, v2))

            temp = IOHelper.read_struct(io, '<2B', False)

    def callback_to_raw_crop_convert(self, io, io_raw):
        temp = IOHelper.read_struct(io, '<2B', False)
        if temp is not None:
            [v1, v2] = temp
            IOHelper.write_struct(io_raw, '<4B', *Color.from_1555(v1, v2))

    def callback_from_image_convert(self, io, pixel):
        IOHelper.write_struct(io, "<2B", *Color.to_1555(*pixel))
