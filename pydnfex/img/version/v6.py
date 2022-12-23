from io import FileIO
from typing import List

from pydnfex.util import image as image_util
from pydnfex.util.io_helper import IOHelper
from .v2 import IMGv2
from ..image import ColorBoard, FormatConvertor


class IMGv6(IMGv2):
    def __init__(self):
        super().__init__()
        self._color_boards = []  # type: List[ColorBoard]

    def _callback_before_images_open(self):
        io = self._io  # type: FileIO

        # multiple color board.
        color_boards = []

        [color_board_count] = IOHelper.read_struct(io, 'i')
        for _ in range(color_board_count):
            color_board = ColorBoard.open(io)
            color_boards.append(color_board)

        self._color_boards = color_boards

    @property
    def color_boards(self):
        return self._color_boards

    @property
    def file_size(self):
        size = super().file_size
        # color_boards_count
        size += 4
        for color_board_v6 in self._color_boards:
            # color count.
            size += 4
            # colors size.
            size += len(color_board_v6.colors) * 4

        return size

    def _callback_before_images_save(self, io):
        # color_board count.
        IOHelper.write_struct(io, 'i', len(self._color_boards))
        for color_board in self._color_boards:
            color_board.save(io)

    def build(self, image, color_board=None, **kwargs):
        return super().build(image, color_board=color_board, **kwargs)

    def _build(self, image, color_board=None, **kwargs):
        if color_board is None and len(self._color_boards) > 0:
            color_board = self._color_boards[0]

        data = FormatConvertor.to_raw_indexes(image.data, color_board.colors)
        result = image_util.load_raw(data, image.w, image.h)
        return result

    def color_board_by_index(self, index):
        if 0 <= index < len(self._color_boards):
            return self._color_boards[index]
