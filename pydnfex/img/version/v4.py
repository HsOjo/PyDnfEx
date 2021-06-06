from pydnfex.util import image as image_util
from .v2 import IMGv2
from ..image import ColorBoard, FormatConvertor


class IMGv4(IMGv2):
    def __init__(self):
        super().__init__()
        # single color board.
        self._color_board = None  # type: ColorBoard

    def _callback_before_images_open(self):
        self._color_board = ColorBoard.open(self._io)

    @property
    def color_board(self):
        return self._color_board

    @property
    def file_size(self):
        size = super().file_size
        # color count.
        size += 4
        # colors size.
        size += len(self._color_board.colors) * 4

        return size

    def _callback_before_images_save(self, io):
        self._color_board.save(io)

    def _build(self, image, color_board=None, **kwargs):
        if color_board is None:
            color_board = self._color_board

        data = FormatConvertor.to_raw_indexes(image.data, color_board.colors)
        result = image_util.load_raw(data, image.w, image.h)

        return result
