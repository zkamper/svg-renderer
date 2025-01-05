from matplotlib.colors import to_rgb, to_rgba
from PIL import ImageColor

class Styles:
    """
    Clasă ce reține stilurile elementelor.

    Stilurile acceptate sunt `fill`, `stroke` și `stroke-width`.
    :param attrib: atributele elementului
    """
    def __init__(self, attrib):
        if 'fill' in attrib and attrib['fill'] == 'none':
            self.fill = (0, 0, 0, 0)
        else:
            self.fill = ImageColor.getrgb(attrib.get('fill', 'white'))

        self.fill = tuple([c / 255.0 for c in self.fill])
        self.fill = to_rgb(self.fill) + (1,) if len(self.fill) == 3 else to_rgba(self.fill)

        if 'stroke' in attrib:
            self.stroke = ImageColor.getrgb(attrib['stroke'])
            self.stroke = tuple([c / 255.0 for c in self.stroke])
            self.stroke = to_rgb(self.stroke) + (1,) if len(self.stroke) == 3 else to_rgba(self.stroke)
        else:
            self.stroke = (0, 0, 0, 0)

        self.stroke_width = float(attrib.get('stroke-width', 1))

    def __copy__(self):
        return Styles({
            'fill': (self.fill[0], self.fill[1], self.fill[2], self.fill[3]),
            'stroke': (self.stroke[0], self.stroke[1], self.stroke[2], self.stroke[3]),
            'stroke-width': self.stroke,
        })