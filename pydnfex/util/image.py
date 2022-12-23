from io import BytesIO

from PIL import Image
from PIL.DdsImagePlugin import DdsImageFile


def load_dds(data, box=None, rotate=0):
    with BytesIO(data) as io_dds:
        image = DdsImageFile(io_dds)
        if box is not None:
            image = image.crop(box)

        if rotate == 1:
            image = image.transpose(Image.ROTATE_90)

        return image.copy()


def load_raw(data, w, h, rotate=0):
    image = Image.frombytes('RGBA', (w, h), data)

    if rotate == 1:
        image = image.transpose(Image.ROTATE_90)

    return image
