from common.context import MyContext
from common.element import Element
import cairo

class SVG(Element):
    def __init__(self, attrib: dict, children: list[Element]):
        super().__init__('svg', attrib)
        if 'width' not in attrib or 'height' not in attrib:
            raise ValueError('attribute \'width\' or \'height\' not found')
        self.width = int(attrib['width'].replace('px', ''))
        self.height = int(attrib['height'].replace('px', ''))
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        self.ctx = MyContext(cairo.Context(self.surface), self.width, self.height)
        for child in children:
            self.add_child(child)

    def draw(self):
        for child in self.children:
            child.draw_element(self.ctx)
        self.surface.write_to_png('output.png')