import hashlib
from io import BytesIO
from typing import List

from pydnfex.hard_code import NPK_MAGIC
from pydnfex.util.io_helper import IOHelper
from .file import File


class NotNPKFileException(Exception):
    pass


class NPK:
    def __init__(self):
        self._files = []  # type: List[File]

    @staticmethod
    def open(io):
        magic = IOHelper.read_ascii_string(io, 16)
        if magic != NPK_MAGIC:
            raise NotNPKFileException

        [count] = IOHelper.read_struct(io, 'i')

        npk = NPK()
        for i in range(count):
            npk.files.append(File.open(io))

        return npk

    def load_all(self):
        for f in self._files:
            f.load()

    def save(self, io=None):
        files = self._files

        # clean file.
        io.truncate()

        # build head in memory.
        with BytesIO() as io_header:
            IOHelper.write_ascii_string(io_header, NPK_MAGIC)
            count = len(files)
            IOHelper.write_struct(io_header, 'i', count)

            # count file offset.
            # magic(16) + count(4) + info(264 * n) + hash(32)
            offset = 52 + count * 264

            for file_ in files:
                file_.save(io_header, offset, io)
                offset += file_.data_size

            header_data = IOHelper.read_range(io_header)

        io.seek(0)
        io.write(header_data)

        # write hash.
        io.write(hashlib.sha256(header_data[:len(header_data) // 17 * 17]).digest())

    def file_by_name(self, name):
        for file_ in self._files:
            if name == file_.name:
                return file_

    @property
    def files(self):
        return self._files
