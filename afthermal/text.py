from contextlib import contextmanager

from .hw import get_command


# use HTML-like for text?
#
# <b>: bold
# <inv>: invert
# <updown>: upside down
# <u>: underline
# <dw>: double width
# <dh>: double height
# <del>: strike through


class Visitor(object):
    def visit(self, node):
        for cls in type(node).mro():
            meth = getattr(self, 'visit_' + cls.__name__, None)
            if meth is None:
                continue
            return meth(node)

        raise NotImplementedError('No visitation method visitor for {}'
                                  .format(node.__class__.__name__))


class Node(object):
    def __init__(self, *children):
        self.children = children


class ByteStringVisitor(Visitor):
    def __init__(self, encoding='ascii'):
        super(ByteStringVisitor, self).__init__()
        self.encoding = encoding

    def visit_FormatMode(self, node):
        buf = []
        buf.append(node.SEQ_ON)

        for child in node.children:
            buf.append(self.visit(child))

        buf.append(node.SEQ_OFF)

        return b''.join(buf)

    def visit_Text(self, node):
        return node.text.encode(self.encoding)


class FormatMode(Node):
    def _enter(self, encoding):
        raise NotImplementedError

    def _exit(self, encoding):
        raise NotImplementedError

    def to_bytestring(self, encoding='ascii'):
        buf = []
        buf.append(self._enter(encoding))

        for child in self.children:
            buf.append(child.to_bytestring(encoding))

        buf.append(self._exit(encoding))

        return b''.join(buf)


class Text(object):
    def __init__(self, text):
        self.text = text

    def to_bytestring(self, encoding='ascii'):
        # FIXME: escape special chars
        return self.text.encode(encoding)


class UpsideDown(FormatMode):
    SEQ_ON = get_command('set_updown_mode', 1)
    SEQ_OFF = get_command('set_updown_mode', 0)


class Invert(FormatMode):
    SEQ_ON = get_command('set_reverse_mode', 1)
    SEQ_OFF = get_command('set_reverse_mode', 0)


class Bold(FormatMode):
    SEQ_ON = get_command('set_font_bold', 1)
    SEQ_OFF = get_command('set_font_bold', 0)


class Underline(FormatMode):
    SEQ_ON = get_command('set_underline', 1)
    SEQ_OFF = get_command('set_underline', 0)


class Format(object):
    """Format text using printer specific escape sequences.

    :param bold: Enabled bold face.
    :param invert: Enable white-on-blasck priting.
    :param upside_down: Turn letters upside down.
    :param underline: Underline text.
    :param double_width: Print characters twice as wide.
    :param double_height: Print characters twice as high.
    :param strikethrough: Enable strikethrough.
    """
    def __init__(self, bold=False, invert=False, upside_down=False,
                 underline=False, double_width=False, double_height=False,
                 strikethrough=False):
        start = b''
        end = b''

        enlarge = 0
        if double_width:
            enlarge |= 32
        if double_height:
            enlarge |= 1

        if enlarge:
            start += get_command('set_font_enlarge', enlarge)
            end = get_command('set_font_enlarge', 0) + end

        self.start = start
        self.end = end

    def __call__(self, buf):
        """Format text using format escape sequences."""
        return self.start + buf + self.end

    @contextmanager
    def on(self, printer):
        """Enable formatting inside context manager."""
        printer.write(self.start)
        yield
        printer.write(self.end)
