from matplotlib.colors import to_rgb, to_rgba

class Styles:
    def __init__(self, attrib):
        self.fill = to_rgb(attrib.get('fill', 'white'))
        self.fill = [int(x * 255) for x in self.fill]
        exist_stroke = 1 if 'stroke' in attrib else 0
        self.stroke = to_rgba(attrib.get('stroke', 'black'), exist_stroke)
        self.stroke = [int(x * 255) for x in self.stroke]
        self.stroke_width = float(attrib.get('stroke-width', 1))

    def __copy__(self):
        return Styles({
            'fill': (self.fill[0], self.fill[1], self.fill[2]),
            'stroke': (self.stroke[0], self.stroke[1], self.stroke[2]),
            'stroke-width': self.stroke
        })