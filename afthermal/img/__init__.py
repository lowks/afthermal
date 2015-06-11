import os

from ..util import from_range
from .. import hw


# these images have been created with gimp; nd is the normally dithered
# (Floyd-Steinberg) version, while rb uses the "reduce bleeding" setting
LENA_ND_FN = os.path.join(os.path.dirname(__file__), 'lena-nd.png')
LENA_RB_FN = os.path.join(os.path.dirname(__file__), 'lena-rb.png')


class ObjectConverter(object):
    def __init__(self, printer):
        self.printer = printer

    def print_out(self, obj):
        self.printer.print_image(*self.convert(obj))

    def conert(self, obj):
        raise NotImplementedError


class ImageConverter(ObjectConverter):
    def __init__(self, printer, width=hw.DOTS_PER_LINE):

        super(ImageConverter, self).__init__(printer)

        # use from range to sanity check
        from_range(8, hw.DOTS_PER_LINE+1, 8, 'width')

        self.width = width

    def open(self):
        raise NotImplementedError

    def print_file(self, fn):
        img = self.open(fn)
        self.print_out(img)