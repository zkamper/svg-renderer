from element import Element
import cairo

class SVG(Element):
    def __init__(self, attrib: dict, children: list[Element]):
        super().__init__('svg', attrib)
        if 'width' not in attrib or 'height' not in attrib:
            raise ValueError('attribute \'width\' or \'height\' not found')
        self.width = int(attrib['width'].replace('px', ''))
        self.height = int(attrib['height'].replace('px', ''))
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        self.ctx = cairo.Context(self.surface)
        for child in children:
            self.add_child(child)

    def draw_element(self, ctx: cairo.Context):
        for child in self.children:
            child.draw_element(self.ctx)