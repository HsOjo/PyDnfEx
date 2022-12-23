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

    def save(self, io=None, group_by_md5=True):
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
            if group_by_md5:
                self._callback_save_files_group_by_md5(offset, io_header, io)
            else:
                self._callback_save_files(offset, io_header, io)

            header_data = IOHelper.read_range(io_header)

        io.seek(0)
        io.write(header_data)

        # write hash.
        io.write(hashlib.sha256(header_data[:len(header_data) // 17 * 17]).digest())

    def _callback_save_files_group_by_md5(self, offset, io_header, io):
        files = self._files

        files_offset = {}
        for file in files:
            md5 = file.md5
            file_offset = files_offset.get(md5)
            if file_offset is None:
                file_offset = files_offset[md5] = offset
                offset += file.data_size
                file.save(io_header, file_offset, io)
            else:
                file.save(io_header, file_offset)

    def _callback_save_files(self, offset, io_header, io):
        files = self._files
        for file in files:
            file.save(io_header, offset, io)
            offset += file.data_size

    def file_by_name(self, name):
        for file in self._files:
            if name == file.name:
                return file

    def file_by_index(self, index):
        if 0 <= index < len(self._files):
            return self._files[index]

    @property
    def files(self):
        return self._files
