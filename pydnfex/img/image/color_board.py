from pydnfex.util.io_helper import IOHelper


class ColorBoard:
    def __init__(self):
        self._colors = []

    def add_color(self, color):
        self._colors.append(color)

    @staticmethod
    def open(io):
        cb = ColorBoard()

        [count] = IOHelper.read_struct(io, 'i')
        for i in range(count):
            color = IOHelper.read_struct(io, '<4B')
            cb.add_color(color)

        return cb

    def save(self, io):
        # color_count
        IOHelper.write_struct(io, 'i', len(self._colors))
        for color in self._colors:
            # color
            IOHelper.write_struct(io, '<4B', *color)

    @property
    def colors(self):
        return self._colors
