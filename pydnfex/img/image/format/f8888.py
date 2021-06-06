from pydnfex.hard_code import PIX_SIZE, IMAGE_FORMAT_8888
from pydnfex.util.io_helper import IOHelper
from .format import Format


class Format8888(Format):
    ps = PIX_SIZE[IMAGE_FORMAT_8888]

    def callback_to_raw(self, io, io_raw):
        temp = IOHelper.read_struct(io, '<4B', False)
        while temp is not None:
            [b, g, r, a] = temp
            IOHelper.write_struct(io_raw, '<4B', r, g, b, a)

            temp = IOHelper.read_struct(io, '<4B', False)

    def callback_to_raw_crop_convert(self, io, io_raw):
        temp = IOHelper.read_struct(io, '<4B', False)
        if temp is not None:
            [b, g, r, a] = temp
            IOHelper.write_struct(io_raw, '<4B', r, g, b, a)

    def callback_from_image_convert(self, io, pixel):
        [r, g, b, a] = pixel
        IOHelper.write_struct(io, "<4B", b, g, r, a)
